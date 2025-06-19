let dic = {},
   invalidFiles = [];
//  1TDw4KONPyeH8Rr9EVdjfQ0GYjjnYZ2ag
let FOLDER_ID = '1TDw4KONPyeH8Rr9EVdjfQ0GYjjnYZ2ag',
   patPrefect = /^(北海道|青森県|岩手県|宮城県|秋田県|山形県|福島県|茨城県|栃木県|群馬県|埼玉県|千葉県|東京都|神奈川県|新潟県|富山県|石川県|福井県|山梨県|長野県|岐阜県|静岡県|愛知県|三重県|滋賀県|京都府|大阪府|兵庫県|奈良県|和歌山県|鳥取県|島根県|岡山県|広島県|山口県|徳島県|香川県|愛媛県|高知県|福岡県|佐賀県|長崎県|熊本県|大分県|宮崎県|鹿児島県|沖縄県)/;


function toHalfWidth(str) {
   str = str.replace(/：/g, ':');
   str = str.replace(/　/g, ' ');
   return str.replace(/[０-９]/g, s => String.fromCharCode(s.charCodeAt(0) - 65248));
}


function getFileUrlByName(folderId, fileName) {
   const folder = DriveApp.getFolderById(folderId);
   const files = folder.getFilesByName(fileName);
   if (files.hasNext()) {
       const file = files.next();
       const url = file.getUrl(); //    Logger.log("File URL: " + url);
       return url;
   } else {
       Logger.log("File not found.");
       return null;
   }
}


function convertNFC(txt) {
   const radicalToStandard = {
       '⼀': '一', '⼁': '丨', '⼂': '丶', '⼃': '丿', '⼄': '乙', '⼅': '亅', '⼆': '二', '⼇': '亠', '⼈': '人', '⼉': '儿', 
       '⼊': '入', '⼋': '八', '⼌': '冂', '⼍': '冖', '⼎': '冫', '⼏': '几', '⼐': '凵', '⼑': '刀', '⼒': '力', '⼓': '勹', 
       '⼔': '匕', '⼕': '匚', '⼖': '匸', '⼗': '十', '⼘': '卜', '⼙': '卩', '⼚': '厂', '⼛': '厶', '⼜': '又', '⼝': '口', 
       '⼞': '囗', '⼟': '土', '⼠': '士', '⼡': '夂', '⼢': '夊', '⼣': '夕', '⼤': '大', '⼥': '女', '⼦': '子', '⼧': '宀', 
       '⼨': '寸', '⼩': '小', '⼪': '尢', '⼫': '尸', '⼬': '屮', '⼭': '山', '⼮': '巛', '⼯': '工', '⼰': '己', '⼱': '巾', 
       '⼲': '干', '⼳': '幺', '⼴': '广', '⼵': '廴', '⼶': '廾', '⼷': '弋', '⼸': '弓', '⼹': '彐', '⼺': '彡', '⼻': '彳', 
       '⼼': '心', '⼽': '戈', '⼾': '戶', '⼿': '手', '⽀': '支', '⽁': '攴', '⽂': '文', '⽃': '斗', '⽄': '斤', '⽅': '方', 
       '⽆': '无', '⽇': '日', '⽈': '曰', '⽉': '月', '⽊': '木', '⽋': '欠', '⽌': '止', '⽍': '歹', '⽎': '殳', '⽏': '毋', 
       '⽐': '比', '⽑': '毛', '⽒': '氏', '⽓': '气', '⽔': '水', '⽕': '火', '⽖': '爪', '⽗': '父', '⽘': '爻', '⽙': '爿', 
       '⽚': '片', '⽛': '牙', '⽜': '牛', '⽝': '犬', '⽞': '玄', '⽟': '玉', '⽠': '瓜', '⽡': '瓦', '⽢': '甘', '⽣': '生', 
       '⽤': '用', '⽥': '田', '⽦': '疋', '⽧': '疒', '⽨': '癶', '⽩': '白', '⽪': '皮', '⽫': '皿', '⽬': '目', '⽱': '矛', 
       '⽲': '矢', '⽳': '石', '⽴': '立', '⽵': '竹', '⽶': '米', '⽷': '糸', '⽸': '缶', '⽹': '网', '⽺': '羊', '⽻': '羽', 
       '⽼': '老', '⽽': '而', '⽾': '耒', '⽿': '耳', '⾀': '聿', '⾁': '肉', '⾂': '臣', '⾃': '自', '⾄': '至', '⾅': '臼', 
       '⾆': '舌', '⾇': '舛', '⾈': '舟', '⾉': '艮', '⾊': '色', '⾋': '艸', '⾌': '虍', '⾍': '虫', '⾎': '血', '⾏': '行', 
       '⾐': '衣', '⾑': '襾', '⾒': '見', '⾓': '角', '⾔': '言', '⾕': '谷', '⾗': '豆', '⾘': '豕', '⾙': '貝', '⾚': '赤', 
       '⾛': '走', '⾜': '足', '⾝': '身', '⾞': '車', '⾟': '辛', '⾠': '辰', '⾡': '辵', '⾢': '邑', '⾣': '酉', '⾤': '釆', 
       '⾥': '里', '⾦': '金', '⾧': '長', '⾨': '門', '⾩': '阜', '⾪': '隶', '⾫': '隹', '⾬': '雨', '⾭': '青', '⾮': '非', 
       '⾯': '面', '⾰': '革', '⾱': '韋', '⾲': '韭', '⾳': '音', '⾴': '頁', '⾵': '風', '⾶': '飛', '⾷': '食', '⾸': '首', 
       '⾹': '香', '⾺': '馬', '⾻': '骨', '⾼': '高', '⾿': '髟', '⿀': '鬥', '⿁': '鬯', '⿂': '鬲', '⿃': '鬼', '⿄': '魚', 
       '⿅': '鳥', '⿆': '鹵', '⿇': '鹿', '⿈': '麥', '⿉': '麻', '⿊': '黃', '⿋': '黍', '⿌': '黑', '⿍': '黹', '⿎': '黽', 
       '⿏': '鼎', '⿐': '鼓', '⿑': '鼠', '⿒': '鼻', '⿓': '齊', '⿔': '齒', '⿕': '龍', '（': '(', '）': ')', };
   for (let ch in radicalToStandard) {
       let reg = new RegExp(ch, 'g');
       txt = txt.replace(reg, radicalToStandard[ch]);
   }
   return txt;
}


