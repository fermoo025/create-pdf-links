from pdf2image import convert_from_path
import pytesseract

pages = convert_from_path("100129115598 (3).pdf")
for i, page in enumerate(pages):
    text = pytesseract.image_to_string(page)
    print(f"Page {i + 1}:\n{text}")
