## Setup

Cria ambiente virtual
```bash
python3 -m venv .venv
```

Ativa ambiente virtual
```bash
source .venv/bin/activate
```

Instala o projeto em modo editável (alinha com o `pyproject.toml`):

```bash
pip install -e ".[dev]"
```

## Avaliador (benchmark)

Compara bibliotecas num PDF e gera um JSON com critérios agrupados (velocidade, layout, tabelas, saída, dependências, rubricas de engenharia, acurácia opcional).

Execute na raiz do repositório (para os caminhos relativos a `dataset/` funcionarem):

```bash
python -m document_extraction_benchmark.main --lib pypdf --file dataset/sample.pdf
python -m document_extraction_benchmark.main --lib pdfminer.six --file dataset/sample.pdf -o report.json
python -m document_extraction_benchmark.main --lib pymupdf --file dataset/sample.pdf --repeat 3 --warmup 1
python -m document_extraction_benchmark.main --lib pdfplumber --file dataset/sample.pdf --ground-truth expected.txt
```

Bibliotecas suportadas no `--lib`: `docling`, `pymupdf`, `pdfplumber`, `pdfminer` (alias de `pdfminer.six`), `pypdf`.

Critérios **automáticos** incluem tempo médio de `extract()`, heurísticas de layout, contagens de tabela, metadados de saída, `requires()` da distribuição PyPI, linhas do adaptador neste repositório, e (se `--ground-truth` for passado) similaridade aproximada de texto. Rubricas em `metrics/engineering.py` são **rótulos estáticos** para relatório (validar na documentação de cada lib).

**Docling:** na primeira execução pode baixar modelos (Hugging Face). Teste de smoke opcional: `RUN_DOCLING_SMOKE=1 pytest tests/test_smoke_extract.py::test_docling_run_evaluation`.

## Testes

```bash
pytest
```