import pymupdf4llm
import pathlib
import os

pdf_filename = "book.pdf"
docs_folder = "docs"

if not os.path.exists(pdf_filename):
    print(f"Error: {pdf_filename} not found!")
    exit(1)

# Конвертация
md_text = pymupdf4llm.to_markdown(pdf_filename)

# Создание папки
pathlib.Path(docs_folder).mkdir(exist_ok=True)

# Запись файла
header = "# Учебник Биологии (5 класс)\n\n"
output_path = pathlib.Path(docs_folder) / "index.md"
output_path.write_text(header + md_text, encoding='utf-8')

print("Conversion complete.")
