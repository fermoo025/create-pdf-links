from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def form():
    return render_template('form.html')

@app.route('/proxy', methods=['POST'])
def proxy_to_gas():
    try:
        data = request.get_json()
        appId = data['appId']; del data['appId']; data['command'] = 'convert'
        url=f'https://script.google.com/macros/s/{appId}/exec'
        response = requests.post(url, json=data, timeout=285)
        print(response.text)
        return jsonify({
            'status': 'ok',
            'gas_response': response.text.strip()
        })
    except requests.exceptions.Timeout:
        return jsonify({
            'status': 'timeout',
            'gas_response': 'yet (timeout)'
        }), 200
    except Exception as e:
        print(e)
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
