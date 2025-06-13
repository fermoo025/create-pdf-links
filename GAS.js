function matchPdfUsingINumericPrice() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const folder = DriveApp.getFolderById('1jwQ03EQ0O7Ofl8geDH21v1HXom8NNiH7');
  const files = folder.getFiles();
  const data = sheet.getDataRange().getValues();

  function toHalfWidth(str) {
    return str.replace(/[０-９]/g, s => String.fromCharCode(s.charCodeAt(0) - 65248));
  }

  while (files.hasNext()) {
    const file = files.next();
    const textRaw = file.getBlob().getDataAsString();
    const text = toHalfWidth(textRaw);

    // 金額抽出（万円換算）
    let priceValue = null;
    const manMatch = text.match(/([\d,]+)\s*万円/);
    if (manMatch) {
      priceValue = parseInt(manMatch[1].replace(/,/g, ''), 10);
    } else {
      const yenMatch = text.match(/([\d,]+)\s*[円¥]/);
      if (yenMatch) {
        priceValue = Math.round(parseInt(yenMatch[1].replace(/,/g, ''), 10) / 10000);
      }
    }
    if (!priceValue) continue;

    // 住所抽出（○○市or区から先頭30文字まで）
    const addressMatch = text.match(/[^\n\r]*(市|区)[^\n\r]{0,30}/);
    if (!addressMatch) continue;
    const pdfAddress = addressMatch[0].trim();

    let matched = false;

    for (let i = 1; i < data.length; i++) {
      const sheetPrice = parseInt(String(data[i][8]).replace(/[^\d]/g, ''), 10); // I列
      const sheetAddress = String(data[i][5]).trim(); // F列

      if (!sheetPrice || !sheetAddress) continue;

      if (sheetPrice === priceValue && sheetAddress.includes(pdfAddress)) {
        const linkFormula = `=HYPERLINK("${file.getUrl()}", "図面")`;
        sheet.getRange(i + 1, 3).setFormula(linkFormula); // C列に挿入
        sheet.getRange(i + 1, 7).setValue("✔ 一致");
        matched = true;
        break;
      }
    }

    if (!matched) {
      sheet.appendRow([
        "✖ 不一致", `PDF: ${file.getName()}`, `抽出価格: ${priceValue}`, `抽出住所: ${pdfAddress}`
      ]);
    }
  }
}