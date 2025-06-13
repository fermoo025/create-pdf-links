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
  function getDisp(v,ib=0){
    let nn=v, ret='';
    while(v>999){ let rem=v % 1000; v/=1000; v=Math.floor(v); ret=''+rem+','+ret;    }
    ret=''+v+','+ret;
    let len=ret.length; ret=ret.substring(0,len-1)
    if(ib && nn>=10000){ ret=ret.substring(0,len-1-5)+'億'+ret.substring(len-1-5);    }
    return ret;
  }
  function getFileFromPrice(pr){
    const fs=[];
    for(let di in dic){ if( dic[di]['price']==pr) fs.push(di);    }
    if( fs.length==0){
      for (let fn in invalidFiles){
        let pat=getDisp(pr);
        let pattern = `\\b${pat}(万|\\b)`, text;
        text=dic[fn].text?dic[fn].text:'';
        let regex = new RegExp(pattern), match=text.match(pattern);
        if (match) fs.push(fn);
        else{
          pat=getDisp(pr, 1); pattern = `\\b${pat}(万|\\b)`; regex = new RegExp(pattern); match=text.match(pattern);
          if(match){ fs.push(fn);}
        }
      }
    }
    return fs;
  }
  function getFileFromAddr(addr){
    const fs=[];
    for(let di in dic){
      let pattern = `\\b${addr}\\b`;
      let regex = new RegExp(pattern), match=dic[fn].text.match(pattern);
      if (match) fs.push(fn);
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
  let fn='';
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
  data.shift();
  data.forEach((dat)=>{
    let price=parseInt(dat[8].trim().replace(/,/g,'')), fn='', addr=dat[5].trim();
    let fs=getFileFromPrice(price);
    if(fs.length==1)fn=fs[0];
    else if( fs.length>1){ fn='MULTI_PRICE';
    }else{
      fs=getFileFromAddr(addr);
      if(fs.length==1){fn=fs[0]+'ADDR_MATCH';
      }else if(fs.length>1) fn='MULTI_ADDR';
      else fn='NOT_FOUND';
    }
    console.log(price, addr, fn);
  });
}
