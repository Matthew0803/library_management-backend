# Library Management System - API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication
Currently, no authentication is required for API access.

## Response Format
All API responses are in JSON format. Successful responses include the requested data, while error responses include an `error` field with a descriptive message.

## Book Management Endpoints

### 1. Get All Books
**Endpoint:** `GET /books`

**Description:** Retrieve all books with optional search and pagination.

**Query Parameters:**
- `search` (optional): Search term to filter books
- `page` (optional): Page number for pagination (default: 1)
- `per_page` (optional): Number of books per page (default: 20)

**Example Request:**
```bash
curl "http://localhost:5000/api/books?search=gatsby&page=1&per_page=10"
```

**Example Response:**
```json
{
  "books": [
    {
      "id": 1,
      "title": "The Great Gatsby",
      "author": "F. Scott Fitzgerald",
      "isbn": "978-0-7432-7356-5",
      "genre": "Fiction",
      "publication_year": 1925,
      "description": "A classic American novel set in the Jazz Age",
      "is_checked_out": false,
      "borrower_name": null,
      "borrower_email": null,
      "checkout_date": null,
      "due_date": null,
      "created_at": "2025-07-19T01:54:22.970858",
      "updated_at": "2025-07-19T01:54:22.970861"
    }
  ],
  "total": 1,
  "pages": 1,
  "current_page": 1,
  "per_page": 10
}
```

### 2. Create a New Book
**Endpoint:** `POST /books`

**Description:** Add a new book to the library.

**Request Body:**
```json
{
  "title": "Book Title",           // Required
  "author": "Author Name",         // Required
  "isbn": "978-0-123456-78-9",    // Optional
  "genre": "Fiction",             // Optional
  "publication_year": 2023,       // Optional
  "description": "Book description" // Optional
}
```

**Example Request:**
```bash
curl -X POST http://localhost:5000/api/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "1984",
    "author": "George Orwell",
    "genre": "Dystopian Fiction",
    "publication_year": 1949,
    "description": "A dystopian social science fiction novel"
  }'
```

**Example Response:**
```json
{
  "id": 2,
  "title": "1984",
  "author": "George Orwell",
  "isbn": null,
  "genre": "Dystopian Fiction",
  "publication_year": 1949,
  "description": "A dystopian social science fiction novel",
  "is_checked_out": false,
  "borrower_name": null,
  "borrower_email": null,
  "checkout_date": null,
  "due_date": null,
  "created_at": "2025-07-19T02:00:00.000000",
  "updated_at": "2025-07-19T02:00:00.000000"
}
```

### 3. Get a Specific Book
**Endpoint:** `GET /books/{id}`

**Description:** Retrieve details of a specific book by ID.

**Path Parameters:**
- `id`: Book ID (integer)

**Example Request:**
```bash
curl http://localhost:5000/api/books/1
```

**Example Response:**
```json
{
  "id": 1,
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "isbn": "978-0-7432-7356-5",
  "genre": "Fiction",
  "publication_year": 1925,
  "description": "A classic American novel set in the Jazz Age",
  "is_checked_out": true,
  "borrower_name": "John Doe",
  "borrower_email": "john@example.com",
  "checkout_date": "2025-07-19T01:54:27.659431",
  "due_date": "2025-08-02T01:54:27.659436",
  "created_at": "2025-07-19T01:54:22.970858",
  "updated_at": "2025-07-19T01:54:27.659444"
}
```

### 4. Update a Book
**Endpoint:** `PUT /books/{id}`

**Description:** Update an existing book's information.

**Path Parameters:**
- `id`: Book ID (integer)

**Request Body:** (All fields optional)
```json
{
  "title": "Updated Title",
  "author": "Updated Author",
  "isbn": "978-0-123456-78-9",
  "genre": "Updated Genre",
  "publication_year": 2024,
  "description": "Updated description"
}
```

**Example Request:**
```bash
curl -X PUT http://localhost:5000/api/books/1 \
  -H "Content-Type: application/json" \
  -d '{
    "description": "An updated description of the book"
  }'
```

**Example Response:**
```json
{
  "id": 1,
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "isbn": "978-0-7432-7356-5",
  "genre": "Fiction",
  "publication_year": 1925,
  "description": "An updated description of the book",
  "is_checked_out": false,
  "borrower_name": null,
  "borrower_email": null,
  "checkout_date": null,
  "due_date": null,
  "created_at": "2025-07-19T01:54:22.970858",
  "updated_at": "2025-07-19T02:05:00.000000"
}
```

### 5. Delete a Book
**Endpoint:** `DELETE /books/{id}`

**Description:** Delete a book from the library. Cannot delete books that are currently checked out.

**Path Parameters:**
- `id`: Book ID (integer)

**Example Request:**
```bash
curl -X DELETE http://localhost:5000/api/books/1
```

**Success Response:** `204 No Content`

**Error Response (if book is checked out):**
```json
{
  "error": "Cannot delete a book that is currently checked out"
}
```

## Check-in/Check-out Endpoints

### 6. Check Out a Book
**Endpoint:** `POST /books/{id}/checkout`

**Description:** Check out a book to a borrower.

**Path Parameters:**
- `id`: Book ID (integer)

**Request Body:**
```json
{
  "borrower_name": "John Doe",           // Required
  "borrower_email": "john@example.com",  // Required
  "days": 14                            // Optional (default: 14)
}
```