function getDisp(v, ib = 0) {
   let nn = v,
       ret = '';
   while (v > 999) {
       let rem = v % 1000;
       v /= 1000;
       v = Math.floor(v);
       ret = '' + rem + ',' + ret;
   }
   ret = '' + v + ',' + ret;
   let len = ret.length;
   ret = ret.substring(0, len - 1)
   if (ib && nn >= 10000) {
       ret = ret.substring(0, len - 1 - 5) + '億' + ret.substring(len - 1 - 5);
   }
   return ret;
}


function getFileFromAddr(addr) {
   const fs = [];
   addr = toHalfWidth(addr);
   addr = addr.replace(/丁目/, '');
   let addr2 = addr.replace(patPrefect, ''),
       addr3 = addr2;
   const digits = '一二三四五六七八九';
   if (addr2.length > 5) {
       let ch = addr2.substring(addr2.length - 1);
       if (ch.match(/[1-9]/)) addr3 = addr2.substring(0, addr2.length - 1) + digits[parseInt(ch) - 1];
   }
   for (let di in dic) {
       let b = 1;
       if (di.indexOf('レインズ資料 4180万円.pdf') == 0)
           b++;
       let pattern = `${addr}`;
       let regex = new RegExp(pattern),
           match = dic[di].text.match(pattern);
       if (match) fs.push(di);
       else {
           pattern = `${addr2}`;
           regex = new RegExp(pattern), match = dic[di].text.match(pattern);
           if (match) fs.push(di);
           else {
               pattern = `${addr3}`;
               regex = new RegExp(pattern), match = dic[di].text.match(pattern);
               if (match) fs.push(di);
           }
       }
   }
   return fs;
}


