from flask import Flask, request, render_template
import requests

app = Flask(__name__)

def do_convert(appId, folderId, subFolders, sheetId, tabName):
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

@app.route('/', methods=['GET'])
def form():
    if request.method == 'POST':
        appId = request.form['app_id']
        folderId = request.form['folder_id']
        subFolders = request.form['sub_folders']
        sheetId = request.form['sheet_id']
        tabName = request.form['tab_name']
        do_convert(appId, folderId, subFolders, sheetId, tabName)
        return render_template('result.html', name=username)
    return render_template('form.html')

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    folderId = data.folderId.strip(); appId = data.appId.strip(); sheetId = data.sheetId.strip()
    subFolders = data.subFolders.get().strip(); tabName = data.tabName.get().strip() 
    url = f'https://script.google.com/macros/s/{appId}/exec'
    data = {'folderId': folderId, 'command': 'convert', 'subFolders': subFolders}
    try:
        response = requests.post(url, json=data, timeout=330)
        return response.content
    except requests.exceptions.Timeout:
        return 'yet'

if __name__ == '__main__':
    app.run(debug=True)
