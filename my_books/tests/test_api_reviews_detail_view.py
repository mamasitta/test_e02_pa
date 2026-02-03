from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Book, Review
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status


class ReviewDeatilViewTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            password='user1pass',
            email='user1@gmail.com'
        )

        self.user2 = User.objects.create_user(
            username='user2',
            password='user2pass',
            email='user2@gmail.com'
        )

        self.admin = User.objects.create_superuser(
            username='admin',
            password='adminpass',
            email='admin@gmail.com'
        )

        self.book = Book.objects.create(
            title='test book',
            author='test aut',
            published_date='2020-01-01',
            description='test desc'
        )

        self.review=Review.objects.create(
            author=self.user1,
            book=self.book,
            review='Review 1'
        )

        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)
        self.token_admin = Token.objects.create(user=self.admin)

        self.client = APIClient()
        self.url = lambda pk: reverse('books:review-detail', args=[pk])

    def test_get_review_detail_unauthenticated_client(self):
        responce = self.client.get(self.url(self.review.id))

        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        self.assertEqual(self.review.id, responce.data['id'])
        self.assertEqual(self.review.review, responce.data['review'])
        self.assertEqual(responce.data['author']['username'], self.user1.username)


    def test_get_review_detail_unauthenticated_client_not_existing_review_id(self):
        responce = self.client.get(self.url(9999999))

        self.assertEqual(responce.status_code, status.HTTP_404_NOT_FOUND)


    def test_put_update_review_with_review_author_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')

        updated_data = {
            'review': 'PUT update review',
            'book': self.book.pk
        }
        responce = self.client.put(
            self.url(self.review.id),
            updated_data,
            format='json'
        )
        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()
        self.assertEqual(self.review.review, 'PUT update review')


    def test_put_update_review_not_author_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2.key}')
        self.review.review
        updated_data = {
            'review': 'PUT update review',
            'book': self.book.pk
        }
        responce = self.client.put(
            self.url(self.review.id),
            updated_data,
            format='json'
        )
        self.assertEqual(responce.status_code, status.HTTP_403_FORBIDDEN)

    
        