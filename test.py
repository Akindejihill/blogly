from unittest import TestCase
from app import app
from flask import session
##import nessesary app components


class ConnectionTests(TestCase):

    def test_list(self):
        with app.test_client() as client:
            result = client.get('/users')
            html = result.get_data(as_text = True)

            self.assertEqual(result.status_code, 200)
            self.assertIn( '<title>List Users</title>', html)

    def test_list(self):
        with app.test_client() as client:
            result = client.get('/users/1')
            html = result.get_data(as_text = True)

            self.assertEqual(result.status_code, 200)
            self.assertIn( 'First name: Alen', html)

    def test_list(self):
        with app.test_client() as client:
            result = client.get('/users/1/edit')
            html = result.get_data(as_text = True)

            self.assertEqual(result.status_code, 200)
            self.assertIn( 'Edit a user', html)

    def test_list(self):
        with app.test_client() as client:
            result = client.get('/users/55/delete')
            html = result.get_data(as_text = True)

            self.assertEqual(result.status_code, 302)




# class SubmissionTests(TestCase):

#     def test_submission(self):
#         with app.test_client() as client:
#             result0 = client.get('/users/1')
#             result = client.post('/submit', data={'key': 'value'})

#             self.assertEqual(result.status_code, 200)
#             self.assertIn(result.data['key'], 'expected text') 