function getFileFromPrice(pr) {
   const fs = [];
   for (let di in dic) {
       if (dic[di]['price'] == pr) fs.push(di);
   }
   if (fs.length == 0) {
       invalidFiles.forEach((fn) => {
           let pat = getDisp(pr);
           let pattern = `[^,\\d]${pat}\\s*(万)`,
               text;
           text = dic[fn].text ? dic[fn].text : '';
           let regex = new RegExp(pattern, 'm'),
               match = text.match(pattern);
           if (match) fs.push(fn);
           else {
               pat = pat.replace(',', '');
               pattern = `[^,\\d]${pat}\\s*(万)`;
               regex = new RegExp(pattern, 'm');
               match = text.match(pattern);
               if (match) {
                   fs.push(fn);
               } else {
                   pat = getDisp(pr, 1);
                   pattern = `[^億,\\d]${pat}\\s*(万)`;
                   regex = new RegExp(pattern, 'm');
                   match = text.match(pattern);
                   if (match) {
                       fs.push(fn);
                   } else {
                       pr *= 10000;
                       pat = getDisp(pr);
                       pattern = `[^,\\d]${pat}\\s*(円)`;
                       regex = new RegExp(pattern, 'm');
                       match = text.match(pattern);
                       if (match) {
                           fs.push(fn);
                       }
                   }
               }
           }
       });
   }
   return fs;
}
function getPdfText(fil){
  const blob = fil.getBlob();
  const resource = { title: blob.getName(), mimeType: MimeType.GOOGLE_DOCS };
  const file = Drive.Files.insert(resource, blob, { ocr: false });
  const doc = DocumentApp.openById(file.id), textRaw = doc.getBody().getText();
  DriveApp.getFileById(file.id).setTrashed(true);
  return convertNFC(toHalfWidth(textRaw)).trim();
}
function updateStatus(content) {
  const folderId = FOLDER_ID, folder = DriveApp.getFolderById(folderId);
  const files=folder.getFilesByType(MimeType.PLAIN_TEXT)
  while (files.hasNext()) { let file = files.next(); file.setTrashed(true); } 
  folder.createFile( content + '.txt', '');
}
function convertPdfs(folderId, subFolders){
  FOLDER_ID = folderId;
  const pFolder = DriveApp.getFolderById(FOLDER_ID); 
  const tic=Date.now(); let subs= subFolders.split(',');
  subs.forEach((sub,i,ar)=>{ ar[i]=sub.trim(); });
  var folders = pFolder.getFolders();
  while (folders.hasNext()) {
    const folder = folders.next(), fName= folder.getName();
    if( subs.indexOf( fName) ==-1) continue;
    const dic = {}, txtFns=[]; let files = folder.getFiles();
    while (files.hasNext()) { 
      const file=files.next(); let fn=file.getName();
      let ext=fn.substring(fn.length -3); fn=fn.substring(0, fn.length - 4 );      
      if( ext == 'txt')  dic[fn] = 1;  else if(dic[fn]==undefined) dic[fn] = 0; 
    }
    for( let fn in dic){
      if( dic[fn] == 0){
        const files=folder.getFilesByName(fn+'.pdf');
        const file = files.next(), text= getPdfText(file);
        folder.createFile(fn + '.txt', text);
        if( Date.now() - tic > 300000 ) { // updateStatus('yet'); 
          return 'yet';  }// timeout;
      }
    }  
  }
  return 'done'; //updateStatus('done'); 
  console.log('done');
}
function downTexts(folderId, subNames){
  FOLDER_ID = folderId;
  const pFolder = DriveApp.getFolderById(FOLDER_ID), pName= pFolder.getName();
  var folders = pFolder.getFolders(); let allText = '';
  while (folders.hasNext()) {
    const folder=folders.next(), fName=folder.getName();
    if ( subNames.indexOf(fName)==-1 ) continue;
    const files = folder.getFiles();
    while( files.hasNext()){
      const file = files.next(); let fn= file.getName(), pdfName= fn.substring(0, fn.length - 3)+'pdf'; 
      if(!fn.endsWith('.txt')) continue;
      const pdfs= folder.getFilesByName(pdfName); 
      const pdfFile=pdfs.next(), url = pdfFile.getUrl(); 
      allText += `${pName}/${fName}/${pdfName}===${url}\n`;
      allText += file.getBlob().getDataAsString()+"\n"; 
    }
  }
  return allText;
}
function doGet(e) {
  const html = `
    <html>
      <head><title>Sample</title></head>
      <body>
        <h1>Hello from GAS</h1>
        <p>This is a long HTML message.</p>
        <!-- You can insert more HTML here -->
      </body>
    </html>
  `;
  return ContentService.createTextOutput(html)
    .setMimeType(ContentService.MimeType.HTML);
}
function doPost(e) {
  var data = JSON.parse(e.postData.contents);
  if(data.command == 'convert'){ const ret = convertPdfs(data.folderId, data.subFolders);  
    return ContentService.createTextOutput(ret);
  }  else if(data.command == 'down'){
    let subs=data.subNames.trim().split(',');
    subs.forEach((sub,i,ar)=>{ ar[i]=sub.trim(); });
    const allText = downTexts(data.folderId, subs ); 
    const responseData = { success: true,allText: allText } // Raw POST content
    return ContentService .createTextOutput(JSON.stringify(responseData)) .setMimeType(ContentService.MimeType.JSON);
  }else if ( data.command == 'getCsv')  {
    const sheetId=data.sheetId, sheetName=data.sheetName; 
    var spreadsheet = SpreadsheetApp.openById(sheetId), rows = [];
    var sheet = spreadsheet.getSheetByName(sheetName);
    var data = sheet.getDataRange().getValues(); data.shift();
    for (var i = 0; i < data.length; i++) {
       rows.push([ i, data[i][2], data[i][5], data[i][7] ]); // 2,6,8?
       }
    const responseData = { success: true,data: rows } // Raw POST content
    return ContentService .createTextOutput(JSON.stringify(responseData)) .setMimeType(ContentService.MimeType.JSON);
  }else if( data.command == 'setCsv'){
    const sheetId=data.sheetId, sheetName=data.sheetName; 
    var spreadsheet = SpreadsheetApp.openById(sheetId);
    var sheet = spreadsheet.getSheetByName(sheetName);
    let rows= data.rows;
    rows.forEach(row=>{ let ind=row[0]; sheet.getRange(ind+2, 3).setValue(row[1]);  });
    const responseData = { success: true,data: rows.length } // Raw POST content
    return ContentService .createTextOutput(JSON.stringify(responseData)) .setMimeType(ContentService.MimeType.JSON);
  }
}
function matchPdfUsingINumericPrice() {


   const folder = DriveApp.getFolderById(FOLDER_ID);
   const files = folder.getFiles();
   dic = {};invalidFiles = [];
   //let allText='';
   while (files.hasNext()) {
       const fil = files.next(),
           fn = fil.getName(),
           blob = fil.getBlob();
       const resource = {
           title: blob.getName(),
           mimeType: MimeType.GOOGLE_DOCS
       };
       const file = Drive.Files.insert(resource, blob, {
           ocr: false
       });
       const doc = DocumentApp.openById(file.id),
           textRaw = doc.getBody().getText();
       DriveApp.getFileById(file.id).setTrashed(true);
       const text = convertNFC(toHalfWidth(textRaw)).trim(); //console.log(text);
       //allText+=fn+'=================\n'+text+'\n';
       if (text == '') continue;
       dic[fn] = {
           text: text,
           price: 0
       };
   }
   common();
}


