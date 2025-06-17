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

def getStatus():
    creds = credsa.authenticate(); service = build('drive', 'v3', credentials=creds)
    val1 = entry1.get().strip(); query = f"'{val1}' in parents and trashed = false"
    results = service.files().list( q=query, fields="files(id, name)", pageSize=1 ).execute()
    files = results.get('files', [])
    if files: file = files[0]; return file['name'][0: -4]
    else: return 'not'

def list_folders_in_folder(parent_folder_id):
    creds = credsa.authenticate(); service = build('drive', 'v3', credentials=creds)
    query = f"'{parent_folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"    
    response = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    folders = response.get('files', []); ret=[]
    if not folders: return []
    else:
        for folder in folders:
            ret.append({'name': folder['name'], 'id': folder['id']})
    return ret

def do_convert():
    status=getStatus(); val1 = entry1.get().strip(); val2 = entry2.get().strip()       
    val4 = entry4.get().strip() 
    url = f'https://script.google.com/macros/s/{val2}/exec'
    if status == 'run': 
        print('running')
        root.after(10000, do_convert)
    elif status != 'done': 
        data = {'folderId': val1, 'command': 'convert'}
        print('posted!!')
        response = requests.post(url, json=data)
        if response.ok:
            print(response.text[0:200]); root.after(10000, do_convert)
        else: print("❌ Error:", response.status_code)
    else:
        data = {'folderId': val1, 'command': 'down', 'subNames': val4 }
        print(f'down {val4}')
        response = requests.post(url, json=data)
        if response.ok:
            all_text=response.text
            print(all_text)

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
    val1 = entry1.get().strip() #folderId
    val2 = entry2.get().strip() #appId
    val3 = entry3.get().strip() #sheetId   
    status=getStatus()
    if status== 'run':
        messagebox.showinfo("Info", f"""<run> exists in {val1}: this is due to running process or 
        remained file. If you've been not running, please erase it.""")
        return
    elif status == 'done': delete_txt('done') 
    do_convert()        
    
root = tk.Tk()
root.title("Wider Form")
root.geometry("600x340") 
label1 = tk.Label(root, text="FOLDER ID:", anchor='w')
label1.pack(fill='x', padx=20, pady=(20, 5))
entry1 = tk.Entry(root, width=60)
entry1.pack(padx=20, pady=5)
label2 = tk.Label(root, text="APP ID:", anchor='w')
label2.pack(fill='x', padx=20, pady=5)
entry2 = tk.Entry(root, width=90)
entry2.pack(padx=20, pady=5)
label3 = tk.Label(root, text="SHEET ID:", anchor='w')
label3.pack(fill='x', padx=20, pady=5)
entry3 = tk.Entry(root, width=60)
entry3.pack(padx=20, pady=5)
label4 = tk.Label(root, text="SubFolders:", anchor='w')
label4.pack(fill='x', padx=20, pady=5)
entry4 = tk.Entry(root, width=60)
entry4.pack(padx=20, pady=5)
submit_button = tk.Button(root, text="Submit", width=20, height=3, command=submit)
submit_button.pack(pady=20)
entry1.insert(0, '1jlXkIMCa-rmWJZG0lwbAlKbixw-DI7y3')  
entry2.insert(0, 'AKfycbwpLQSggVwrUtWd1Ygs26MMM2iF7Gpmn8HuNID_EIzBG2ObZs976Byq_VkRmibuhdHu')  
entry3.insert(0, '1aCRXquuVO4TS6YvVadR34FJgvwHiDvFqOSbgqpLJf3k')  
entry4.insert(0, '250614,250615')  
root.mainloop()
