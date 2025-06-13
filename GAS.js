function matchPdfUsingINumericPrice() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const folder = DriveApp.getFolderById('1jwQ03EQ0O7Ofl8geDH21v1HXom8NNiH7');
  const files = folder.getFiles();
  const data = sheet.getDataRange().getValues();

  function toHalfWidth(str) {
    return str.replace(/[０-９]/g, s => String.fromCharCode(s.charCodeAt(0) - 65248));
  }
  const dic={}, invalidFiles=[];
  let allText='';
  while (files.hasNext()) {
    const fil = files.next(); 
    const fn=fil.getName();
    const blob = fil.getBlob();
    const resource = {
      title: blob.getName(),
      mimeType: MimeType.GOOGLE_DOCS
    };
    const file = Drive.Files.insert(resource, blob, { ocr: false });
    const doc = DocumentApp.openById(file.id);
    const textRaw = doc.getBody().getText();
    DriveApp.getFileById(file.id).setTrashed(true);
    const text = toHalfWidth(textRaw).trim(); //console.log(text);
    allText+=fn+'=================\n'+text+'\n';
    if(text=='')continue;
    dic[fn]={ text:text, price:''};
    const manMatch = text.match(/価\s*格[：:\s]*([\d,億]+)\s*万\s*円/m);
    let priceValue=0;
    if (manMatch) {
      priceValue = parseInt(manMatch[1].replace(/[,億]/g, ''), 10);
    } else {
      const yenMatch = text.match(/価\s*格[：:\s]*([\d,]+)\s*[円¥]/);
      if (yenMatch) {
        priceValue = Math.round(parseInt(yenMatch[1].replace(/,/g, ''), 10) / 10000);
      }
    }
    if (priceValue > 0) dic[fn]['price'] = priceValue; else invalidFiles.push(fn);
    //break;
  }
  DriveApp.createFile('allPdfTxt', allText, MimeType.PLAIN_TEXT);

}
function matchPdfUsingINumericPrice2() {
  function getFileFromPrice(pr){
    const fs=[];
    for(let di in dic){ if( dic[di]['price']==pr) fs.push(di);    }
    if( len(fs)==0){
      for (let fn in invalidFiles)
            match=re.search(rf'\b{pr}(万|\b)', dic[fn]['text'])
            if match:
                fs.append(fn)
    }
    return fs;
  }
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const data = sheet.getDataRange().getValues();
  const dic={}, invalidFiles=[];
  const allFiles=DriveApp.getFilesByName('allPdfTxt');
  const allFile = allFiles.next();
  const allText=allFile.getBlob().getDataAsString();
  const lines=allText.split('\n');
  dic={}; let fn='';
  lines.forEach((line)=>{
    line=line.trim(); if(line=='')return;
    if(line.endsWith('=================')){ fn=line.replace('=================',''); dic[fn]={text:'',price:0};
    }else{ dic[fn].text+=line+'\n'; }
  });
  for(let fn in dic){
    let text=dic[fn].text;
    const manMatch = text.match(/価\s*格[：:\s]*([\d,億]+)\s*万\s*円/m);
    let priceValue=0;
    if (manMatch) {
      priceValue = parseInt(manMatch[1].replace(/[,億]/g, ''), 10);
    } else {
      const yenMatch = text.match(/価\s*格[：:\s]*([\d,]+)\s*[円¥]/);
      if (yenMatch) {
        priceValue = Math.round(parseInt(yenMatch[1].replace(/,/g, ''), 10) / 10000);
      }
    }
    if (priceValue > 0) dic[fn]['price'] = priceValue; else invalidFiles.push(fn);
  }
}
