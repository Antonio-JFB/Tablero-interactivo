import fitz  # PyMuPDF
import os

# Ruta relativa al archivo PDF
pdf_path = '../archivos/homicidios_01112024_v2.pdf'

# Extraer el nombre base del archivo sin la extensión
image_name = os.path.splitext(os.path.basename(pdf_path))[0]
# Ruta de la carpeta de salida
output_folder = '../imagenes'  # Ruta relativa para subir a 'Tablero-interactivo' y luego a 'imagenes'
# Ruta completa para guardar la imagen
image_path = os.path.join(output_folder, f"{image_name}.png")

# Abrir el archivo PDF
pdf_document = fitz.open(pdf_path)

# Verificar que el PDF tenga al menos una página
if pdf_document.page_count > 0:
    # Cargar solo la primera página (índice 0)
    page = pdf_document.load_page(0)

    # Convertir la página a imagen
    image = page.get_pixmap(dpi=300)  # Exportar con una resolución de 300 DPI

    # Crear la carpeta 'imagenes' si no existe
    os.makedirs(output_folder, exist_ok=True)

    # Guardar la imagen en la carpeta especificada
    image.save(image_path)
    print(f"La primera página se ha guardado como {image_path}")
else:
    print("El PDF no contiene páginas.")

# Cerrar el documento PDF
pdf_document.close()
