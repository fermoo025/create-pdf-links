import re
import readPdfs as rp
import requests
import json
import copy
import tkinter as tk

patPrefect = r"^(北海道|青森県|岩手県|宮城県|秋田県|山形県|福島県|茨城県|栃木県|群馬県|埼玉県|千葉県|東京都|神奈川県|新潟県|富山県|石川県|福井県|山梨県|長野県|岐阜県|静岡県|愛知県|三重県|滋賀県|京都府|大阪府|兵庫県|奈良県|和歌山県|鳥取県|島根県|岡山県|広島県|山口県|徳島県|香川県|愛媛県|高知県|福岡県|佐賀県|長崎県|熊本県|大分県|宮崎県|鹿児島県|沖縄県)"
dic = {}
invalidFiles = []

def toHalfWidth(str):
    str = str.replace('：', ':')
    str = str.replace('　', ' ')
    return re.sub(r'[０-９]', lambda m: chr(ord(m.group(0)) - 0xFEE0), str)

def getDisp(v, ib=0):
    nn = v
    ret = ""
    while v > 999:
        rem = v % 1000
        v /= 1000
        v = int(v)
        ret = "" + str(rem) + "," + ret
    ret = "" + str(v) + "," + ret
    ret = ret[0:-1]
    if ib and nn >= 10000:
        ret = ret[0:-6] + "億" + ret[-6:]
    return ret


def getFileFromAddr(addr):
    
    fs = []
    addr = toHalfWidth(addr)
    addr = addr.replace("丁目", "")
    addr2 = re.sub(patPrefect, "", addr)
    addr3 = addr2
    digits = "一二三四五六七八九"
    if len(addr2) > 4:
        ch = addr2[-1]
        if re.match(r"[1-9]", ch):
            addr3 = addr2[0:-1] + digits[int(ch) - 1]
    for di in dic:
        b = 1
        if di.startswith("レインズ資料 4180万円.pdf"):
            b += 1
        match = re.search(addr, dic[di]['text'])
        if match:
            fs.append(di)
        else:
            match = re.search(addr2, dic[di]['text'])
            if match:
                fs.append(di)
            else:
                match = re.search(addr3, dic[di]['text'])
                if match:
                    fs.append(di)
    return fs


def getFileFromPrice(pr):
    fs = []
    for di in dic:
        if dic[di]["price"] == pr:
            fs.append(di)
    if len(fs) == 0:
        prMan = int(pr / 10000)
        for fn in invalidFiles:
            text = dic[fn]['text'] if dic[fn]['text'] else ""

            pat = getDisp(prMan)
            pattern = f"[^,\\d]${pat}\\s*(万)"
            match = re.search(pattern, text, re.MULTILINE)
            if match:
                fs.append(fn)
            else:
                pat = pat.replace(",", "")
                pattern = f"[^,\\d]${pat}\\s*(万)"
                match = re.search(pattern, text, re.MULTILINE)
                if match:
                    fs.append(fn)
                else:
                    pat = getDisp(prMan, 1)
                    pattern = f"[^億,\\d]${pat}\\s*(万)"
                    match = re.search(pattern, text, re.MULTILINE)
                    if match:
                        fs.append(fn)
                    else:
                        pat = getDisp(pr)
                        pattern = f"[^,\\d]${pat}\\s*(円)"
                        match = re.search(pattern, text, re.MULTILINE)
                        if match:
                            fs.append(fn)
    return fs

def dispMsg(msg, tka):
    tka.insert(tk.END, f"{msg}\n")
    
