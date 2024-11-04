# Dashboard de Homicidios Dolosos en México

Este proyecto es un **Dashboard interactivo** para visualizar y analizar datos de homicidios dolosos en México. La aplicación permite a los usuarios explorar información sobre homicidios a nivel nacional, estatal y municipal, proporcionando un análisis visual de las tendencias y estadísticas de seguridad en el país.

## Descripción del Proyecto

El Dashboard de Homicidios Dolosos ofrece una plataforma interactiva para analizar los datos de homicidios reportados en México, permitiendo filtrar la información por fechas, regiones y otras categorías relevantes. Utiliza datos oficiales de homicidios dolosos, que se descargan y actualizan diariamente desde el portal de seguridad pública del gobierno.

### Funcionalidades Principales

1. **Descarga Automática de Datos**: El sistema descarga diariamente los archivos PDF con datos de homicidios dolosos desde el portal [Informe Seguridad CNS](http://www.informeseguridad.cns.gob.mx/).
2. **Extracción de Datos de PDF**: Se utiliza OCR (reconocimiento óptico de caracteres) para convertir el texto de los PDF en datos estructurados.
3. **Procesamiento y Almacenamiento**: Los datos se procesan y almacenan en una base de datos para facilitar el análisis y la consulta.
4. **Visualización de Datos Interactiva**: El dashboard presenta los datos en forma de gráficos y tablas, permitiendo a los usuarios explorar las estadísticas por estado, municipio, fecha y otros criterios.
5. **Autenticación de Usuarios**: Permite que solo usuarios autorizados accedan al dashboard para proteger los datos y asegurar la privacidad de la información.

### Tecnologías Utilizadas

- **Python**: Para la lógica de backend y procesamiento de datos.
- **Tesseract OCR**: Para extraer texto de archivos PDF.
- **Django/Dash/Streamlit**: Para la creación y visualización de gráficos en el dashboard.
- **SQLite/PostgreSQL**: Para el almacenamiento de datos.
- **Requests**: Para la descarga automática de los archivos PDF.

## Instalación y Configuración

### Requisitos Previos

- **Python 3.7+**
- **Tesseract OCR**: Debe estar instalado en tu sistema. Puedes descargarlo [aquí](https://github.com/tesseract-ocr/tesseract).
- Librerías adicionales de Python:
  ```bash
  pip install pytesseract pdf2image requests Django
