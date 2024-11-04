import pytesseract
from pdf2image import convert_from_path

# Especifica la ruta al ejecutable de Tesseract (actualiza si es necesario)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_pdf(pdf_path):
    # Convierte las páginas del PDF a imágenes
    pages = convert_from_path(pdf_path)

    # Extrae el texto de cada página
    text = ''
    for page in pages:
        text += pytesseract.image_to_string(page) + '\n'

    return text

# Ruta del archivo PDF
pdf_file_path = 'homicidios_17102024_v2.pdf'

# Extrae el texto del PDF
extracted_text = extract_text_from_pdf(pdf_file_path)

# Guarda el texto extraído en un archivo de texto
output_text_file = 'homicidios_17102024_v2.txt'
with open(output_text_file, 'w', encoding='utf-8') as file:
    file.write(extracted_text)

print(f"Texto extraído y guardado en {output_text_file}")
