# backend/books/models.py

class Book:
    """Classe Book simple pour commencer"""
    
    def __init__(self, title, author, isbn, total_copies=1):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.total_copies = total_copies
        self.available_copies = total_copies
    
    def is_available(self):
        """Vérifie si le livre est disponible"""
        return self.available_copies > 0
    
    def borrow(self):
        """Emprunte un livre"""
        if self.is_available():
            self.available_copies -= 1
            return True
        return False
    
    def return_book(self):
        """Retourne un livre"""
        if self.available_copies < self.total_copies:
            self.available_copies += 1
            return True
        return False