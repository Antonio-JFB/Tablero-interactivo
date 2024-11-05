import fitz  # PyMuPDF

# Ruta al archivo PDF
pdf_path = 'homicidios_03112024_v2.pdf'

# Abrir el archivo PDF
pdf_document = fitz.open(pdf_path)

# Verificar que el PDF tenga al menos una página
if pdf_document.page_count > 0:
    # Cargar solo la primera página (índice 0)
    page = pdf_document.load_page(0)
    
    # Convertir la página a imagen
    image = page.get_pixmap(dpi=300)  # Exportar con una resolución de 300 DPI
    
    # Guardar la imagen
    image_path = 'pagina_1.png'
    image.save(image_path)
    print(f"La primera página se ha guardado como {image_path}")
else:
    print("El PDF no contiene páginas.")

# Cerrar el documento PDF
pdf_document.close()
