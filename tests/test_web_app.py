import unittest
from web_app import app as flask_app

class TestWebApp(unittest.TestCase):

    def setUp(self):
        flask_app.config['TESTING'] = True
        self.client = flask_app.test_client()

    def login(self, username='admin', password='password123'):
        return self.client.post('/login', data=dict(username=username, password=password), follow_redirects=True)

    def test_login_logout(self):
        rv = self.login()
        # Check if login redirects to home page with expected content
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Total Income', rv.data)  # Adjusted to check for dashboard content
        rv = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'Login', rv.data)

    def test_export_transactions_requires_login(self):
        rv = self.client.get('/transactions/export')
        self.assertEqual(rv.status_code, 302)  # Redirect to login

    def test_export_transactions_after_login(self):
        self.login()
        rv = self.client.get('/transactions/export')
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(rv.headers['Content-Disposition'].startswith('attachment;'))

    def test_notifications_page(self):
        self.login()
        rv = self.client.get('/notifications')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Notifications', rv.data)

if __name__ == '__main__':
    unittest.main()