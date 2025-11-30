import pytest
from django.test import TestCase
from books.models import Book

class BookModelTests(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="123456789",
            available=True
        )
    
    def test_book_creation(self):
        assert self.book.title == "Test Book"
        assert self.book.available is True
    
    def test_book_string_representation(self):
        assert str(self.book) == "Test Book"