import pymupdf
import pathlib
import glob
import os
import shutil

print("--- ЗАПУСК: ЖЕЛЕЗОБЕТОННЫЙ ВАРИАНТ ---")

# 1. Очистка старого (чтобы не было путаницы)
if os.path.exists("docs"):
    shutil.rmtree("docs")
pathlib.Path("docs/img").mkdir(parents=True, exist_ok=True)

# 2. Ищем PDF
pdf_files = glob.glob("*.pdf")
if not pdf_files:
    print("ОШИБКА: PDF файл не найден! Загрузи его в корень репозитория.")
    exit(1)

pdf_filename = pdf_files[0]
doc = pymupdf.open(pdf_filename)
print(f"Обрабатываю учебник: {pdf_filename} ({len(doc)} страниц)")

# 3. Создаем контент
md_content = f"# {pdf_filename}\n\n"
md_content += "Если картинки не грузятся — обновите страницу через минуту.\n\n"

for i, page in enumerate(doc):
    page_num = i + 1
    
    # Имя файла: просто цифра, чтобы не было проблем с путями
    image_filename = f"{page_num}.png"
    # Сохраняем в папку docs/img/
    image_path = pathlib.Path(f"docs/img/{image_filename}")
    
    # Рендерим картинку (zoom=1.5 — баланс качества и скорости)
    pix = page.get_pixmap(matrix=pymupdf.Matrix(1.5, 1.5))
    pix.save(image_path)
    
    # Используем HTML тег <img>, он надежнее, чем Markdown
    # loading="lazy" ускоряет загрузку сайта
    md_content += f"### Страница {page_num}\n"
    md_content += f'<img src="img/{image_filename}" alt="Страница {page_num}" width="100%" loading="lazy" />\n\n'
    md_content += "---\n\n"
    
    if page_num % 20 == 0:
        print(f"Готово {page_num} страниц...")

# 4. Записываем index.md
(pathlib.Path("docs") / "index.md").write_text(md_content, encoding='utf-8')

print("УСПЕХ! Все картинки разложены по папкам.")
