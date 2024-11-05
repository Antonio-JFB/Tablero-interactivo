import requests
from datetime import datetime, timedelta


# Función para descargar el PDF
def descargar_pdf(url, fecha):
    response = requests.get(url)
    if response.status_code == 200:
        filename = f"homicidios_{fecha}.pdf"
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Descargado: {filename}")
    else:
        print(f"El archivo {url} no está disponible.")


# Rango de fechas
inicio = datetime(2019, 1, 1)
fin = datetime(2024, 8, 31)

# Iterar sobre el rango de fechas
fecha_actual = inicio
while fecha_actual <= fin:
    # Formatear la fecha como DDMMYYYY
    fecha_str = fecha_actual.strftime('%d%m%Y')

    # Generar la URL
    url = f"http://informeseguridad.cns.gob.mx/files/homicidios_{fecha_str}.pdf"

    # Descargar el archivo PDF
    descargar_pdf(url, fecha_str)

    # Avanzar al siguiente día
    fecha_actual += timedelta(days=1)