function common() {
   const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
   const data = sheet.getDataRange().getValues();
   for (const fn in dic) {
       const text=dic[fn].text;
       const manMatch = text.match(/価\s*格(?:[:\s]|\(\s*税\s*込\s*\))*([\d,億]+)\s*万/m);
       let priceValue = 0;
       if (manMatch) {
           priceValue = parseInt(manMatch[1].replace(/[,億]/g, ''), 10);
       } else {
           const yenMatch = text.match(/価\s*格(?:[:\s]|\(\s*税\s*込\s*\))*([\d,]+)\s*[円¥]/m);
           if (yenMatch) {
               priceValue = Math.round(parseInt(yenMatch[1].replace(/,/g, ''), 10) / 10000);
           }
       }
       if (priceValue > 0) dic[fn]['price'] = priceValue;
       else invalidFiles.push(fn);
   }
   //DriveApp.createFile('allPdfTxt', allText, MimeType.PLAIN_TEXT);
   data.shift();
   data.forEach((dat, index) => {
       let price = parseInt(toHalfWidth(dat[9]).trim().replace(/,/g, '')),
           fn = '',
           addr = dat[6].trim();
       let fs = getFileFromPrice(price);
       let isPriceMatch = 0,
           fa = [];
       if (fs.length == 1) {
           let a = 1;
           if (price == 4180)
               a++;
           fa = getFileFromAddr(addr);
           if (fa.length == 1) {
               fn = fa[0];
               isPriceMatch = 1;
           } else if (fa.length > 1) {
               fn = 'MULTI_PRICE_ADDR';
               isPriceMatch = 1;
           } //else fn = fa[0];
       }
       if (isPriceMatch == 0) {
           if (fs.length > 1) {
               fn = 'MULTI_PRICE';
           } else if (fs.length == 0) {
               fs = getFileFromAddr(addr);
               if (fs.length == 1) {
                   fn = 'ADDR_MATCH' + fs[0];
               } else if (fs.length > 1)
                   fn = 'MULTI_ADDR';
               else
                   fn = 'NOT_FOUND';
           } else { // fs.length=1 & fa.length=0
               fn = 'PRICE_FOUND_BUT_ADDR_MISMATCH';
           }
       }
       if (fn.endsWith('.pdf')) {
           let rn = fn;
           if (rn.indexOf('ADDR_MATCH') === 0) rn = rn.substring(10);
           let url = getFileUrlByName(FOLDER_ID, rn);
           sheet.getRange(index + 2, 3).setValue(url);


       }
       console.log(price + '\t' + addr + '\t' + fn);
   });
}
