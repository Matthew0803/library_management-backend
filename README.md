# Library Management System

A modern, full-stack library management system built with Flask (backend) and React (frontend). This application provides a complete solution for managing library books, including check-in/check-out functionality, search capabilities, and real-time statistics.

## 🚀 Features

### Minimum Requirements ✅
- **Book Management**: Add, edit, and delete books with comprehensive metadata
- **Check-in/Check-out**: Track book borrowing with borrower information and due dates
- **Search Functionality**: Find books by title, author, genre, ISBN, or description

### Additional Features 🌟
- **Real-time Statistics Dashboard**: Track total books, available books, checked-out books, and overdue items
- **Professional UI**: Modern, responsive design using Tailwind CSS and shadcn/ui components
- **Data Persistence**: SQLite database ensures data is maintained between sessions
- **Input Validation**: Comprehensive validation on both frontend and backend
- **Error Handling**: User-friendly error messages and proper error handling
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## 🛠 Technology Stack

### Backend
- **Framework**: Flask 3.1.1
- **Database**: SQLite with SQLAlchemy ORM
- **API**: RESTful API with CORS support
- **Validation**: Input validation and error handling

### Frontend
- **Framework**: React 18 with modern hooks
- **UI Library**: shadcn/ui components with Tailwind CSS
- **Icons**: Lucide React icons
- **Build Tool**: Vite for fast development and building

## 📋 Prerequisites

- Python 3.11 or higher
- Node.js 20 or higher (for development)
- pip (Python package manager)

## 🚀 Quick Start

### Option 1: Run the Complete Application (Recommended)

The application is already built and ready to run as a unified Flask application:

```bash
# Navigate to the project directory
cd library_management

# Activate the virtual environment
source venv/bin/activate

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Start the application
python src/main.py
```

The application will be available at `http://localhost:5000`

### Option 2: Development Mode (Frontend and Backend Separately)

If you want to run the frontend and backend separately for development:

#### Backend Setup
```bash
# Navigate to the backend directory
cd library_management

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the Flask server
python src/main.py
```

#### Frontend Setup (in a new terminal)
```bash
# Navigate to the frontend directory
cd library-frontend

# Install dependencies
pnpm install

# Start the development server
pnpm run dev --host
```

## 📁 Project Structure

```
library_management/
├── src/
│   ├── models/
│   │   ├── user.py          # User model (template)
│   │   └── book.py          # Book model with check-in/out logic
│   ├── routes/
│   │   ├── user.py          # User routes (template)
│   │   └── book.py          # Book API endpoints
│   ├── static/              # Built React frontend files
│   ├── database/
│   │   └── app.db          # SQLite database
│   └── main.py             # Flask application entry point
├── venv/                   # Python virtual environment
├── requirements.txt        # Python dependencies
└── README.md              # This file

library-frontend/           # React frontend source (for development)
├── src/
│   ├── components/         # React components
│   ├── App.jsx            # Main application component
│   └── main.jsx           # React entry point
├── dist/                  # Built frontend files
└── package.json           # Node.js dependencies
```

## 🔌 API Endpoints

### Books
- `GET /api/books` - Get all books (with optional search)
- `POST /api/books` - Create a new book
- `GET /api/books/{id}` - Get a specific book
- `PUT /api/books/{id}` - Update a book
- `DELETE /api/books/{id}` - Delete a book
- `POST /api/books/{id}/checkout` - Check out a book
- `POST /api/books/{id}/checkin` - Check in a book
- `GET /api/books/search` - Advanced search
- `GET /api/books/stats` - Get library statistics

### Request/Response Examples

#### Create a Book
```bash
curl -X POST http://localhost:5000/api/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "genre": "Fiction",
    "publication_year": 1925,
    "isbn": "978-0-7432-7356-5",
    "description": "A classic American novel"
  }'
```

#### Check Out a Book
```bash
curl -X POST http://localhost:5000/api/books/1/checkout \
  -H "Content-Type: application/json" \
  -d '{
    "borrower_name": "John Doe",
    "borrower_email": "john@example.com",
    "days": 14
  }'
```

## 🎯 Usage Guide

### Adding Books
1. Click the "Add Book" button
2. Fill in the required fields (Title and Author)
3. Optionally add Genre, Publication Year, ISBN, and Description
4. Click "Add Book" to save

### Searching Books
1. Enter search terms in the search box
2. Search works across title, author, genre, ISBN, and description
3. Click "Search" or press Enter

### Checking Out Books
1. Find an available book
2. Click the "Check Out" button
3. Enter borrower name and email
4. Optionally adjust the loan period (default: 14 days)
5. Click "Check Out"

### Checking In Books
1. Find a checked-out book
2. Click the "Check In" button
3. The book will be marked as available

### Editing Books
1. Click the "Edit" button on any book
2. Modify the desired fields
3. Click "Update Book" to save changes

### Deleting Books
1. Click the "Delete" button on any available book
2. Confirm the deletion in the dialog
3. Note: Checked-out books cannot be deleted

## 🔧 Configuration

### Database Configuration
The application uses SQLite by default. The database file is located at `src/database/app.db`. To use a different database, modify the `SQLALCHEMY_DATABASE_URI` in `src/main.py`.

### CORS Configuration
CORS is enabled for all origins in development. For production, consider restricting origins in `src/main.py`.

## 🧪 Testing

The application has been thoroughly tested with the following scenarios:
- ✅ Adding books with all metadata fields
- ✅ Editing existing books
- ✅ Deleting available books (prevents deletion of checked-out books)
- ✅ Searching across all book fields
- ✅ Checking out books with borrower information
- ✅ Checking in books
- ✅ Real-time statistics updates
- ✅ Responsive design on different screen sizes
- ✅ Error handling and validation

## 🚀 Deployment

The application is ready for deployment as a unified Flask application. The React frontend is built and served from Flask's static directory.

### Production Considerations
1. Set `debug=False` in `src/main.py`
2. Use a production WSGI server like Gunicorn
3. Configure proper CORS origins
4. Use environment variables for sensitive configuration
5. Consider using PostgreSQL for production database

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is created as a take-home assignment and is available for educational purposes.

## 🆘 Troubleshooting

### Common Issues

**Port already in use**
```bash
# Kill any process using port 5000
sudo lsof -ti:5000 | xargs kill -9
```

**Virtual environment issues**
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Database issues**
```bash
# Reset database (will lose all data)
rm src/database/app.db
python src/main.py  # Will recreate the database
```

## 📞 Support

For questions or issues, please refer to the code comments or create an issue in the repository.

---

**Built with ❤️ for Valsoft Interview Assignment**

