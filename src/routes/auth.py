from flask import Blueprint, request, jsonify, g
from src.services.auth_service import auth_service
from src.models.auth import User, UserRole, Permission
from src.models.user import db
from src.utils.auth_decorators import token_required, permission_required, admin_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/google', methods=['POST'])
def google_login():
    """Login with Google OAuth token"""
    try:
        data = request.json
        google_token = data.get('token')
        
        if not google_token:
            return jsonify({'error': 'Google token is required'}), 400
        
        # Verify Google token
        user_info = auth_service.verify_google_token(google_token)
        if not user_info:
            return jsonify({'error': 'Invalid Google token'}), 401
        
        # Create or update user
        user = auth_service.create_or_update_user(user_info)
        
        # Generate tokens
        access_token = auth_service.generate_access_token(user)
        refresh_token = auth_service.generate_refresh_token(user)
        
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/refresh', methods=['POST'])
def refresh_token():
    """Refresh access token using refresh token"""
    try:
        data = request.json
        refresh_token_string = data.get('refresh_token')
        
        if not refresh_token_string:
            return jsonify({'error': 'Refresh token is required'}), 400
        
        result = auth_service.refresh_access_token(refresh_token_string)
        if not result:
            return jsonify({'error': 'Invalid or expired refresh token'}), 401
        
        return jsonify({
            'access_token': result['access_token'],
            'user': result['user'].to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/logout', methods=['POST'])
@token_required
def logout():
    """Logout user and revoke refresh token"""
    try:
        data = request.json
        refresh_token_string = data.get('refresh_token')
        
        if refresh_token_string:
            auth_service.revoke_refresh_token(refresh_token_string)
        
        return jsonify({'message': 'Logged out successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/logout-all', methods=['POST'])
@token_required
def logout_all():
    """Logout user from all devices"""
    try:
        user = g.current_user
        auth_service.revoke_all_user_tokens(user.id)
        
        return jsonify({'message': 'Logged out from all devices'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/me', methods=['GET'])
@token_required
def get_current_user():
    """Get current user information"""
    user = g.current_user
    return jsonify({
        'user': user.to_dict(),
        'permissions': [perm.value for perm in Permission if user.has_permission(perm)]
    }), 200

@auth_bp.route('/auth/users', methods=['GET'])
@permission_required(Permission.VIEW_USERS)
def get_users():
    """Get all users (requires VIEW_USERS permission)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        users = User.query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'users': [user.to_dict() for user in users.items],
            'total': users.total,
            'pages': users.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/users/<int:user_id>/role', methods=['PUT'])
@permission_required(Permission.MANAGE_USERS)
def update_user_role(user_id):
    """Update user role (requires MANAGE_USERS permission)"""
    try:
        data = request.json
        new_role = data.get('role')
        
        if not new_role:
            return jsonify({'error': 'Role is required'}), 400
        
        # Validate role
        try:
            role_enum = UserRole(new_role)
        except ValueError:
            return jsonify({'error': 'Invalid role'}), 400
        
        user = User.query.get_or_404(user_id)
        user.role = role_enum
        db.session.commit()
        
        return jsonify({
            'message': 'User role updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/users/<int:user_id>/status', methods=['PUT'])
@admin_required
def update_user_status(user_id):
    """Activate/deactivate user (admin only)"""
    try:
        data = request.json
        is_active = data.get('is_active')
        
        if is_active is None:
            return jsonify({'error': 'is_active field is required'}), 400
        
        user = User.query.get_or_404(user_id)
        user.is_active = bool(is_active)
        db.session.commit()
        
        # Revoke all tokens if deactivating user
        if not is_active:
            auth_service.revoke_all_user_tokens(user_id)
        
        return jsonify({
            'message': f'User {"activated" if is_active else "deactivated"} successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/roles', methods=['GET'])
@token_required
def get_roles():
    """Get all available roles"""
    roles = [{'value': role.value, 'name': role.name} for role in UserRole]
    return jsonify({'roles': roles}), 200

@auth_bp.route('/auth/permissions', methods=['GET'])
@token_required
def get_permissions():
    """Get all available permissions"""
    permissions = [{'value': perm.value, 'name': perm.name} for perm in Permission]
    return jsonify({'permissions': permissions}), 200
