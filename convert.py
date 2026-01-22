import pymupdf # Это база для работы с PDF
import pathlib
import glob
import os

print("--- ЗАПУСК В РЕЖИМЕ КАРТИНОК (SCAN MODE) ---")

# 1. Ищем файл
pdf_files = glob.glob("*.pdf")
if not pdf_files:
    print("ОШИБКА: PDF файл не найден!")
    exit(1)

pdf_filename = pdf_files[0]
doc = pymupdf.open(pdf_filename)

# 2. Подготовка папок
docs_folder = pathlib.Path("docs")
docs_folder.mkdir(exist_ok=True)

# Сюда будем писать код страницы сайта
md_content = f"# Учебник: {pdf_filename}\n\n"
md_content += "**Примечание:** Это скан учебника. Поиск по тексту недоступен.\n\n"

print(f"Всего страниц: {len(doc)}")

# 3. Проходим по каждой странице
for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    
    # Делаем картинку (zoom=2 улучшает качество в 2 раза)
    pix = page.get_pixmap(matrix=pymupdf.Matrix(2, 2))
    
    image_name = f"page_{page_num + 1}.png"
    image_path = docs_folder / image_name
    
    # Сохраняем картинку в папку docs
    pix.save(image_path)
    
    # Добавляем картинку в markdown файл
    md_content += f"## Страница {page_num + 1}\n\n"
    md_content += f"![Страница {page_num + 1}]({image_name})\n\n"
    md_content += "---\n\n" # Разделитель
    
    if (page_num + 1) % 10 == 0:
        print(f"Обработано {page_num + 1} страниц...")

# 4. Сохраняем главный файл сайта
(docs_folder / "index.md").write_text(md_content, encoding='utf-8')

print("Готово! Все страницы превращены в картинки для сайта.")
