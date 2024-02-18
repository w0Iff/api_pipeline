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
        user_with_camera = User(name='Jaroslaw Niedisco', phone_number='112')
        user_without_camera = User(name='Slawomir Tezniedisco', phone_number='997')

        camera_for_user = Kamera(user=user_with_camera)

        with app.app_context():
            db.session.add_all([user_with_camera, user_without_camera, camera_for_user])
            db.session.commit()

        response = self.app.get('/find_user_with_camera?nazwa_osoby=John Doe')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('Jaroslaw Niedisco', data['nazwa_osoby'])
        self.assertIn('112', data['numer_telefonu'])
        self.assertTrue(data['ma_kamere'])

        response_no_camera = self.app.get('/find_user_with_camera?nazwa_osoby=Slawomir Tezniedisco')
        data_no_camera = response_no_camera.get_json()
        self.assertEqual(response_no_camera.status_code, 200)
        self.assertIn('Slawomir Tezniedisco', data_no_camera['blad'])

if __name__ == '__main__':
    unittest.main()
