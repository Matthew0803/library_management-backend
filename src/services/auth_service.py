import os
import jwt
import secrets
from datetime import datetime, timedelta
from google.auth.transport import requests
from google.oauth2 import id_token
from src.models.auth import User, RefreshToken, UserRole
from src.models.user import db

class AuthService:
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        self.app = app
        self.jwt_secret = app.config.get('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
        self.google_client_id = app.config.get('GOOGLE_CLIENT_ID')
        self.access_token_expires = timedelta(hours=1)
        self.refresh_token_expires = timedelta(days=30)
    
    def verify_google_token(self, token):
        """Verify Google OAuth token and return user info"""
        try:
            # Verify the token with Google
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), self.google_client_id
            )
            
            # Check if the token is from the correct issuer
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            
            return {
                'google_id': idinfo['sub'],
                'email': idinfo['email'],
                'name': idinfo['name'],
                'profile_picture': idinfo.get('picture', '')
            }
        except ValueError as e:
            print(f"Token verification failed: {e}")
            return None
    
    def create_or_update_user(self, user_info):
        """Create a new user or update existing user from Google OAuth"""
        user = User.query.filter_by(email=user_info['email']).first()
        
        if user:
            # Update existing user
            user.name = user_info['name']
            user.profile_picture = user_info['profile_picture']
            user.google_id = user_info['google_id']
            user.updated_at = datetime.utcnow()
        else:
            # Create new user
            user = User(
                email=user_info['email'],
                name=user_info['name'],
                google_id=user_info['google_id'],
                profile_picture=user_info['profile_picture'],
                role=UserRole.MEMBER  # Default role for new users
            )
            db.session.add(user)
        
        user.update_last_login()
        db.session.commit()
        return user
    
    def generate_access_token(self, user):
        """Generate JWT access token"""
        payload = {
            'user_id': user.id,
            'email': user.email,
            'role': user.role.value,
            'exp': datetime.utcnow() + self.access_token_expires,
            'iat': datetime.utcnow(),
            'type': 'access'
        }
        
        return jwt.encode(payload, self.jwt_secret, algorithm='HS256')
    
    def generate_refresh_token(self, user):
        """Generate and store refresh token"""
        # Revoke existing refresh tokens for this user
        RefreshToken.query.filter_by(user_id=user.id, is_revoked=False).update({'is_revoked': True})
        
        # Generate new refresh token
        token_string = secrets.token_urlsafe(64)
        refresh_token = RefreshToken(
            user_id=user.id,
            token=token_string,
            expires_at=datetime.utcnow() + self.refresh_token_expires
        )
        
        db.session.add(refresh_token)
        db.session.commit()
        
        return token_string
    
    def verify_access_token(self, token):
        """Verify JWT access token and return user info"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            
            if payload.get('type') != 'access':
                return None
            
            user = User.query.get(payload['user_id'])
            if not user or not user.is_active:
                return None
            
            return user
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def refresh_access_token(self, refresh_token_string):
        """Generate new access token using refresh token"""
        refresh_token = RefreshToken.query.filter_by(
            token=refresh_token_string,
            is_revoked=False
        ).first()
        
        if not refresh_token or not refresh_token.is_valid():
            return None
        
        user = refresh_token.user
        if not user or not user.is_active:
            return None
        
        # Generate new access token
        access_token = self.generate_access_token(user)
        
        return {
            'access_token': access_token,
            'user': user
        }
    
    def revoke_refresh_token(self, refresh_token_string):
        """Revoke a refresh token"""
        refresh_token = RefreshToken.query.filter_by(token=refresh_token_string).first()
        if refresh_token:
            refresh_token.revoke()
            return True
        return False
    
    def revoke_all_user_tokens(self, user_id):
        """Revoke all refresh tokens for a user"""
        RefreshToken.query.filter_by(user_id=user_id, is_revoked=False).update({'is_revoked': True})
        db.session.commit()

# Global auth service instance
auth_service = AuthService()
