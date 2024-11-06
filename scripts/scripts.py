import fitz  # PyMuPDF
import os

# Ruta relativa al archivo PDF
pdf_path = '../archivos/homicidios_01112024_v2.pdf'

# Extraer el nombre base del archivo sin la extensión
base_name = os.path.splitext(os.path.basename(pdf_path))[0]

# Ruta de la carpeta de salida
output_folder = '../imagenes'  # Carpeta de salida para la imagen
text_folder = '../textos'      # Carpeta de salida para el texto

# Rutas completas para guardar la imagen y el texto
image_path = os.path.join(output_folder, f"{base_name}.png")
text_path = os.path.join(text_folder, f"{base_name}.txt")

# Abrir el archivo PDF
pdf_document = fitz.open(pdf_path)

# Crear las carpetas de salida si no existen
os.makedirs(output_folder, exist_ok=True)
os.makedirs(text_folder, exist_ok=True)

# Verificar que el PDF tenga al menos una página
if pdf_document.page_count > 0:
    # Cargar solo la primera página (índice 0)
    page = pdf_document.load_page(0)

    # Convertir la página a imagen
    image = page.get_pixmap(dpi=300)  # Exportar con una resolución de 300 DPI
    image.save(image_path)
    print(f"La primera página se ha guardado como imagen en {image_path}")

    # Extraer el texto de la primera página
    page_text = page.get_text("text")
    with open(text_path, 'w', encoding='utf-8') as text_file:
        text_file.write(page_text)
    print(f"El texto de la primera página se ha guardado en {text_path}")
else:
    print("El PDF no contiene páginas.")

# Cerrar el documento PDF
pdf_document.close()
