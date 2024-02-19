import unittest
from main import app, db, User

class TestCheckUserNamePalindrome(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_check_user_name_palindrome(self):
        data = {'nazwa_osoby': 'Jaroslaw Niedisco'}
        response = self.app.post('/check_user_name_palindrome', json=data)

        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertEqual(result['nazwa_osoby'], 'Jaroslaw Niedisco')
        self.assertFalse(result['is_palindrome'])

        data_palindrome = {'nazwa_osoby': 'level'}
        response_palindrome = self.app.post('/check_user_name_palindrome', json=data_palindrome)

        self.assertEqual(response_palindrome.status_code, 200)
        result_palindrome = response_palindrome.get_json()
        self.assertEqual(result_palindrome['nazwa_osoby'], 'level')
        self.assertTrue(result_palindrome['is_palindrome'])

if __name__ == '__main__':
    unittest.main()
