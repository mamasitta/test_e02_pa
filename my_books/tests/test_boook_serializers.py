from django.test import TestCase
from datetime import date
from ..serializers import BookSerializer
from ..models import Book

class BookSerializerTest(TestCase):

    def setUp(self):
        self.book_data = {
            'title': 'Test Book',
            'author': 'Test Aut',
            'description': 'This is test description',
            'published_date': date(2020, 1, 1),
            'is_published': True
        }


    def test_book_valid_serializer(self):
        serializer = BookSerializer(data=self.book_data)
        self.assertTrue(serializer.is_valid())


        book = serializer.save()
        self.assertEqual(book.title, self.book_data['title'])
        self.assertEqual(book.author, self.book_data['author'])

    def test_book_serializer_duplicate_title(self):
        Book.objects.create(**self.book_data)

        serializer = BookSerializer(data=self.book_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
        self.assertIn('already exists', str(serializer.errors['title']))
