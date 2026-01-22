import pymupdf
import pathlib
import glob
import os
import shutil

print("--- ЗАПУСК: СОЗДАНИЕ САЙТА ИЗ СКАНА ---")

# 1. Подготовка папок
if os.path.exists("docs"):
    shutil.rmtree("docs") # Удаляем старое, чтобы не мешало
    
# Создаем структуру: docs/assets (для картинок)
assets_folder = pathlib.Path("docs/assets")
assets_folder.mkdir(parents=True, exist_ok=True)

# 2. Находим твой файл
pdf_files = glob.glob("*.pdf")
if not pdf_files:
    print("ОШИБКА: PDF не найден в главной папке!")
    exit(1)

pdf_filename = pdf_files[0]
print(f"Обрабатываю файл: {pdf_filename}")

# 3. Открываем PDF
doc = pymupdf.open(pdf_filename)

# Начало текста для сайта
md_content = f"# {pdf_filename}\n\n"
md_content += "!!! info \"Информация\"\n    Это скан учебника. Листайте вниз для просмотра страниц.\n\n"

# 4. Проходим по страницам
for i, page in enumerate(doc):
    page_num = i + 1
    
    # Сохраняем картинку (jpg легче, чем png, сайт будет быстрее)
    image_name = f"page_{page_num}.jpg"
    # matrix=1.5 дает хорошее качество, но не огромный вес
    pix = page.get_pixmap(matrix=pymupdf.Matrix(1.5, 1.5))
    pix.save(assets_folder / image_name)
    
    # Добавляем страницу в файл сайта
    md_content += f"### Страница {page_num}\n\n"
    # Стандартный код картинки в Markdown
    md_content += f"![Стр {page_num}](assets/{image_name})\n\n"
    md_content += "---\n\n"
    
    if page_num % 10 == 0:
        print(f"Обработано {page_num} страниц...")

# 5. Сохраняем index.md
(pathlib.Path("docs") / "index.md").write_text(md_content, encoding='utf-8')

print("УСПЕХ! Сайт сгенерирован.")
