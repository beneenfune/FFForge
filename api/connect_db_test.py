import io
import unittest

from __init__ import app, api

class FlaskIntegrationTestCase(unittest.TestCase):

    def setUp(self):
        # app.config['TESTING'] = True
        self.client = app.test_client()

    # def test_db_connection(self):
        
    # def test_file_input(self):
    #     self.assertEqual(response.status_code, 200)

    def test_string_input(self):

        # Get a response from client
        response = self.client.post('/api/text-input', data={
            'smiles_string':'test SMILES string!'
        })

        assert response.status.code == 200
        
        # Assert that the response is of string type
        # self.assertEqual(response.content_type, str)
    