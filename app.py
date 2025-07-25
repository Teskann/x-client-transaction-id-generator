from flask import Flask, request, jsonify
import bs4
import requests
from x_client_transaction.utils import generate_headers, handle_x_migration, get_ondemand_file_url
from x_client_transaction import ClientTransaction

app = Flask(__name__)

def initialize_session():
    session = requests.Session()
    session.headers = generate_headers()
    home_page_response = handle_x_migration(session=session)
    ondemand_file_url = get_ondemand_file_url(response=home_page_response)
    ondemand_file = session.get(url=ondemand_file_url)
    ondemand_file_response = bs4.BeautifulSoup(ondemand_file.content, 'html.parser')
    return ClientTransaction(home_page_response=home_page_response, ondemand_file_response=ondemand_file_response)

client_transaction = initialize_session()

@app.route('/generate-x-client-transaction-id', methods=['GET'])
def generate_transaction_id():
    global client_transaction
    path = request.args.get('path')

    if not path:
        return jsonify({'error': "Missing required parameter 'path'"}), 400

    transaction_id = client_transaction.generate_transaction_id('GET', path=path)

    return jsonify({
        'x-client-transaction-id': transaction_id
    })

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

@app.route('/reset-session', methods=['GET'])
def reset_session():
    def token_is_valid(token):
        from pathlib import Path
        with open(Path(__file__).parent / 'reset-session-token-secret.txt', 'r') as f:
            accepted_token = f.read()
        return token == accepted_token

    token = request.args.get('token')
    if not token or not token_is_valid(token):
        return jsonify({'error': 'Invalid token'}), 401

    global client_transaction
    client_transaction = initialize_session()
    return jsonify({'message': 'Session reinitialized successfully'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)