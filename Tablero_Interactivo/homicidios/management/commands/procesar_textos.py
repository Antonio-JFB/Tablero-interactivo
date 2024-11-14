from django.core.management.base import BaseCommand
from homicidios.models import Entidad, Homicidio
import os
import re
from datetime import datetime
from django.conf import settings
from django.db import transaction


class Command(BaseCommand):
    help = 'Procesa los archivos de texto con datos de homicidios y los guarda en la base de datos'

    def handle(self, *args, **kwargs):
        input_folder = os.path.join(settings.BASE_DIR, 'textos')

        for filename in os.listdir(input_folder):
            if filename.endswith('_v2_filtrado.txt'):
                date_str = re.search(r'homicidios_(\d{8})', filename).group(1)
                fecha = datetime.strptime(date_str, '%d%m%Y').date()

                with open(os.path.join(input_folder, filename), 'r', encoding='utf-8') as file:
                    lines = file.readlines()

                registros = []  # Lista para almacenar registros de homicidios para `bulk_create`

                for line in lines:
                    match = re.match(r'^(.*?): (\d+)$', line.strip())
                    if match:
                        nombre_entidad = match.group(1).strip()
                        homicidios = int(match.group(2))

                        # Buscar o crear la entidad
                        entidad, created = Entidad.objects.get_or_create(nombre=nombre_entidad)

                        # Evitar duplicados
                        if not Homicidio.objects.filter(entidad=entidad, fecha=fecha).exists():
                            registros.append(Homicidio(entidad=entidad, fecha=fecha, total=homicidios))

                # Inserción en la base de datos en lotes con `bulk_create`
                Homicidio.objects.bulk_create(registros)
                self.stdout.write(self.style.SUCCESS(
                    f"Archivo {filename} procesado con éxito. {len(registros)} registros guardados."))
