# scripts/procesar_textos.py
import os
import re
from datetime import datetime
from django.conf import settings
from homicidios.models import Entidad, Homicidio


def procesar_textos():
    input_folder = os.path.join(settings.BASE_DIR, 'textos')

    # Recorre todos los archivos en la carpeta '../textos'
    for filename in os.listdir(input_folder):
        if filename.endswith('_v2_filtrado.txt'):
            # Extraer la fecha del nombre del archivo
            date_str = re.search(r'homicidios_(\d{8})', filename).group(1)
            fecha = datetime.strptime(date_str, '%d%m%Y').date()

            # Abrir el archivo y leer las líneas
            with open(os.path.join(input_folder, filename), 'r', encoding='utf-8') as file:
                lines = file.readlines()

            # Procesar cada línea del archivo
            for line in lines:
                match = re.match(r'^(.*?): (\d+)$', line.strip())
                if match:
                    nombre_entidad = match.group(1).strip()
                    homicidios = int(match.group(2))

                    # Buscar la entidad en la base de datos, o crearla si no existe
                    entidad, created = Entidad.objects.get_or_create(nombre=nombre_entidad)

                    # Guardar los datos de homicidios en la base de datos
                    Homicidio.objects.create(
                        entidad=entidad,
                        fecha=fecha,
                        total=homicidios  # Almacena el total de homicidios en el campo 'total'
                    )
            print(f"Archivo {filename} procesado con éxito.")
