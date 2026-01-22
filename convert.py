import pymupdf
import pathlib
import glob
import os
import shutil

print("--- ПОПЫТКА №3: РОДНОЙ ФОРМАТ ---")

# 1. Чистим папку docs, чтобы не было мусора
if os.path.exists("docs"):
    shutil.rmtree("docs")
    
# Создаем папки заново
img_folder = pathlib.Path("docs/assets") # Назовем папку assets, так надежнее
img_folder.mkdir(parents=True, exist_ok=True)

# 2. Ищем PDF
pdf_files = glob.glob("*.pdf")
if not pdf_files:
    # Если PDF нет, создаем аварийную страницу
    (pathlib.Path("docs") / "index.md").write_text("# ОШИБКА: Нет файла PDF в репозитории!", encoding='utf-8')
    exit(1)

pdf_filename = pdf_files[0]
print(f"Обрабатываю: {pdf_filename}")

try:
    doc = pymupdf.open(pdf_filename)
except Exception as e:
    print(f"Файл битый: {e}")
    exit(1)

# 3. Генерируем контент
md_content = f"# Учебник: {pdf_filename}\n\n"
md_content += "Если вы видите этот текст, значит сайт работает. Листайте вниз.\n\n"

# Настройки качества (dpi=100 - это баланс, чтобы телефон не вис, но текст был четким)
# Если поставить больше, сайт может не загрузиться.
matrix = pymupdf.Matrix(1.2, 1.2) 

for i, page in enumerate(doc):
    page_num = i + 1
    image_name = f"page_{page_num}.jpg" # Используем JPG, они легче PNG
    
    # Сохраняем картинку
    pix = page.get_pixmap(matrix=matrix)
    pix.save(img_folder / image_name)
    
    # ВОТ ГЛАВНОЕ ИЗМЕНЕНИЕ:
    # Используем стандартный Markdown (![текст](путь)), а не HTML.
    # Это 100% понимает любой движок.
    md_content += f"## Страница {page_num}\n\n"
    md_content += f"![Стр {page_num}](assets/{image_name})\n\n"
    md_content += "---\n\n"
    
    # Пишем в лог каждые 10 страниц
    if page_num % 10 == 0:
        print(f"Сделано {page_num} из {len(doc)}")

# 4. Сохраняем файл сайта
(pathlib.Path("docs") / "index.md").write_text(md_content, encoding='utf-8')

print("УСПЕХ! Код сгенерирован в безопасном формате.")
