from cnocr import CnOcr

img_fp = '../imagenes/homicidios_01112024_v2.png'
ocr = CnOcr()  # Usa valores predeterminados
out = ocr.ocr(img_fp)

# Filtramos solo el texto y lo mostramos en una lista más legible
for item in out:
    print(item['text'])
