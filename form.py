
import tkinter as tk
import requests
import re
import analyze as an

def dispMsg(msg):
    text_area.insert(tk.END, f"{msg}\n")
def do_convert():
    folder_id = entry_folder_id.get().strip(); app_id = entry_app_id.get().strip(); sheet_id = entry_sheet_id.get().strip()
    sub_folders = entry_sub_folders.get().strip(); tab_name = entry_tab_name.get().strip() 
    url = f'https://script.google.com/macros/s/{app_id}/exec'
    data = {'folderId': folder_id, 'command': 'convert', 'subFolders': sub_folders}
    while True:
        dispMsg('posted!!')
        try:
            response = requests.post(url, json=data, timeout=330)
        except requests.exceptions.Timeout:
            root.after(10000, do_convert)
            return
        if response.ok:
            if response.text != 'yet': break
        else: dispMsg("❌ Error:", response.status_code); break
    data = {'folderId': folder_id, 'command': 'down', 'subNames': sub_folders }
    dispMsg(f'down {sub_folders}')
    response = requests.post(url, json=data)
    if response.ok:
        hh=response.headers.get('Content-Type')
        if  'application/json' in hh:
            data = response.json()
            if data['success']:
                all_text=data['allText']; lines = all_text.split('\n'); dic = {}; path = ''
                # with open(f"allText.txt", 'w', encoding='utf-8') as f:
                #     f.write(all_text)
                for line in lines:
                    line=line.strip()
                    if line=='': continue
                    match=re.match(r'(.+/.+/.+\.pdf)===(https://.+)', line); 
                    if match: path=match.group(1); dic[path]= { 'url': match.group(2), 'text': ''}
                    else: dic[path]['text'] += line + '\n'
                an.common( dic, sheet_id, tab_name, app_id, text_area)
        
def submit():
    val1 = entry_folder_id.get().strip() #folderId
    val2 = entry_app_id.get().strip() #appId
    val3 = entry_sheet_id.get().strip() #sheetId 
    do_convert()        
    
root = tk.Tk()
root.title("Google Drive Sync Tool")
root.geometry("700x350")
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
submit_button = tk.Button(root, text="Submit", width=20, command=submit)
submit_button.grid(row=3, column=0, columnspan=4, pady=15)

text_area = tk.Text(root, height=10, width=40)
scrollbar = tk.Scrollbar(root, command=text_area.yview)
text_area.config(yscrollcommand=scrollbar.set)

# Grid placement
text_area.grid(row=4, column=0, columnspan=4, sticky="nsew")  # Fill all space
scrollbar.grid(row=4, column=4, sticky="ns")
# Make the grid cell expand
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# entry_folder_id.insert(0, '1jlXkIMCa-rmWJZG0lwbAlKbixw-DI7y3')  
entry_folder_id.insert(0, '1T6p8TBxikn8LIYrilCTxaplqwF9nfVGB')  
# entry_app_id.insert(0, 'AKfycbwpLQSggVwrUtWd1Ygs26MMM2iF7Gpmn8HuNID_EIzBG2ObZs976Byq_VkRmibuhdHu')  
entry_app_id.insert(0, 'AKfycbwM5zKfSCh7Rx4S3uu7fGxE98xT8K8zWUgIQMszA0M6AH9xiMxMMKu9ExPFiA98YD70mQ')  
# entry_sheet_id.insert(0, '1dhN88VZ8FMK2zueiKsY2Irr20xRrgG87--ojr-gy2ug')  
entry_sheet_id.insert(0, '1CVAAilMvM8LsrZIelRz6nf4SRvFeoawGonw6L4QlSC8')  
entry_sub_folders.insert(0, '250612')  
entry_tab_name.insert(0, '2506')  

root.mainloop()

