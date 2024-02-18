import unittest
from main import app, db, User

class TestDeleteUser(unittest.TestCase):
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

    def test_delete_user(self):
        user = User(name='Adam Malysz', phone_number='999')
        with app.app_context():
            db.session.add(user)
            db.session.commit()

        response = self.app.delete(f'/delete_user/{user.id}')
        self.assertEqual(response.status_code, 200)
        with app.app_context():
            self.assertEqual(User.query.count(), 0)

if __name__ == '__main__':
    unittest.main()
