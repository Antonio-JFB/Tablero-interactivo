import fitz  # PyMuPDF
import os

# Carpetas de entrada y salida
input_folder = '../archivos'   # Carpeta con los archivos PDF
output_folder_images = '../imagenes'  # Carpeta para guardar las imágenes
output_folder_texts = '../textos'     # Carpeta para guardar los textos

# Crear las carpetas de salida si no existen
os.makedirs(output_folder_images, exist_ok=True)
os.makedirs(output_folder_texts, exist_ok=True)

# Recorrer todos los archivos en la carpeta de entrada
for filename in os.listdir(input_folder):
    # Verificar si el archivo tiene extensión .pdf
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(input_folder, filename)

        # Extraer el nombre base del archivo sin la extensión
        base_name = os.path.splitext(filename)[0]

        # Rutas de salida para la imagen y el texto
        image_path = os.path.join(output_folder_images, f"{base_name}.png")
        text_path = os.path.join(output_folder_texts, f"{base_name}.txt")

        # Abrir el archivo PDF
        pdf_document = fitz.open(pdf_path)

        # Verificar que el PDF tenga al menos una página
        if pdf_document.page_count > 0:
            # Cargar solo la primera página (índice 0)
            page = pdf_document.load_page(0)

            # Convertir la página a imagen
            image = page.get_pixmap(dpi=300)
            image.save(image_path)
            print(f"La primera página de '{filename}' se ha guardado como imagen en {image_path}")

            # Extraer el texto de la primera página
            page_text = page.get_text("text")
            with open(text_path, 'w', encoding='utf-8') as text_file:
                text_file.write(page_text)
            print(f"El texto de la primera página de '{filename}' se ha guardado en {text_path}")
        else:
            print(f"El archivo '{filename}' no contiene páginas.")

        # Cerrar el documento PDF
        pdf_document.close()
