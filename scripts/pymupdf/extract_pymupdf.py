import time # Tempo de execucao

from pathlib import Path # Adicionado para gerenciar as pastas
from datetime import datetime # Adicionado para colocar data no nome do arquivo
start = time.time()  # Marca o início da velocidade de processamento 

import pymupdf

# open a document
# doc = pymupdf.open("data/sample.pdf")
doc = pymupdf.open("data/research-papers.pdf") 
# doc = pymupdf.open("data/symbols.pdf") 
# doc = pymupdf.open("data/table.pdf") 


out = open("scripts/pymupdf/outputs/output_pymupdf.txt", "wb") # create a text output

for page in doc: # iterate the document pages
    
    print(f"Processando pagina {page.number + 1}")

    text = page.get_text().encode("utf8") # get plain text (is in UTF-8)
    out.write(text) # write text of page
    out.write(bytes((12,))) # write page delimiter (form feed 0x0C)
out.close()

end = time.time() 
duration = end - start

# Extracao na ordem de leitura
print("Ordem de leitura")
header = "Header"  # text in header
for page in doc:
    page.insert_text((50, 50), header)  # insert header
    page.insert_text(  # insert footer 50 points above page bottom
        (50, page.rect.height - 50),
        f"Page {page.number + 1} of {doc.page_count}", # text in footer
    )
print("Fim")

# Extrai as imagens inteiras do arquivo
''''
for page_index in range(len(doc)): # iterate over pdf pages
    page = doc[page_index] # get the page
    image_list = page.get_images()

    # print the number of images found on the page
    if image_list:
        print(f"Found {len(image_list)} images on page {page_index}")
    else:
        print("No images found on page", page_index)

    for image_index, img in enumerate(image_list, start=1): # enumerate the image list
        xref = img[0] # get the XREF of the image
        pix = pymupdf.Pixmap(doc, xref) # create a Pixmap

        if pix.n - pix.alpha > 3: # CMYK: convert to RGB first
            pix = pymupdf.Pixmap(pymupdf.csRGB, pix)

        pix.save(f"page_{page_index}-image_{image_index}.png") # save the image as png
        pix = None
'''



print("Extração concluída com sucesso!")
print((f"\n\n--- Tempo de processamento: {duration:.2f}s ---"))