import json

from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework.test import APITestCase

from rest_framework_simplejwt.tokens import RefreshToken

from .models import Note

class NotesModelTestCase(TestCase):
    user1= None
    user2= None

    def setUp(self) -> None:
        self.user1= User.objects.create_user('test1', 'test1@test.com', 'test1')
        self.user2= User.objects.create_user('test2', 'test2@test.com', 'test2')
    
    def test_should_create_a_note(self):
        note= Note.objects.create(owner= self.user1, description='Test Note 1')
        self.assertEqual(note.description, 'Test Note 1')
        self.assertEqual(note.owner, self.user1)

    def test_should_share_existing_note_to_another_user(self):
        note= Note.objects.create(owner= self.user1, description='Test Note 1')
        note.shared_with.add(self.user2)
        
        shared_notes= Note.objects.filter(shared_with__id=self.user2.id)
        self.assertNotEqual(shared_notes.count(), 0)
        self.assertEqual(shared_notes.first(), note)

    def test_should_delete_notes_if_user_deleted(self):
        Note.objects.create(owner= self.user1, description='Test Note 1')
        Note.objects.create(owner= self.user1, description='Test Note 2')
        Note.objects.create(owner= self.user1, description='Test Note 3')

        count_before= Note.objects.filter(owner= self.user1).count()
        self.assertEqual(count_before, 3)
        
        self.user1.delete()

        count_after= Note.objects.filter(owner= self.user1).count()
        self.assertEqual(count_after, 0)


class NoteAPITestCase(APITestCase):
    user1= None
    user2= None
    token1= None
    token2= None

    def setUp(self) -> None:
        self.user1= User.objects.create_user('test1', 'test1@test.com', 'test1')
        self.user2= User.objects.create_user('test2', 'test2@test.com', 'test2')
        self.token1= str(RefreshToken().for_user(self.user1).access_token)
        self.token2= str(RefreshToken().for_user(self.user2).access_token)
        note1= Note.objects.create(owner= self.user1, description='User 1 Test Note 1')
        note1.shared_with.add(self.user2)
        note2= Note.objects.create(owner= self.user1, description='User 1 Test Note 2')
        note2.shared_with.add(self.user2)
        Note.objects.create(owner= self.user1, description='User 1 Test Note 3')
        Note.objects.create(owner= self.user2, description='User 2 Test Note 4')
        Note.objects.create(owner= self.user2, description='User 2 Test Note 5')

    def test_should_fetch_notes_of_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token1)
        _response= self.client.get('/api/notes/')
        _response_data= _response.json()
        self.assertEqual(len(_response_data), 3)
        self.assertContains(_response, 'User 1')
        self.assertNotContains(_response, 'User 2')

    def test_should_fetch_note_details_of_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token1)
        note= Note.objects.filter(owner=self.user1).first()
        _response= self.client.get(f'/api/notes/{note.id}/')
        _response_data= _response.json()

        self.assertIn('id', _response_data)
        self.assertIn('description', _response_data)
        self.assertIn('owner', _response_data)
        self.assertEqual(_response.status_code, 200)

    def test_should_fetch_shared_notes_of_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token2)
        _response= self.client.get('/api/notes/')
        _response_data= _response.json()
        self.assertEqual(len(_response_data), 4)
        self.assertContains(_response, 'User 1')
        self.assertContains(_response, 'User 2')
        self.assertNotContains(_response, 'Test Note 3')

    def test_should_fetch_notes_based_on_search_of_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token2)
        _response= self.client.get('/api/search/?description=User 2')
        _response_data= _response.json()
        self.assertEqual(len(_response_data), 2)
        self.assertContains(_response, 'User 2')
        self.assertNotContains(_response, 'User 1')

    def test_should_create_note_for_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token1)
        _response= self.client.post(
            '/api/notes/', 
            json.dumps({'description': 'New note from user 1'}), 
            content_type='application/json'
        )
        _response_data= _response.json()
        note= Note.objects.filter(id=_response_data['id']).first()

        self.assertIn('id', _response_data)
        self.assertIn('description', _response_data)
        self.assertIsNotNone(note)
        self.assertEqual(_response.status_code, 201)

    def test_should_update_note_for_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token1)
        note= Note.objects.filter(owner=self.user1).first()
        _response= self.client.put(
            f'/api/notes/{note.id}/', 
            json.dumps({'description': 'Updated Note'}), 
            content_type='application/json'
        )
        _response_data= _response.json()
        update_note= Note.objects.filter(id=_response_data['id']).first()

        self.assertIn('id', _response_data)
        self.assertIn('description', _response_data)
        self.assertIsNotNone(update_note)
        self.assertEqual(update_note.description, "Updated Note")
        self.assertEqual(_response.status_code, 200)

    def test_should_delete_note_for_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token1)
        note= Note.objects.filter(owner=self.user1).first()
        _response= self.client.delete(f'/api/notes/{note.id}/')
        self.assertEqual(_response.status_code, 204)

    def test_should_share_note_with_another_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token1)
        note= Note.objects.filter(owner=self.user1).first()
        _response= self.client.post(
            f'/api/notes/{note.id}/share', 
            json.dumps({'username':'test2'}), 
            content_type='application/json'
        )
        _response_data= _response.json()

        shared_note= Note.objects.filter(
            Q(shared_with__id=User.objects.get(username='test2').id) and
            Q(id=note.id) 
        ).first()

        self.assertIsNotNone(shared_note)
        self.assertEqual(shared_note.id, note.id)
        self.assertIn('message', _response_data)
        self.assertContains(
            _response, 
            'Shared note with user successfully!', 
            status_code=200
        )