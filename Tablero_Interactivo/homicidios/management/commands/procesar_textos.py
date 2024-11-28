import os
import re
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from homicidios.models import Entidad, Homicidio
from cnocr import CnOcr
import fitz  # PyMuPDF
from django.db import transaction


class Command(BaseCommand):
    help = "Convierte PDFs a texto, procesa los datos de homicidios y los guarda en la base de datos"

    def handle(self, *args, **kwargs):
        # Carpetas de entrada y salida
        pdf_folder = os.path.join(settings.BASE_DIR, 'archivos')  # PDFs de entrada
        image_folder = os.path.join(settings.BASE_DIR, 'imagenes')  # Imágenes generadas
        text_folder = os.path.join(settings.BASE_DIR, 'textos')  # Textos generados

        # Crear carpetas de salida si no existen
        os.makedirs(image_folder, exist_ok=True)
        os.makedirs(text_folder, exist_ok=True)

        # Expresión regular para entidades y homicidios
        pattern = re.compile(r"([A-Za-zÁÉÍÓÚáéíóúÑñ\s]+?)\s*(\d+)")

        # Instanciar el OCR
        ocr = CnOcr()

        # Procesar los PDFs
        self.stdout.write("=== Iniciando procesamiento de PDFs a texto ===")
        pdf_count = 0
        for filename in os.listdir(pdf_folder):
            if filename.endswith('.pdf'):
                pdf_count += 1
                self.stdout.write(f"Procesando archivo PDF: {filename}")
                pdf_path = os.path.join(pdf_folder, filename)
                base_name = os.path.splitext(filename)[0]

                image_path = os.path.join(image_folder, f"{base_name}.png")
                text_path = os.path.join(text_folder, f"{base_name}_filtrado.txt")

                # Procesar el PDF
                self.process_pdf(pdf_path, image_path, text_path, ocr, pattern)

        if pdf_count == 0:
            self.stdout.write("No se encontraron archivos PDF en la carpeta de entrada.")
        else:
            self.stdout.write(f"=== Procesamiento de PDFs completado. Total de PDFs procesados: {pdf_count} ===")

        # Procesar los textos generados
        self.stdout.write("=== Iniciando carga de datos en la base de datos ===")
        self.process_texts(text_folder)
        self.stdout.write("=== Carga de datos completada ===")

    def process_pdf(self, pdf_path, image_path, text_path, ocr, pattern):
        """Convierte la primera página del PDF a imagen, extrae texto con OCR y filtra datos."""
        pdf_document = fitz.open(pdf_path)

        if pdf_document.page_count > 0:
            page = pdf_document.load_page(0)
            image = page.get_pixmap(dpi=300)
            image.save(image_path)

            self.stdout.write(f"Imagen generada: {image_path}")

            out = ocr.ocr(image_path)
            extracted_text = "\n".join([item['text'] for item in out])
            filtered_data = pattern.findall(extracted_text)
            filtered_text = "\n".join([f"{entidad.strip()}: {homicidios}" for entidad, homicidios in filtered_data])

            with open(text_path, 'w', encoding='utf-8') as text_file:
                text_file.write(filtered_text)

            self.stdout.write(f"Texto filtrado guardado: {text_path}")

        else:
            self.stdout.write(f"El archivo '{pdf_path}' no tiene páginas.")

        pdf_document.close()

    @transaction.atomic
    def process_texts(self, text_folder):
        """Procesa los archivos de texto generados y guarda los datos en la base de datos."""
        text_count = 0
        record_count = 0
        duplicate_count = 0

        for filename in os.listdir(text_folder):
            if filename.endswith('_filtrado.txt'):
                text_count += 1
                self.stdout.write(f"Procesando archivo de texto: {filename}")

                match = re.search(r'(\d{8})', filename)
                if not match:
                    self.stdout.write(f"No se encontró una fecha válida en el archivo: {filename}")
                    continue

                date_str = match.group(1)
                fecha = datetime.strptime(date_str, '%d%m%Y').date()

                with open(os.path.join(text_folder, filename), 'r', encoding='utf-8') as file:
                    lines = file.readlines()

                registros = []
                for line in lines:
                    match = re.match(r'^(.*?): (\d+)$', line.strip())
                    if match:
                        nombre_entidad = match.group(1).strip()
                        homicidios = int(match.group(2))

                        entidad, _ = Entidad.objects.get_or_create(nombre=nombre_entidad)

                        if not Homicidio.objects.filter(entidad=entidad, fecha=fecha).exists():
                            registros.append(Homicidio(entidad=entidad, fecha=fecha, total=homicidios))
                        else:
                            duplicate_count += 1
                            self.stdout.write(self.style.WARNING(
                                f"Registro duplicado omitido: {nombre_entidad}, Fecha: {fecha}, Total: {homicidios}"
                            ))

                Homicidio.objects.bulk_create(registros)
                record_count += len(registros)

                self.stdout.write(self.style.SUCCESS(
                    f"Archivo {filename} procesado con éxito. {len(registros)} registros guardados, {duplicate_count} duplicados omitidos."
                ))

        if text_count == 0:
            self.stdout.write("No se encontraron archivos de texto para procesar.")
        else:
            self.stdout.write(f"=== Total de archivos de texto procesados: {text_count} ===")
            self.stdout.write(f"=== Total de registros guardados en la base de datos: {record_count} ===")
            self.stdout.write(f"=== Total de registros duplicados omitidos: {duplicate_count} ===")
