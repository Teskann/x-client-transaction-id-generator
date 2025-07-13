from flask_app_fixtures import client


def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_json() == {'status': 'healthy'}

def test_generate_transaction_id_missing_path(client):
    response = client.get('/generate-x-client-transaction-id')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == "Missing required parameter 'path'"

def test_generate_transaction_id_with_path(client):
    response = client.get('/generate-x-client-transaction-id?path=/test')
    assert response.status_code == 200
    data = response.get_json()
    assert 'x-client-transaction-id' in data
    assert isinstance(data['x-client-transaction-id'], str)

def test_reset_session(client):
    def get_token():
        from pathlib import Path
        with open(Path(__file__).parent.parent / 'reset-session-token-secret.txt', 'r') as f:
            return f.read()
    token = get_token()
    response = client.get(f'/reset-session?token={token}')
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Session reinitialized successfully'}

def test_reset_session_invalid_token(client):
    response = client.get(f'/reset-session')
    assert response.status_code == 401
    assert response.get_json() == {'error': 'Invalid token'}

    response = client.get(f'/reset-session?token=invalid-token')
    assert response.status_code == 401
    assert response.get_json() == {'error': 'Invalid token'}

def test_generate_transaction_id_different_paths(client):
    response1 = client.get('/generate-x-client-transaction-id?path=/test1')
    response2 = client.get('/generate-x-client-transaction-id?path=/test2')

    assert response1.status_code == 200
    assert response2.status_code == 200

    data1 = response1.get_json()
    data2 = response2.get_json()

    assert 'x-client-transaction-id' in data1
    assert 'x-client-transaction-id' in data2
