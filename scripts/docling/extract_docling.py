import time # Tempo de execucao

from pathlib import Path # Adicionado para gerenciar as pastas
from datetime import datetime # Adicionado para colocar data no nome do arquivo

start = time.time()  # Marca o início da velocidade de processamento

print(f"Start time", start)
# --------- Implementacao do Código do Site do Docling ---------

from docling.datamodel.base_models import InputFormat # Importa uma lista de formatos que a biblioteca aceita
from docling.datamodel.pipeline_options import ( # Importa as ferramentas de configuração
    TesseractOcrOptions, # Controla como o PDF é processado
    PdfPipelineOptions, # Permite configurar o motor de leitura de imagens (OCR)
)
from docling.document_converter import DocumentConverter, PdfFormatOption # DocumentConverter: faz a conversão PdfFormatOption: liga as configurações de PDF ao conversor


pipeline_options = PdfPipelineOptions() # Cria um objeto de configuração vazio para PDFs
pipeline_options.do_ocr = False # Força a biblioteca a tentar ler o texto mesmo que ele seja uma imagem
# Obs: Mudado para False, pois nao estou precisando ler imagens no momento

pipeline_options.ocr_options = TesseractOcrOptions()  # Usa o Tesseract, lê as imagens

print("Cria doc conversor")
doc_converter = DocumentConverter( # Cria o conversor
    format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
)

print("Converte o arquivo")
# --------- Converte o arquivo ---------
# result = doc_converter.convert("data/sample.pdf") # teste com docs simples
# result = doc_converter.convert("data/research-papers.pdf") # teste com artigo cientifico
result = doc_converter.convert("data/table.pdf") # teste docs com tabela
# result = doc_converter.convert("data/symbols.pdf") # teste com simbolos

# --------- Opcoes de output ---------
# 1. MARKDOWN (O que você já estava usando)
#print("--- SAÍDA MARKDOWN ---")
#print(result.document.export_to_markdown())

# 2. JSON (Estrutura da IA e metadados)
# print("--- SAÍDA JSON ---")
# print(result.document.export_to_dict()) 

# 3. HTML (Visual para web)
# print("--- SAÍDA HTML ---")
# print(result.document.export_to_html())

print("Printa o doc")
# 4. TEXTO PURO (Sem nenhuma formatação, apenas as palavras)
print("--- SAÍDA TEXTO PURO ---")
print(result.document.export_to_text())

# 5. DOCTAGS (Formato especial do Docling para treinamento de modelos)
# print("--- SAÍDA DOCTAGS ---")
# print(result.document.export_to_document_tokens())

# --------- Marca o fim da velocidade de processamento ---------
end = time.time()     
print(f"Velocidade de processamento: {end - start:.2f} segundos")

# --------- Salvamento do Output ---------

# 1. Define onde salvar (Cria uma pasta 'outputs' dentro de 'scripts/docling/')
output_dir = Path(__file__).parent / "outputs"
output_dir.mkdir(parents=True, exist_ok=True)

# 2. Cria um nome único com data e hora para não sobrescrever o anterior
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = output_dir / f"teste_{timestamp}.txt"

# 3. Salva o conteúdo em Markdown (ou troque para .txt se preferir)
duration = end - start

print("Salva o conteúdo em Markdown")

with open(output_file, "w", encoding="utf-8") as f:
    f.write(result.document.export_to_markdown())
    # Adicionamos o tempo de execução no final do arquivo salvo para seu controle
    f.write(f"\n\n--- Tempo de processamento: {duration:.2f}s ---")

print("Terminou de processa o file")
print(f"\n✅ Teste salvo com sucesso em: {output_file}")









# Teste usando Docling de forma mais simples
''''
from docling.document_converter import DocumentConverter  

source = ".data/research-papers.pdf" 
converter = DocumentConverter() 
doc = converter.convert(source).document 
print(doc.export_to_markdown())
'''
