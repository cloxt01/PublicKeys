from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/proxy', methods=['GET'])
def proxy():
    target_url = request.args.get('url')
    response = requests.get(target_url)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(port=5000)