**Example Request:**
```bash
curl -X POST http://localhost:5000/api/books/1/checkout \
  -H "Content-Type: application/json" \
  -d '{
    "borrower_name": "Jane Smith",
    "borrower_email": "jane@example.com",
    "days": 21
  }'
```

**Example Response:**
```json
{
  "message": "Book checked out successfully",
  "book": {
    "id": 1,
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "isbn": "978-0-7432-7356-5",
    "genre": "Fiction",
    "publication_year": 1925,
    "description": "A classic American novel set in the Jazz Age",
    "is_checked_out": true,
    "borrower_name": "Jane Smith",
    "borrower_email": "jane@example.com",
    "checkout_date": "2025-07-19T02:00:00.000000",
    "due_date": "2025-08-09T02:00:00.000000",
    "created_at": "2025-07-19T01:54:22.970858",
    "updated_at": "2025-07-19T02:00:00.000000"
  }
}
```

**Error Response (if book is already checked out):**
```json
{
  "error": "Book is already checked out"
}
```

### 7. Check In a Book
**Endpoint:** `POST /books/{id}/checkin`

**Description:** Check in a book (return it to the library).

**Path Parameters:**
- `id`: Book ID (integer)

**Example Request:**
```bash
curl -X POST http://localhost:5000/api/books/1/checkin
```

**Example Response:**
```json
{
  "message": "Book checked in successfully",
  "book": {
    "id": 1,
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "isbn": "978-0-7432-7356-5",
    "genre": "Fiction",
    "publication_year": 1925,
    "description": "A classic American novel set in the Jazz Age",
    "is_checked_out": false,
    "borrower_name": null,
    "borrower_email": null,
    "checkout_date": null,
    "due_date": null,
    "created_at": "2025-07-19T01:54:22.970858",
    "updated_at": "2025-07-19T02:05:00.000000"
  }
}
```

**Error Response (if book is not checked out):**
```json
{
  "error": "Book is not checked out"
}
```

## Search and Statistics Endpoints

### 8. Advanced Search
**Endpoint:** `GET /books/search`

**Description:** Advanced search with specific field filters.

**Query Parameters:**
- `title`: Filter by title (partial match)
- `author`: Filter by author (partial match)
- `genre`: Filter by genre (partial match)
- `isbn`: Filter by ISBN (partial match)
- `available_only`: Show only available books (true/false)

**Example Request:**
```bash
curl "http://localhost:5000/api/books/search?author=orwell&available_only=true"
```

**Example Response:**
```json
[
  {
    "id": 2,
    "title": "1984",
    "author": "George Orwell",
    "isbn": null,
    "genre": "Dystopian Fiction",
    "publication_year": 1949,
    "description": "A dystopian social science fiction novel",
    "is_checked_out": false,
    "borrower_name": null,
    "borrower_email": null,
    "checkout_date": null,
    "due_date": null,
    "created_at": "2025-07-19T02:00:00.000000",
    "updated_at": "2025-07-19T02:00:00.000000"
  }
]
```

### 9. Library Statistics
**Endpoint:** `GET /books/stats`

**Description:** Get library statistics including total books, available books, checked-out books, and overdue books.

**Example Request:**
```bash
curl http://localhost:5000/api/books/stats
```

**Example Response:**
```json
{
  "total_books": 10,
  "available_books": 7,
  "checked_out_books": 3,
  "overdue_books": 1
}
```

## Error Handling

### HTTP Status Codes
- `200 OK`: Successful GET, PUT requests
- `201 Created`: Successful POST requests
- `204 No Content`: Successful DELETE requests
- `400 Bad Request`: Invalid request data or business logic error
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

### Error Response Format
```json
{
  "error": "Descriptive error message"
}
```

### Common Error Messages
- `"Title and author are required"`: Missing required fields when creating a book
- `"Book is already checked out"`: Attempting to check out an already checked-out book
- `"Book is not checked out"`: Attempting to check in a book that isn't checked out
- `"Cannot delete a book that is currently checked out"`: Attempting to delete a checked-out book
- `"Borrower name and email are required"`: Missing required fields when checking out a book

## Rate Limiting
Currently, no rate limiting is implemented. For production use, consider implementing rate limiting to prevent abuse.

## Data Validation

### Book Fields
- `title`: String, required, max 200 characters
- `author`: String, required, max 100 characters
- `isbn`: String, optional, max 20 characters, should be unique
- `genre`: String, optional, max 50 characters
- `publication_year`: Integer, optional
- `description`: Text, optional

### Checkout Fields
- `borrower_name`: String, required, max 100 characters
- `borrower_email`: String, required, max 120 characters, must be valid email format
- `days`: Integer, optional, min 1, max 90, default 14

## Database Schema

### Books Table
```sql
CREATE TABLE book (
    id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    isbn VARCHAR(20) UNIQUE,
    genre VARCHAR(50),
    publication_year INTEGER,
    description TEXT,
    is_checked_out BOOLEAN DEFAULT FALSE,
    borrower_name VARCHAR(100),
    borrower_email VARCHAR(120),
    checkout_date DATETIME,
    due_date DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Testing the API

You can test the API using curl commands as shown in the examples above, or use tools like:
- Postman
- Insomnia
- HTTPie
- Browser developer tools

For automated testing, consider using:
- pytest for Python backend tests
- Jest for JavaScript frontend tests
- Selenium for end-to-end testing

