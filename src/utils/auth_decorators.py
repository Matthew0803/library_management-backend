from functools import wraps
from flask import request, jsonify, g
from src.services.auth_service import auth_service
from src.models.auth import Permission

def token_required(f):
    """Decorator to require valid JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        # Verify token
        user = auth_service.verify_access_token(token)
        if not user:
            return jsonify({'error': 'Token is invalid or expired'}), 401
        
        # Store user in Flask's g object for use in the route
        g.current_user = user
        return f(*args, **kwargs)
    
    return decorated

def permission_required(permission: Permission):
    """Decorator to require specific permission"""
    def decorator(f):
        @wraps(f)
        @token_required
        def decorated(*args, **kwargs):
            user = g.current_user
            
            if not user.has_permission(permission):
                return jsonify({
                    'error': 'Insufficient permissions',
                    'required_permission': permission.value
                }), 403
            
            return f(*args, **kwargs)
        return decorated
    return decorator

def role_required(*roles):
    """Decorator to require specific user roles"""
    def decorator(f):
        @wraps(f)
        @token_required
        def decorated(*args, **kwargs):
            user = g.current_user
            
            if user.role not in roles:
                return jsonify({
                    'error': 'Insufficient role privileges',
                    'required_roles': [role.value for role in roles],
                    'user_role': user.role.value
                }), 403
            
            return f(*args, **kwargs)
        return decorated
    return decorator

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        user = g.current_user
        
        if user.role.value != 'admin':
            return jsonify({'error': 'Admin privileges required'}), 403
        
        return f(*args, **kwargs)
    return decorated

def optional_auth(f):
    """Decorator that adds user info if token is present, but doesn't require it"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
                user = auth_service.verify_access_token(token)
                g.current_user = user
            except (IndexError, AttributeError):
                g.current_user = None
        else:
            g.current_user = None
        
        return f(*args, **kwargs)
    
    return decorated
