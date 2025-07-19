# Flask Backend Deployment Guide

This guide provides instructions on how to deploy the Flask backend for the Library Management System.

## 🚀 Overview

The Flask backend provides the RESTful API for managing books, handling check-in/check-out operations, and providing library statistics. It uses SQLite as its database, which is suitable for development and small-scale deployments. For production, consider migrating to a more robust database like PostgreSQL.

## 🛠 Prerequisites

- Python 3.11 or higher
- `pip` (Python package installer)
- `gunicorn` (for production deployment)
- A hosting service (e.g., Heroku, Railway, DigitalOcean, AWS Elastic Beanstalk)

## 📁 Project Structure

```
library_management/
├── src/
│   ├── models/              # Database models (book.py, user.py)
│   ├── routes/              # API routes (book.py, user.py)
│   ├── database/            # Contains app.db (SQLite database file)
│   └── main.py              # Flask application entry point
├── venv/                    # Python virtual environment
├── requirements.txt         # Python dependencies
├── Procfile                 # For Heroku deployment
└── README.md                # Project README
```

## 🚀 Local Development

To run the Flask backend locally:

1.  **Navigate to the project directory:**
    ```bash
    cd library_management
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Flask application:**
    ```bash
    python src/main.py
    ```

    The API will be available at `http://localhost:5000/api`.

## ☁️ Deployment to Cloud Platforms

### Option 1: Heroku (Recommended for quick deployment)

Heroku is a platform as a service (PaaS) that allows you to deploy, run, and manage applications entirely in the cloud.

#### Step 1: Prepare your Flask application

1.  **Create a `Procfile`** in the root of your `library_management` directory. This file tells Heroku how to run your application:
    ```
    web: gunicorn src.main:app
    ```
    *Note: `src.main:app` assumes your Flask app instance is named `app` in `src/main.py`.*

2.  **Add `gunicorn` to `requirements.txt`**:
    If not already present, add `gunicorn` to your `requirements.txt` file:
    ```
    Flask==3.0.3
    Flask-SQLAlchemy==3.1.1
    Flask-CORS==4.0.0
    SQLAlchemy==2.0.29
    gunicorn==21.2.0
    ```

3.  **Create a `runtime.txt`** (optional, but recommended for specific Python version):
    ```
    python-3.11.0
    ```

#### Step 2: Deploy using Heroku CLI

1.  **Install Heroku CLI** (if you haven't already):
    Follow the instructions on the [Heroku Dev Center](https://devcenter.heroku.com/articles/heroku-cli).

2.  **Log in to Heroku:**
    ```bash
    heroku login
    ```

3.  **Navigate to your project directory:**
    ```bash
    cd library_management
    ```

4.  **Create a new Heroku application:**
    ```bash
    heroku create your-library-backend-app-name
    ```
    (Replace `your-library-backend-app-name` with a unique name for your app. Heroku will provide a URL like `https://your-library-backend-app-name.herokuapp.com/`)

5.  **Push your code to Heroku:**
    ```bash
    git add .
    git commit -m "Prepare for Heroku deployment"
    git push heroku main
    ```
    *Note: If your main branch is named `master`, use `git push heroku master`.*

6.  **Scale your web dyno (if needed):**
    ```bash
    heroku ps:scale web=1
    ```

7.  **Open your deployed app:**
    ```bash
    heroku open
    ```
    Your Flask API will be accessible at `https://your-library-backend-app-name.herokuapp.com/api`.

### Option 2: Railway

Railway is another excellent PaaS that simplifies deployment.

1.  **Connect your GitHub repository** to Railway.
2.  Railway will usually **auto-detect** your Flask application.
3.  **Configure environment variables** in the Railway dashboard if needed (e.g., for database connections if you switch from SQLite).
4.  **Deploy** your application.

### Option 3: DigitalOcean App Platform / AWS Elastic Beanstalk

These services offer more control and scalability but require more configuration.

1.  **Containerize your Flask app** (e.g., using Docker) for easier deployment.
2.  **Follow the specific deployment guides** for DigitalOcean App Platform or AWS Elastic Beanstalk.

## 🔒 CORS Configuration

It is crucial to configure CORS (Cross-Origin Resource Sharing) on your Flask backend to allow your Next.js frontend to communicate with it. In `src/main.py`, ensure your `CORS` configuration is updated to allow requests from your deployed Next.js frontend URL.

```python
from flask_cors import CORS

app = Flask(__name__)
# ... other app configurations ...

# Configure CORS to allow requests from your Next.js frontend
# Replace 'https://your-nextjs-app.vercel.app' with the actual URL of your deployed Next.js app
CORS(app, resources={r"/api/*": {"origins": "https://your-nextjs-app.vercel.app"}})

# ... rest of your main.py ...
```

## 🗄️ Database Considerations

-   **SQLite (`app.db`)**: The current setup uses SQLite, which is file-based. For production environments, especially with multiple instances or high traffic, it's recommended to migrate to a client-server database like PostgreSQL or MySQL.
-   **Database Migrations**: For schema changes, consider using Flask-Migrate (based on Alembic) to manage database migrations.

## 🧪 Testing Your Deployed Backend

After deployment, you can test your API endpoints using `curl` or tools like Postman:

-   **Get all books:**
    ```bash
    curl https://your-flask-backend-app-name.herokuapp.com/api/books
    ```

-   **Add a new book:**
    ```bash
    curl -X POST https://your-flask-backend-app-name.herokuapp.com/api/books \
      -H "Content-Type: application/json" \
      -d 
    ```

-   **Get statistics:**
    ```bash
    curl https://your-flask-backend-app-name.herokuapp.com/api/books/stats
    ```

Ensure all endpoints respond as expected. Once your backend is deployed and accessible, you can update the `NEXT_PUBLIC_API_URL` in your Next.js frontend to point to this new backend URL.

