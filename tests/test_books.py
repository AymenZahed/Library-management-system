# tests/test_books.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.books.models import Book

def test_book_creation():
    """Test la création d'un livre"""
    book = Book("Python Guide", "John Doe", "1234567890", 5)
    
    assert book.title == "Python Guide"
    assert book.author == "John Doe"
    assert book.isbn == "1234567890"
    assert book.total_copies == 5
    assert book.available_copies == 5

def test_book_availability():
    """Test la disponibilité d'un livre"""
    book = Book("Test Book", "Author", "1111111111", 3)
    
    # Livre disponible
    assert book.is_available() == True
    
    # Emprunter tous les livres
    book.borrow()
    book.borrow()
    book.borrow()
    
    # Plus disponible
    assert book.is_available() == False

def test_book_borrow_return():
    """Test emprunt et retour de livre"""
    book = Book("Demo Book", "Writer", "9999999999", 2)
    
    # Emprunter
    assert book.borrow() == True
    assert book.available_copies == 1
    
    # Retourner
    assert book.return_book() == True
    assert book.available_copies == 2