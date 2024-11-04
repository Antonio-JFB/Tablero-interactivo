import pdfplumber

def extract_first_page_text(pdf_path):
    # Abre el archivo PDF
    with pdfplumber.open(pdf_path) as pdf:
        # Extrae el texto de la primera página
        first_page = pdf.pages[0]
        text = first_page.extract_text()
    return text

# Ruta al archivo PDF
pdf_path = "archivos/homicidios_01112024_v2.pdf"
texto_primera_pagina = extract_first_page_text(pdf_path)

# Imprime el texto extraído
print("Texto de la primera página:")
print(texto_primera_pagina)
