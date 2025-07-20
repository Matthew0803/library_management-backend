from src.models.user import db
from datetime import datetime
from enum import Enum

class UserRole(Enum):
    ADMIN = "admin"
    LIBRARIAN = "librarian"
    MEMBER = "member"

class Permission(Enum):
    # Book permissions
    CREATE_BOOK = "create_book"
    UPDATE_BOOK = "update_book"
    DELETE_BOOK = "delete_book"
    VIEW_BOOK = "view_book"
    
    # User management permissions
    MANAGE_USERS = "manage_users"
    VIEW_USERS = "view_users"
    
    # Library operations
    CHECKOUT_BOOK = "checkout_book"
    CHECKIN_BOOK = "checkin_book"
    VIEW_LIBRARY_STATS = "view_library_stats"

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    google_id = db.Column(db.String(100), unique=True, nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True)
    role = db.Column(db.Enum(UserRole), default=UserRole.MEMBER, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'profile_picture': self.profile_picture,
            'role': self.role.value,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    def has_permission(self, permission: Permission) -> bool:
        """Check if user has a specific permission based on their role"""
        role_permissions = {
            UserRole.ADMIN: [
                Permission.CREATE_BOOK, Permission.UPDATE_BOOK, Permission.DELETE_BOOK, Permission.VIEW_BOOK,
                Permission.MANAGE_USERS, Permission.VIEW_USERS,
                Permission.CHECKOUT_BOOK, Permission.CHECKIN_BOOK, Permission.VIEW_LIBRARY_STATS
            ],
            UserRole.LIBRARIAN: [
                Permission.CREATE_BOOK, Permission.UPDATE_BOOK, Permission.VIEW_BOOK,
                Permission.VIEW_USERS,
                Permission.CHECKOUT_BOOK, Permission.CHECKIN_BOOK, Permission.VIEW_LIBRARY_STATS
            ],
            UserRole.MEMBER: [
                Permission.VIEW_BOOK,
                Permission.CHECKOUT_BOOK, Permission.CHECKIN_BOOK
            ]
        }
        
        return permission in role_permissions.get(self.role, [])
    
    def update_last_login(self):
        """Update the last login timestamp"""
        self.last_login = datetime.utcnow()
        db.session.commit()

class RefreshToken(db.Model):
    __tablename__ = 'refresh_tokens'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_revoked = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('refresh_tokens', lazy=True))
    
    def is_valid(self):
        """Check if the refresh token is still valid"""
        return not self.is_revoked and self.expires_at > datetime.utcnow()
    
    def revoke(self):
        """Revoke the refresh token"""
        self.is_revoked = True
        db.session.commit()
