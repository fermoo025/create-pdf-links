import requests

url = 'https://script.google.com/macros/s/AKfycbyiCHn1ZYHgEn0mULf2kBA3KopNdDtJR0-28pbDWNLz4ce956w4NxnHZ4mUvmItwrUg/exec'
data = {'folderId': '1TRXjKEfWGK8OAh5TIP8_CFjmbIHEGKul', 'sheetId': '1CVAAilMvM8LsrZIelRz6nf4SRvFeoawGonw6L4QlSC8',
        'command': 'qq'}

response = requests.post(url, json=data)
print(response.text)
