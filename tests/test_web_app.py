import pytest
from web_app import app as flask_app

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def login(client, username='admin', password='password123'):
    return client.post('/login', data=dict(username=username, password=password), follow_redirects=True)

def test_login_logout(client):
    rv = login(client)
    assert b'Dashboard' in rv.data
    rv = client.get('/logout', follow_redirects=True)
    assert b'Login' in rv.data

def test_export_transactions_requires_login(client):
    rv = client.get('/transactions/export')
    assert rv.status_code == 302  # Redirect to login

def test_export_transactions_after_login(client):
    login(client)
    rv = client.get('/transactions/export')
    assert rv.status_code == 200
    assert rv.headers['Content-Disposition'].startswith('attachment;')

def test_notifications_page(client):
    login(client)
    rv = client.get('/notifications')
    assert rv.status_code == 200
    assert b'Notifications' in rv.data
