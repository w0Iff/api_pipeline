import unittest
from main import app, db, User

class TestAddUser(unittest.TestCase):
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

    def test_add_user(self):
        data = {'name': 'Adam Lata', 'phone_number': '444'}
        response = self.app.post('/add_user', json=data)
        self.assertEqual(response.status_code, 200)
        with app.app_context():
            self.assertEqual(User.query.count(), 1)

if __name__ == '__main__':
    unittest.main()
