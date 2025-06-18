import tkinter as tk
from tkinter import messagebox
import downPdfs  # Make sure this file is in the same folder
import os
import readPdfs
import credsa
import requests
from googleapiclient.discovery import build
import io
from googleapiclient.http import MediaIoBaseDownload
import re
import sqlite3

def do_convert():
    val1 = entry_folder_id.get().strip(); val2 = entry_app_id.get().strip(); val4 = entry_sub_folders.get().strip() 
    url = f'https://script.google.com/macros/s/{val2}/exec'
    data = {'folderId': val1, 'command': 'convert'}
    while True:
        print('posted!!')
        response = requests.post(url, json=data)
        if response.ok:
            if response.text != 'yet': break
        else: print("❌ Error:", response.status_code); break
    data = {'folderId': val1, 'command': 'down', 'subNames': val4 }
    print(f'down {val4}')
    response = requests.post(url, json=data)
    if response.ok:
        hh=response.headers.get('Content-Type')
        if  'application/json' in hh:
            data = response.json()
            if data['success']:
                all_text=data['allText']; lines = all_text.split('\n'); dic = {}; path = ''
                cursor = conn.cursor()
                for line in lines:
                    line=line.strip()
                    if line=='': continue
                    match=re.match(r'(.+/.+/.+\.pdf)===(https://.+)', line); 
                    if match: path=match.group(1); dic[path]= { 'url': match.group(2), 'text': ''}
                    else: dic[path]['text'] += line + '\n'
                
                for path in dic:
                    cursor.execute("INSERT INTO pdf (path, text, url) VALUES (?, ?, ?)", (path, dic[path]['text'],dic[path]['url']))
                    conn.commit()
                conn.close()
                print('inserted')

def delete_txt(folder_id, fn):
    creds = credsa.authenticate()
    service = build('drive', 'v3', credentials=creds)
    query = f"'{folder_id}' in parents and name = '{fn}.txt' and trashed = false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    if not files: return
    for file in files:
        service.files().delete(fileId=file['id']).execute()
        
def submit():
    val1 = entry_folder_id.get().strip() #folderId
    val2 = entry_app_id.get().strip() #appId
    val3 = entry_sheet_id.get().strip() #sheetId 
    do_convert()        
    
root = tk.Tk()
root.title("Google Drive Sync Tool")
root.geometry("700x300")
root.resizable(True, True)

# ---- Top row: APP ID ----
tk.Label(root, text="APP ID").grid(row=0, column=0, padx=5, pady=5, sticky='e')
entry_app_id = tk.Entry(root, width=100)
entry_app_id.grid(row=0, column=1, columnspan=3, padx=5, pady=5)

# ---- Second row: FOLDER ID and SUB FOLDERS ----
tk.Label(root, text="FOLDER ID").grid(row=1, column=0, padx=5, pady=5, sticky='e')
entry_folder_id = tk.Entry(root, width=50)
entry_folder_id.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="SUB FOLDERS").grid(row=1, column=2, padx=5, pady=5, sticky='e')
entry_sub_folders = tk.Entry(root)
entry_sub_folders.grid(row=1, column=3, padx=5, pady=5)

# ---- Third row: SHEET ID and TAB NAME ----
tk.Label(root, text="SHEET ID").grid(row=2, column=0, padx=5, pady=5, sticky='e')
entry_sheet_id = tk.Entry(root, width=50)
entry_sheet_id.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="TAB NAME").grid(row=2, column=2, padx=5, pady=5, sticky='e')
entry_tab_name = tk.Entry(root)
entry_tab_name.grid(row=2, column=3, padx=5, pady=5)

# ---- Fourth row: Submit button ----
submit_button = tk.Button(root, text="Submit", width=20)
submit_button.grid(row=3, column=0, columnspan=4, pady=15)
entry_folder_id.insert(0, '1jlXkIMCa-rmWJZG0lwbAlKbixw-DI7y3')  
entry_app_id.insert(0, 'AKfycbwpLQSggVwrUtWd1Ygs26MMM2iF7Gpmn8HuNID_EIzBG2ObZs976Byq_VkRmibuhdHu')  
entry_sheet_id.insert(0, '1aCRXquuVO4TS6YvVadR34FJgvwHiDvFqOSbgqpLJf3k')  
entry_sub_folders.insert(0, '250614,250615')  

conn = sqlite3.connect("ginza.db")
root.mainloop()

