import shutil
import pathlib
import glob
import os

print("--- ПЛАН Б: ВСТРАИВАНИЕ PDF ЦЕЛИКОМ ---")

# 1. Подготовка папки
if os.path.exists("docs"):
    shutil.rmtree("docs")
pathlib.Path("docs").mkdir(exist_ok=True)

# 2. Ищем твой файл
pdf_files = glob.glob("*.pdf")
if not pdf_files:
    print("ОШИБКА: Файл PDF не найден! Загрузи его в репозиторий.")
    exit(1)

original_pdf = pdf_files[0]
# Копируем файл внутрь папки сайта под простым именем book.pdf
target_pdf = "docs/book.pdf"

print(f"Копирую {original_pdf} -> {target_pdf}")
shutil.copy(original_pdf, target_pdf)

# 3. Создаем страницу просмотра
# Мы используем специальный HTML-код, который говорит браузеру: "Покажи PDF здесь"
md_content = """# Учебник Биологии

<a href="book.pdf" target="_blank" style="background: green; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block; margin-bottom: 20px;">
   📥 Скачать / Открыть на весь экран
</a>

Если учебник не отображается ниже, нажмите кнопку выше.

<div style="height: 90vh; width: 100%;">
    <iframe src="book.pdf" width="100%" height="100%" style="border: none;">
    Ваш браузер не поддерживает встроенные PDF.
    </iframe>
</div>
"""

(pathlib.Path("docs") / "index.md").write_text(md_content, encoding='utf-8')

print("ГОТОВО! PDF встроен в сайт.")
