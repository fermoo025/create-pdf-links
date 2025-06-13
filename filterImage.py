fileName='【Hx若宮】販売図面 2025.06.02.pdf'
# PyPDF2 (basic text extraction)
from PyPDF2 import PdfReader
import pdfplumber
from pdfminer.high_level import extract_text
import glob
import sys
import os

def readPdf1(fileName):
    reader = PdfReader(fileName)
    return "".join([page.extract_text() for page in reader.pages])

def readPdf2(fileName):
    with pdfplumber.open(fileName) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages])

def readPdf3(fileName):
    return extract_text(fileName)

os.chdir('pdfs2')
files = glob.glob('*.pdf')  # Change pattern as needed
for file in files:
    text=readPdf3(file).strip()
    file=file[0:-4]
    with open(f"{file}.txt", 'w', encoding='utf-8') as f:
        f.write(text)
    if text!='': 
        continue
    print (file)
    