from flask import Blueprint, jsonify, request
from src.models.book import Book, db
from sqlalchemy import or_

book_bp = Blueprint('book', __name__)

@book_bp.route('/books', methods=['GET'])
def get_books():
    """Get all books with optional search functionality"""
    search = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = Book.query
    
    if search:
        # Search in title, author, genre, and description
        search_filter = or_(
            Book.title.ilike(f'%{search}%'),
            Book.author.ilike(f'%{search}%'),
            Book.genre.ilike(f'%{search}%'),
            Book.description.ilike(f'%{search}%'),
            Book.isbn.ilike(f'%{search}%')
        )
        query = query.filter(search_filter)
    
    # Pagination
    books = query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    return jsonify({
        'books': [book.to_dict() for book in books.items],
        'total': books.total,
        'pages': books.pages,
        'current_page': page,
        'per_page': per_page
    })

@book_bp.route('/books', methods=['POST'])
def create_book():
    """Add a new book to the library"""
    try:
        print(f"Received request: {request.method}")
        print(f"Content-Type: {request.content_type}")
        print(f"Request data: {request.data}")
        
        data = request.json
        print(f"Parsed JSON: {data}")
        
        # Validate required fields
        if not data.get('title') or not data.get('author'):
            print("Validation failed: Missing title or author")
            return jsonify({'error': 'Title and author are required'}), 400
        
        print(f"Creating book with title: {data['title']}, author: {data['author']}")
        
        book = Book(
            title=data['title'],
            author=data['author'],
            isbn=data.get('isbn') if data.get('isbn') and data.get('isbn').strip() else None,
            genre=data.get('genre'),
            publication_year=data.get('publication_year'),
            description=data.get('description')
        )
        
        print("Book object created, adding to database...")
        db.session.add(book)
        db.session.commit()
        print("Book successfully added to database")
        
        return jsonify(book.to_dict()), 201
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@book_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Get a specific book by ID"""
    book = Book.query.get_or_404(book_id)
    return jsonify(book.to_dict())

@book_bp.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """Update a book's information"""
    try:
        book = Book.query.get_or_404(book_id)
        data = request.json
        
        # Update fields if provided
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.isbn = data.get('isbn', book.isbn)
        book.genre = data.get('genre', book.genre)
        book.publication_year = data.get('publication_year', book.publication_year)
        book.description = data.get('description', book.description)
        
        db.session.commit()
        return jsonify(book.to_dict())
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@book_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Delete a book from the library"""
    try:
        book = Book.query.get_or_404(book_id)
        
        # Check if book is currently checked out
        if book.is_checked_out:
            return jsonify({'error': 'Cannot delete a book that is currently checked out'}), 400
        
        db.session.delete(book)
        db.session.commit()
        return '', 204
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@book_bp.route('/books/<int:book_id>/checkout', methods=['POST'])
def checkout_book(book_id):
    """Check out a book to a borrower"""
    try:
        book = Book.query.get_or_404(book_id)
        data = request.json
        
        # Validate required fields
        if not data.get('borrower_name') or not data.get('borrower_email'):
            return jsonify({'error': 'Borrower name and email are required'}), 400
        
        success, message = book.checkout(
            borrower_name=data['borrower_name'],
            borrower_email=data['borrower_email'],
            days=data.get('days', 14)
        )
        
        if not success:
            return jsonify({'error': message}), 400
        
        db.session.commit()
        return jsonify({
            'message': message,
            'book': book.to_dict()
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@book_bp.route('/books/<int:book_id>/checkin', methods=['POST'])
def checkin_book(book_id):
    """Check in a book (return it)"""
    try:
        book = Book.query.get_or_404(book_id)
        
        success, message = book.checkin()
        
        if not success:
            return jsonify({'error': message}), 400
        
        db.session.commit()
        return jsonify({
            'message': message,
            'book': book.to_dict()
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@book_bp.route('/books/search', methods=['GET'])
def search_books():
    """Advanced search for books"""
    title = request.args.get('title', '')
    author = request.args.get('author', '')
    genre = request.args.get('genre', '')
    isbn = request.args.get('isbn', '')
    available_only = request.args.get('available_only', 'false').lower() == 'true'
    
    query = Book.query
    
    if title:
        query = query.filter(Book.title.ilike(f'%{title}%'))
    if author:
        query = query.filter(Book.author.ilike(f'%{author}%'))
    if genre:
        query = query.filter(Book.genre.ilike(f'%{genre}%'))
    if isbn:
        query = query.filter(Book.isbn.ilike(f'%{isbn}%'))
    if available_only:
        query = query.filter(Book.is_checked_out == False)
    
    books = query.all()
    return jsonify([book.to_dict() for book in books])

@book_bp.route('/books/stats', methods=['GET'])
def get_library_stats():
    """Get library statistics"""
    total_books = Book.query.count()
    checked_out_books = Book.query.filter(Book.is_checked_out == True).count()
    available_books = total_books - checked_out_books
    overdue_books = Book.query.filter(
        Book.is_checked_out == True,
        Book.due_date < db.func.datetime('now')
    ).count()
    
    return jsonify({
        'total_books': total_books,
        'available_books': available_books,
        'checked_out_books': checked_out_books,
        'overdue_books': overdue_books
    })
