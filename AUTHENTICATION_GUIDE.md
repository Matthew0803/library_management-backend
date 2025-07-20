# Authentication System Guide

## Overview

This library management system now includes a comprehensive authentication system with:

- **Google OAuth SSO** for easy login
- **JWT-based session management** with access and refresh tokens
- **Role-based access control** (Admin, Librarian, Member)
- **Permission-based authorization** for fine-grained access control

## User Roles & Permissions

### 🔴 Admin
- Full system access
- Manage users (create, update roles, activate/deactivate)
- All book operations (create, read, update, delete)
- Library statistics and management
- User management dashboard

### 🟡 Librarian
- Create and update books
- View all books and users
- Check out/in books
- View library statistics
- Cannot delete books or manage user roles

### 🟢 Member
- View books (browse catalog)
- Check out and return books
- Limited access to library features

## Setup Instructions

### 1. Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Google+ API
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
5. Set application type to "Web application"
6. Add authorized origins:
   - `http://localhost:3000` (for local development)
   - `https://your-frontend-domain.com` (for production)
7. Copy the Client ID

### 2. Environment Variables

Create a `.env` file in your project root:

```env
# Flask Configuration
SECRET_KEY=your-super-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Google OAuth Configuration
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com

# Database Configuration (optional)
DATABASE_URL=sqlite:///app.db
```

### 3. Railway Deployment

Add these environment variables in your Railway dashboard:

1. Go to your Railway project
2. Click on "Variables" tab
3. Add:
   - `SECRET_KEY`: Generate a secure random string
   - `JWT_SECRET_KEY`: Generate another secure random string
   - `GOOGLE_CLIENT_ID`: Your Google OAuth client ID

## API Endpoints

### Authentication Endpoints

#### Login with Google
```http
POST /api/auth/google
Content-Type: application/json

{
  "token": "google-oauth-token-here"
}
```

**Response:**
```json
{
  "access_token": "jwt-access-token",
  "refresh_token": "refresh-token",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "role": "member",
    "profile_picture": "https://...",
    "is_active": true
  }
}
```

#### Refresh Token
```http
POST /api/auth/refresh
Content-Type: application/json

{
  "refresh_token": "your-refresh-token"
}
```

#### Get Current User
```http
GET /api/auth/me
Authorization: Bearer your-access-token
```

#### Logout
```http
POST /api/auth/logout
Authorization: Bearer your-access-token
Content-Type: application/json

{
  "refresh_token": "your-refresh-token"
}
```

### Protected Book Endpoints

All book endpoints now require appropriate permissions:

- `GET /api/books` - No authentication required (public)
- `POST /api/books` - Requires `CREATE_BOOK` permission (Librarian/Admin)
- `PUT /api/books/:id` - Requires `UPDATE_BOOK` permission (Librarian/Admin)
- `DELETE /api/books/:id` - Requires `DELETE_BOOK` permission (Admin only)
- `POST /api/books/:id/checkout` - Requires `CHECKOUT_BOOK` permission (All roles)
- `POST /api/books/:id/checkin` - Requires `CHECKIN_BOOK` permission (All roles)

### User Management Endpoints (Admin/Librarian only)

#### Get All Users
```http
GET /api/auth/users
Authorization: Bearer your-access-token
```

#### Update User Role
```http
PUT /api/auth/users/:id/role
Authorization: Bearer your-access-token
Content-Type: application/json

{
  "role": "librarian"
}
```

#### Activate/Deactivate User (Admin only)
```http
PUT /api/auth/users/:id/status
Authorization: Bearer your-access-token
Content-Type: application/json

{
  "is_active": false
}
```

## Frontend Integration

### 1. Google OAuth Setup (React/Next.js)

Install Google OAuth library:
```bash
npm install @google-cloud/local-auth google-auth-library
```

### 2. Login Flow Example

```javascript
// Login component
import { GoogleLogin } from '@react-oauth/google';

function LoginButton() {
  const handleGoogleSuccess = async (credentialResponse) => {
    try {
      const response = await fetch('/api/auth/google', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          token: credentialResponse.credential
        })
      });
      
      const data = await response.json();
      
      // Store tokens
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('refresh_token', data.refresh_token);
      localStorage.setItem('user', JSON.stringify(data.user));
      
      // Redirect to dashboard
      window.location.href = '/dashboard';
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  return (
    <GoogleLogin
      onSuccess={handleGoogleSuccess}
      onError={() => console.log('Login Failed')}
    />
  );
}
```

### 3. API Request Helper

```javascript
// api.js
const API_BASE = 'https://your-backend-url.railway.app/api';

async function apiRequest(endpoint, options = {}) {
  const token = localStorage.getItem('access_token');
  
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(`${API_BASE}${endpoint}`, config);
    
    if (response.status === 401) {
      // Token expired, try to refresh
      const refreshed = await refreshToken();
      if (refreshed) {
        // Retry original request
        config.headers.Authorization = `Bearer ${localStorage.getItem('access_token')}`;
        return fetch(`${API_BASE}${endpoint}`, config);
      } else {
        // Refresh failed, redirect to login
        window.location.href = '/login';
        return;
      }
    }
    
    return response;
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
}

async function refreshToken() {
  const refreshToken = localStorage.getItem('refresh_token');
  if (!refreshToken) return false;

  try {
    const response = await fetch(`${API_BASE}/auth/refresh`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token: refreshToken })
    });

    if (response.ok) {
      const data = await response.json();
      localStorage.setItem('access_token', data.access_token);
      return true;
    }
  } catch (error) {
    console.error('Token refresh failed:', error);
  }
  
  return false;
}
```

## Default Admin User

The system automatically creates a default admin user on first startup:

- **Email:** `admin@library.com`
- **Role:** Admin
- **Note:** This user can only login via Google OAuth if they have a Google account with this email

## Security Features

- **JWT tokens expire after 1 hour** (access tokens)
- **Refresh tokens expire after 30 days**
- **Automatic token cleanup** when users are deactivated
- **Role-based permissions** prevent unauthorized access
- **Google OAuth verification** ensures secure authentication
- **CORS protection** limits frontend origins

## Testing the System

1. **Deploy the updated backend** to Railway
2. **Set up Google OAuth** with your frontend domain
3. **Add environment variables** to Railway
4. **Test login flow** with Google account
5. **Verify role permissions** by trying different operations

The authentication system is now fully integrated and ready for production use!
