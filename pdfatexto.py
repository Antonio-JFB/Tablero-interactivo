import pytesseract
from pdf2image import convert_from_path

# Specify the path to the Tesseract executable (update if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract_text_from_pdf(pdf_path):
    # Convert PDF pages to images
    pages = convert_from_path(pdf_path)

    # Extract text from each page image
    text = ''
    for page in pages:
        text += pytesseract.image_to_string(page) + '\n'

    return text


# Example usage
pdf_file_path = 'homicidios_17102024_v2.pdf '
extracted_text = extract_text_from_pdf(pdf_file_path)
print(extracted_text)
