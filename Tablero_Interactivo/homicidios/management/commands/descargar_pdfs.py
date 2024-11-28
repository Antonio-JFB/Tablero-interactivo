import os
import re
import requests
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Descarga automáticamente los archivos PDF de homicidios que faltan desde el servidor oficial."

    def handle(self, *args, **kwargs):
        # Definir la ruta de la carpeta de destino
        carpeta_destino = os.path.join(settings.BASE_DIR, 'archivos')

        # Asegurarse de que la carpeta existe
        os.makedirs(carpeta_destino, exist_ok=True)
        self.stdout.write("Carpeta de destino asegurada: " + carpeta_destino)

        # Obtener la fecha de inicio
        inicio = self.obtener_ultima_fecha(carpeta_destino) + timedelta(days=1)
        fin = datetime.now()

        self.stdout.write(f"Iniciando descarga desde {inicio.strftime('%d-%m-%Y')} hasta {fin.strftime('%d-%m-%Y')}")

        # Iterar sobre el rango de fechas y descargar los archivos
        fecha_actual = inicio
        archivos_descargados = 0
        while fecha_actual <= fin:
            fecha_str = fecha_actual.strftime('%d%m%Y')
            url = f"http://informeseguridad.cns.gob.mx/files/homicidios_{fecha_str}_v2.pdf"
            if self.descargar_pdf(url, fecha_str, carpeta_destino):
                archivos_descargados += 1
            fecha_actual += timedelta(days=1)

        self.stdout.write(f"Descarga completada. Total de archivos descargados: {archivos_descargados}")

    def obtener_ultima_fecha(self, carpeta_destino):
        """Encuentra la fecha del último archivo descargado en la carpeta de destino."""
        archivos = os.listdir(carpeta_destino)
        fechas = []

        # Extraer fechas de los archivos que siguen el patrón 'homicidios_DDMMYYYY_v2.pdf'
        for archivo in archivos:
            match = re.search(r'homicidios_(\d{8})_v2\.pdf', archivo)
            if match:
                fecha_str = match.group(1)
                fecha = datetime.strptime(fecha_str, '%d%m%Y')
                fechas.append(fecha)

        # Retornar la fecha más reciente, o una fecha inicial si no hay archivos
        return max(fechas) if fechas else datetime(2019, 4, 3)

    def descargar_pdf(self, url, fecha_str, carpeta_destino):
        """Descarga el archivo PDF de la URL especificada si no existe."""
        filename_v2 = os.path.join(carpeta_destino, f"homicidios_{fecha_str}_v2.pdf")

        if os.path.exists(filename_v2):
            self.stdout.write(self.style.WARNING(f"Ya existe: {filename_v2}"))
            return False

        response = requests.get(url)
        if response.status_code == 200:
            with open(filename_v2, 'wb') as file:
                file.write(response.content)
            self.stdout.write(self.style.SUCCESS(f"Descargado: {filename_v2}"))
            return True
        else:
            self.stdout.write(self.style.ERROR(f"El archivo {url} no está disponible."))
            return False
