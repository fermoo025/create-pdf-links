from PyPDF2 import PdfReader
import pdfplumber
from pdfminer.high_level import extract_text
import glob
import sys
import re
import os
import csv

rows=[]
with open('data.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        rows.append(row)
os.chdir('pdfs')
files = glob.glob('*.pdf')  # Change pattern as needed
dic={}
invalidFiles=[]
sys.stderr = open(os.devnull, 'w')

def readPdf1(fileName):
    reader = PdfReader(fileName)
    return "".join([page.extract_text() for page in reader.pages])

def readPdf2(fileName):
    with pdfplumber.open(fileName) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages])

def readPdf3(fileName):
    return extract_text(fileName)

def getFileFromPrice(pr):
    fs=[]
    for di in dic:
        if dic[di]['price']==pr:
                fs.append(di)
    if len(fs)==0:
        for fn in invalidFiles:
            match=re.search(rf'\b{pr}(万|\b)', dic[fn]['text'])
            if match:
                fs.append(fn)
    return fs;

for file in files:
    text=readPdf3(file).strip()
    if text=='': 
        continue
    dic[file]={ 'text':text, 'price':''}
    match = re.search(r'価\s*格([\s\d\,億]+)万\s*円', text)  # regex pattern    
    if match:
        price=match.group(1).strip()  # Output: xx123
        price=price.replace('億','')
        dic[file]['price'] = price
    else:
        invalidFiles.append(file)
    
print()
for row in rows:
    price= row[6][0:-2]
    address=row[4]
    fs=getFileFromPrice(price)
    if len(fs)>0:
        print(f"{row[0]}{fs}")
