import unittest
from main import app, db, User, Kamera

class TestFindUserWithCamera(unittest.TestCase):
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

    def test_find_user_with_camera(self):
        user_with_camera = User(name='Jarosław Tylkoniedisco', phone_number='112')
        user_without_camera = User(name='Adam Malysz', phone_number='997')

        with app.app_context():
            db.session.add_all([user_with_camera, user_without_camera])
            db.session.commit()

            camera_for_user = Kamera(user_id=user_with_camera.id)
            db.session.add(camera_for_user)
            db.session.commit()

        response = self.app.get('/find_user_with_camera?nazwa_osoby=Jarosław Tylkoniedisco')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('Jarosław Tylkoniedisco', data['nazwa_osoby'])
        self.assertIn('112', data['numer_telefonu'])
        self.assertTrue(data['ma_kamere'])

        response_no_camera = self.app.get('/find_user_with_camera?nazwa_osoby=Adam Malysz')
        data_no_camera = response_no_camera.get_json()
        self.assertEqual(response_no_camera.status_code, 200)
        self.assertIn('Adam Malysz', data_no_camera['blad'])

if __name__ == '__main__':
    unittest.main()
