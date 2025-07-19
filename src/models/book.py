from src.models.user import db
from datetime import datetime, timedelta

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=True)
    genre = db.Column(db.String(50), nullable=True)
    publication_year = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)
    is_checked_out = db.Column(db.Boolean, default=False, nullable=False)
    borrower_name = db.Column(db.String(100), nullable=True)
    borrower_email = db.Column(db.String(120), nullable=True)
    checkout_date = db.Column(db.DateTime, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'genre': self.genre,
            'publication_year': self.publication_year,
            'description': self.description,
            'is_checked_out': self.is_checked_out,
            'borrower_name': self.borrower_name,
            'borrower_email': self.borrower_email,
            'checkout_date': self.checkout_date.isoformat() if self.checkout_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def checkout(self, borrower_name, borrower_email, days=14):
        """Check out the book to a borrower"""
        if self.is_checked_out:
            return False, "Book is already checked out"
        
        self.is_checked_out = True
        self.borrower_name = borrower_name
        self.borrower_email = borrower_email
        self.checkout_date = datetime.utcnow()
        self.due_date = datetime.utcnow() + timedelta(days=days)
        self.updated_at = datetime.utcnow()
        return True, "Book checked out successfully"

    def checkin(self):
        """Check in the book (return it)"""
        if not self.is_checked_out:
            return False, "Book is not checked out"
        
        self.is_checked_out = False
        self.borrower_name = None
        self.borrower_email = None
        self.checkout_date = None
        self.due_date = None
        self.updated_at = datetime.utcnow()
        return True, "Book checked in successfully"

    def is_overdue(self):
        """Check if the book is overdue"""
        if not self.is_checked_out or not self.due_date:
            return False
        return datetime.utcnow() > self.due_date

