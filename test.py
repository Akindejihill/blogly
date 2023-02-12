from unittest import TestCase
from app import app
from models import make_db, seed_db
from flask import session
##import nessesary app components

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly-test'
if app.config['SQLALCHEMY_DATABASE_URI'] == 'postgresql:///blogly':
    print("YOU ARE USING THE ACTUAL DATABASE!   !!!! STOP !!!!   Use the test database FOOL!")
    exit()


class ConnectionTests(TestCase):

    def test_connection_userslist(self):
        with app.test_client() as client:
            result = client.get('/users')
            html = result.get_data(as_text = True)

            self.assertEqual(result.status_code, 200)
            self.assertIn( '<title>List Users</title>', html)

    def test_connection_user(self):
        with app.test_client() as client:
            result = client.get('/users/1')
            html = result.get_data(as_text = True)

            self.assertEqual(result.status_code, 200)
            self.assertIn( '<h1>Alen Alda</h1>', html)

    def test_connection_edit_user(self):
        with app.test_client() as client:
            result = client.get('/users/1/edit')
            html = result.get_data(as_text = True)

            self.assertEqual(result.status_code, 200)
            
            

    def test_connection_delete_user(self):
        with app.test_client() as client:
            result = client.get('/users/55/delete')
            html = result.get_data(as_text = True)
            self.assertEqual(result.status_code, 302)

    def test_connection_create_tag(self):
        with app.test_client() as client:
            result = client.get('/tags/new')
            html = result.get_data(as_text = True)
            self.assertEqual(result.status_code, 200)

    def test_connection_edit_tag(self):
        with app.test_client() as client:
            result = client.get('/tags/1/edit')
            html = result.get_data(as_text = True)
            self.assertEqual(result.status_code, 200)

    def test_connection_tag_list(self):
        with app.test_client() as client:
            result = client.get('/tags')
            html = result.get_data(as_text = True)
            self.assertEqual(result.status_code, 200)

    def test_connection_show_tag(self):
        with app.test_client() as client:
            result = client.get('/tags/1')
            html = result.get_data(as_text = True)
            self.assertEqual(result.status_code, 200)

    def test_connection_show_tag(self):
        with app.test_client() as client:
            result = client.get('/posts/1')
            html = result.get_data(as_text = True)
            self.assertEqual(result.status_code, 200)

    def test_connection_show_tag(self):
        with app.test_client() as client:
            result = client.get('/users/1/posts/new')
            html = result.get_data(as_text = True)
            self.assertEqual(result.status_code, 200)

    def test_connection_show_tag(self):
        with app.test_client() as client:
            result = client.get('/posts/1/edit')
            html = result.get_data(as_text = True)
            self.assertEqual(result.status_code, 200)


class SubmissionTests(TestCase):

    @classmethod
    def tearDownClass(self):
        make_db()
        seed_db()

    def test_Create_tag_submission(self):
        with app.test_client() as client:
            result = client.post('/tags/new', data={'tag': 'untittest_tag'})
            html = result.get_data(as_text = True)
            self.assertEqual(result.status_code, 302)
            self.assertIn('<p>You should be redirected automatically to the target URL: <a href="/tags">/tags</a>', html)

    def test_Edit_tag_submission(self):
        with app.test_client() as client:
            result = client.post('/tags/1/edit', data={'name': 'first post_alt'})
            html = result.get_data(as_text = True)
            self.assertEqual(result.status_code, 302)
            self.assertIn('You should be redirected automatically to the target URL: <a href="/tags">/tags</a>', html)