def common(dictn, sheetId, sheetName, appId, tka):
    global dic, invalidFiles
    data = {'sheetId': sheetId, 'command': 'getCsv', 'sheetName': sheetName }
    dispMsg(f'down sheet', tka)
    url = f'https://script.google.com/macros/s/{appId}/exec'
    if appId:
        response = requests.post(url, json=data)
        if response.ok:
            hh=response.headers.get('Content-Type')
            if  'application/json' in hh:
                dat = response.json()
                if dat['success']:
                    data=dat['data']; 
                    # with open('data.json', 'w') as f:
                    #     json.dump({'dic':dic, 'data': data}, f)
    else:
        with open("data.json", "r") as f:
            bd = json.load(f); dictn = bd['dic']; data= bd['data']
    invalidFiles = []; dic = copy.deepcopy(dictn)
    for row in dic:
        fn=row
        text = dic[row]["text"]
        manMatch = re.search(
            r"価\s*格(?:[:\s]|\(\s*税\s*込\s*\))*([\d,億]+)\s*万", text, re.MULTILINE
        )
        priceValue = 0
        if manMatch:
            priceValue = (
                int(manMatch.group(1).replace(",", "").replace(r"億", "")) * 10000
            )
        else:
            yenMatch = re.search(
                r"価\s*格(?:[:\s]|\(\s*税\s*込\s*\))*([\d,]+)\s*[円¥]",
                text,
                re.MULTILINE,
            )
            if yenMatch:
                priceValue = int(yenMatch.group(1).replace(",", ""))
        dic[row]["price"] = priceValue
        if priceValue == 0: invalidFiles.append(fn)
    index = 0; result=[]
    for dat in data:
        if dat[1].strip()!='' or dat[2].strip()=='': 
            index +=1; continue;
        txtPrice = toHalfWidth(dat[3]).strip().replace(",", "")
        multi = 1
        if "万円" in txtPrice:
            txtPrice = txtPrice.replace("万円", "")
            multi = 10000
        price = int(float(txtPrice) * multi)
        fn = ""
        addr = dat[2].strip()
        fs = getFileFromPrice(price)
        isPriceMatch = 0
        fa = []
        if len(fs) == 1:
            a = 1
            if price == 64800000:
                a += 1
            fa = getFileFromAddr(addr)
            if len(fa) == 1:
                fn = fa[0]; isPriceMatch = 1; del dic[fn]
                if fn in invalidFiles: invalidFiles.remove(fn)
            elif len(fa) > 1:
                fn = "MULTI_PRICE_ADDR"
                isPriceMatch = 1
            # else: fn= 'PRICE_NO_ADDR' + fs[0]
        if isPriceMatch == 0:
            if len(fs) > 1:
                fn = "MULTI_PRICE"
            elif len(fs) == 0:
                fs = getFileFromAddr(addr)
                if len(fs) == 1:
                    fn = "ADDR_MATCH" + fs[0]; del dic[fs[0]]
                    if fs[0] in invalidFiles: invalidFiles.remove(fs[0])
                elif len(fs) > 1:
                    fn = "MULTI_ADDR"
                else:
                    fn = "NOT_FOUND"
            else: fn = "PRICE_FOUND_BUT_ADDR_MISMATCH"# // fs.length=1 & fa.length=0
        if fn.endswith(".pdf"):
            rn = fn
            if rn.find("ADDR_MATCH") == 0:
                rn = rn[10:]
            # url = getFileUrlByName(FOLDER_ID, rn)
            # sheet.getRange(index + 2, 3).setValue(url)
            result.append([ index, dictn[rn]['url'] ])
        index +=1
        dispMsg(f"{price}\t{addr}\t{fn}", tka)
    data = {'sheetId': sheetId, 'command': 'setCsv', 'sheetName': sheetName, 'rows': result }
    dispMsg(f'uploading sheet', tka)
    url = f'https://script.google.com/macros/s/{appId}/exec'
    if appId:
        response = requests.post(url, json=data)
        if response.ok:
            hh=response.headers.get('Content-Type')
            if  'application/json' in hh:
                dat = response.json()
                if dat['success']:
                    dispMsg(f"{dat['data']} added", tka) 


if __name__ == "__main__":
    common({},'','','')
