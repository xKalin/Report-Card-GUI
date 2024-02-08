from backend.ingestor.ingest_excel import IngestExcel
from backend.loader.excel_loader import ExcelLoader

print('hello')


loader = ExcelLoader()

dfs = loader.load_assessments()

print(dfs)