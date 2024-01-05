from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from rest_framework_simplejwt.tokens import RefreshToken


class UserLoginTestCase(APITestCase):

    def setUp(self):
        User.objects.create_user('test', 'test@test.com', 'test123')

    def test_login_should_return_access_and_refresh_token(self):
        _data= {
            'username': 'test', 
            'password': 'test123'
        }
        _response= self.client.post('/api/auth/login', data=_data)
        _response_data= _response.json()
        
        self.assertIn('refresh', _response_data)
        self.assertIn('access', _response_data)
        self.assertEqual(_response.status_code, 200)

    def test_login_should_return_unauthorized_when_credentials_are_invalid(self):
        _data= {
            'username': 'test_random', 
            'password': 'test123'
        }
        _response= self.client.post('/api/auth/login', data=_data)
        _response_data= _response.json()
        
        self.assertIn('detail', _response_data)
        self.assertEqual(_response_data['detail'], 'No active account found with the given credentials')
        self.assertEqual(_response.status_code, 401)


class UserSignUpTestCase(APITestCase):
    def setUp(self) -> None:
        User.objects.create_user('test', 'test@test.com', 'test123')

    def test_signup_should_return_access_and_refresh_token(self):
        _data= {
            'username':'test2',
            'email':'test2@test.com',
            'password':'random@1234',
            'first_name':'test',
            'last_name': 'test'
        }
        _response= self.client.post('/api/auth/signup', data=_data)
        _response_data= _response.json()

        user= User.objects.filter(username="test2").first()

        self.assertIsNotNone(user)
        self.assertIn('refresh', _response_data)
        self.assertIn('access', _response_data)
        self.assertEqual(_response.status_code, 200)

    def test_signup_should_return_existing_user_error(self):
        _data= {
            'username':'test',
            'email':'test@test.com',
            'password':'random123',
            'first_name':'test',
            'last_name': 'test'
        }
        _response= self.client.post('/api/auth/signup', data=_data)
        _response_data= _response.json()

        self.assertIn('username', _response_data)
        self.assertEqual(_response_data['username'][0], 'A user with that username already exists.')
        self.assertEqual(_response.status_code, 400)

    def test_signup_user_should_return_password_validations(self):
        _data= {
            'username':'test2',
            'email':'test2@test.com',
            'password':'12345',
            'first_name':'test',
            'last_name': 'test'
        }
        _response= self.client.post('/api/auth/signup', data=_data)
        _response_data= _response.json()

        user= User.objects.filter(username="test2").first()

        self.assertIsNone(user)
        self.assertIn('password', _response_data)
        self.assertContains(
            _response, 
            'This password is too short. It must contain at least 8 characters.', 
            status_code=400
        )
        self.assertContains(
            _response, 
            'This password is too common.', 
            status_code=400
        )
        self.assertContains(
            _response, 
            'This password is entirely numeric.', 
            status_code=400
        )

    def test_signup_should_return_common_attributes_error(self):
        _data= {
            'username':'test2',
            'email':'test2@test.com',
            'password':'test2123',
            'first_name':'test2123',
            'last_name': 'test'
        }
        _response= self.client.post('/api/auth/signup', data=_data)
        _response_data= _response.json()

        user= User.objects.filter(username="test2").first()
        self.assertIsNone(user)
        self.assertIn('password', _response_data)
        self.assertContains(
            _response, 
            'The password is too similar to the first name.', 
            status_code=400
        )


class RefreshTokenTestCase(APITestCase):
    def setUp(self) -> None:
        User.objects.create_user('test', 'test@test.com', 'test123')

    def test_refresh_token_should_return_new_access_token(self):
        user= User.objects.get(username='test')
        refresh= RefreshToken().for_user(user)

        _response= self.client.post('/api/auth/refresh', {'refresh': str(refresh)})
        _response_data= _response.json()

        self.assertIn('refresh', _response_data)
        self.assertIn('access', _response_data)
        self.assertNotEqual(_response_data['refresh'], str(refresh))
        self.assertNotEqual(_response_data['access'], str(refresh.access_token))
        self.assertEqual(_response.status_code, 200)

    def test_blacklisted_refresh_token_should_return_error(self):
        user= User.objects.get(username='test')
        refresh= RefreshToken().for_user(user)

        _response= self.client.post('/api/auth/refresh', {'refresh': str(refresh)})
        _response= self.client.post('/api/auth/refresh', {'refresh': str(refresh)})
        _response_data= _response.json()

        self.assertIn('detail', _response_data)
        self.assertIn('code', _response_data)
        self.assertEqual(_response_data['detail'], 'Token is blacklisted')
        self.assertEqual(_response_data['code'], 'token_not_valid')
        self.assertEqual(_response.status_code, 401)