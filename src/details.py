#___________Not Used in the Current Implementation____________________


from bs4 import BeautifulSoup
from docx import Document
import os
import re
import time


def convert_job_page(driver,output_folder):

    os.makedirs(output_folder, exist_ok=True)

    # Get complete rendered HTML
    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")

    # Remove unnecessary HTML elements
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()

    # Extract readable text
    text = soup.get_text(separator="\n", strip=True)

    title = soup.title.get_text(strip=True) if soup.title else "Job"
    filename = re.sub(r'[\\/*?:"<>|]', "_", title)

    # 1. Save as TXT
    txt_path = os.path.join(
        output_folder, f"{filename}.txt"
    )

    with open(txt_path, "w", encoding="utf-8") as file:
        file.write(text)

    # 2. Save as Word
    doc = Document()
    doc.add_heading(title, level=1)
    doc.add_paragraph(text)

    docx_path = os.path.join(
        output_folder, f"{filename}.docx"
    )

    doc.save(docx_path)

    # Set browser zoom to 25%
    driver.execute_script("document.body.style.zoom = '25%'")

    # Wait for rendering

    time.sleep(2)

    # 3. Save rendered webpage as PNG
    driver.save_screenshot(
        os.path.join(output_folder, f"{filename}.png")
    )

    print("Files saved successfully:")
    print(txt_path)
    print(docx_path)
    print(os.path.join(output_folder, f"{filename}.png"))


