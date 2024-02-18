import unittest
from main import app, db, User

class TestViewUsers(unittest.TestCase):
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

    def test_view_users(self):
        user1 = User(name='Adam Malysz', phone_number='777')
        user2 = User(name='Robert Mateja', phone_number='111')
        with app.app_context():
            db.session.add_all([user1, user2])
            db.session.commit()

        response = self.app.get('/view_users')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data['osoby']), 2)

if __name__ == '__main__':
    unittest.main()
