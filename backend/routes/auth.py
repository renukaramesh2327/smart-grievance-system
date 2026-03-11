from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import jwt
import hashlib
from backend.models import User, OTPRequest, FailedLoginAttempt
from backend.extensions import db
from backend.config import Config
from backend.services.otp_service import OTPService
from backend.services.email_service import EmailService
from backend.security import require_firewall, validate_request_data, SecurityFirewall, SecurityLogger
from backend.services.audit_service import log_audit

auth_bp = Blueprint('auth', __name__)

def create_token(user_id):
    """Create JWT token"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + Config.JWT_ACCESS_TOKEN_EXPIRES
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

def verify_token(token):
    """Verify JWT token and return user_id"""
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@auth_bp.route('/register', methods=['POST'])
@require_firewall(max_requests=5, window_minutes=10)  # Max 5 registration attempts per 10 minutes
def register():
    """
    Register a new user
    Required: name, email, phone, password
    Optional: aadhaar_last4, consent
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'password', 'date_of_birth', 'gender']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Validate email
        is_valid_email, normalized_email, email_error = SecurityFirewall.validate_email_address(data['email'])
        if not is_valid_email:
            return jsonify({'error': f'Invalid email: {email_error}'}), 400
        data['email'] = normalized_email
        
        # Validate phone number
        is_valid_phone, phone_error = SecurityFirewall.validate_phone(data['phone'])
        if not is_valid_phone:
            return jsonify({'error': phone_error}), 400
        
        # Validate password strength
        is_strong, password_error = SecurityFirewall.check_password_strength(data['password'])
        if not is_strong:
            return jsonify({'error': password_error}), 400
        
        # Sanitize name input
        is_valid_name, sanitized_name, name_error = SecurityFirewall.validate_input(data['name'], 'name')
        if not is_valid_name:
            SecurityLogger.log_suspicious_activity(request.remote_addr, f"Invalid name input: {name_error}")
            return jsonify({'error': name_error}), 400
        data['name'] = sanitized_name
        
        # Validate phone number format
        phone = data['phone']
        if not phone.isdigit() or len(phone) != 10:
            return jsonify({'error': 'Phone number must be 10 digits'}), 400
        
        # Validate age (must be 18+)
        from datetime import datetime
        try:
            dob = datetime.strptime(data['date_of_birth'], '%Y-%m-%d')
            today = datetime.now()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            
            if age < 18:
                return jsonify({'error': 'You must be at least 18 years old to register'}), 400
            
            if age > 120:
                return jsonify({'error': 'Please enter a valid date of birth'}), 400
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 400
        
        existing_phone = User.query.filter_by(phone=phone).first()
        if existing_phone:
            return jsonify({'error': 'Phone number already registered'}), 400
        
        # Create new user
        user = User(
            name=data['name'],
            email=data['email'],
            phone=phone,
            date_of_birth=data['date_of_birth'],
            gender=data['gender'],
            role='CITIZEN'
        )
        user.set_password(data['password'])
        
        # Handle Aadhaar (optional)
        if data.get('aadhaar_last4'):
            user.aadhaar_last4 = data['aadhaar_last4']
            # Hash full aadhaar if provided (for demo, we only store last 4)
            user.aadhaar_hash = hashlib.sha256(data['aadhaar_last4'].encode()).hexdigest()
        
        db.session.add(user)
        db.session.commit()
        log_audit(user.id, 'register', 'user', user.id)
        return jsonify({
            'message': 'Registration successful. Please verify your email.',
            'user_id': user.id,
            'email': user.email
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/send-otp', methods=['POST'])
@require_firewall(max_requests=10, window_minutes=10)  # Max 10 OTP requests per 10 minutes
def send_otp():
    """
    Send OTP to email or phone
    Required: identifier (email or phone), channel ('email' or 'phone')
    """
    try:
        data = request.get_json()
        identifier = data.get('identifier')
        channel = data.get('channel', 'email')
        
        if not identifier:
            return jsonify({'error': 'identifier is required'}), 400
        
        # Validate identifier
        is_valid, sanitized, error = SecurityFirewall.validate_input(identifier, 'identifier')
        if not is_valid:
            SecurityLogger.log_suspicious_activity(request.remote_addr, f"Invalid OTP identifier: {error}")
            return jsonify({'error': error}), 400
        
        if channel not in ['email', 'phone']:
            return jsonify({'error': 'channel must be email or phone'}), 400
        
        # Generate and send OTP
        otp, error = OTPService.create_otp_request(identifier, channel)
        
        if error:
            return jsonify({'error': error}), 429
        
        return jsonify({
            'message': f'OTP sent to {identifier} via {channel}',
            'demo_mode': Config.DEMO_EMAIL_MODE or Config.DEMO_SMS_MODE,
            'demo_note': 'Check console for OTP in demo mode'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    """
    Verify OTP and mark user as verified
    Required: identifier, otp
    """
    try:
        data = request.get_json()
        identifier = data.get('identifier')
        otp = data.get('otp')
        
        if not identifier or not otp:
            return jsonify({'error': 'identifier and otp are required'}), 400
        
        # Verify OTP
        success, message = OTPService.verify_otp(identifier, otp)
        
        if not success:
            return jsonify({'error': message}), 400
        
        # Find user and mark as verified
        user = User.query.filter_by(email=identifier).first()
        if not user:
            user = User.query.filter_by(phone=identifier).first()
        
        if user:
            if '@' in identifier:
                user.email_verified = True
            else:
                user.phone_verified = True
            db.session.commit()
            
            # Send welcome email
            EmailService.send_welcome_email(user.email, user.name)
        
        return jsonify({'message': message}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

LOGIN_MAX_ATTEMPTS = 3
LOGIN_LOCKOUT_HOURS = 24


@auth_bp.route('/login', methods=['POST'])
@require_firewall(max_requests=10, window_minutes=5)
def login():
    """
    Login user
    Required: email, password
    Server-side lockout: 3 failed attempts = 24-hour lockout per email
    """
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        is_valid_email, normalized_email, email_error = SecurityFirewall.validate_email_address(email)
        if not is_valid_email:
            SecurityLogger.log_authentication_failure(request.remote_addr, email)
            return jsonify({'error': 'Invalid email format'}), 400
        
        attempt = FailedLoginAttempt.query.filter_by(identifier=normalized_email).first()
        if attempt and attempt.lockout_until and datetime.utcnow() < attempt.lockout_until:
            remaining = (attempt.lockout_until - datetime.utcnow()).total_seconds()
            return jsonify({
                'error': 'Account temporarily locked',
                'message': f'Too many failed attempts. Try again in {int(remaining // 3600)} hours.',
                'lockout_until': attempt.lockout_until.isoformat()
            }), 429
        
        user = User.query.filter_by(email=normalized_email).first()
        
        if not user or not user.check_password(password):
            if not attempt:
                attempt = FailedLoginAttempt(identifier=normalized_email, attempt_count=0)
                db.session.add(attempt)
            attempt.attempt_count += 1
            if attempt.attempt_count >= LOGIN_MAX_ATTEMPTS:
                attempt.lockout_until = datetime.utcnow() + timedelta(hours=LOGIN_LOCKOUT_HOURS)
            attempt.updated_at = datetime.utcnow()
            db.session.commit()
            SecurityLogger.log_authentication_failure(request.remote_addr, normalized_email)
            return jsonify({'error': 'Invalid email or password'}), 401
        
        if attempt:
            attempt.attempt_count = 0
            attempt.lockout_until = None
            db.session.commit()
        
        # Check if account is suspended
        if user.account_suspended:
            SecurityLogger.log_blocked_attempt(request.remote_addr, f"Suspended account login attempt: {normalized_email}")
            return jsonify({
                'error': 'Account Suspended',
                'message': f'Your account has been suspended. Reason: {user.suspension_reason}'
            }), 403
        
        # Create token
        token = create_token(user.id)
        log_audit(user.id, 'login', 'user', user.id)
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """
    Initiate password reset process
    Required: email
    """
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        if not user:
            # Don't reveal if user exists or not (security)
            return jsonify({
                'message': 'If this email is registered, you will receive a verification code',
                'email': email
            }), 200
        
        # Send OTP to email
        otp, error = OTPService.create_otp_request(email, 'email')
        
        if error:
            return jsonify({'error': error}), 429
        
        return jsonify({
            'message': 'Verification code sent to your email',
            'email': email,
            'phone_last4': user.phone[-4:] if user.phone else None
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/verify-reset-otp', methods=['POST'])
def verify_reset_otp():
    """
    Verify OTP for password reset
    Required: email, otp
    """
    try:
        data = request.get_json()
        email = data.get('email')
        otp = data.get('otp')
        
        if not email or not otp:
            return jsonify({'error': 'Email and OTP are required'}), 400
        
        # Verify OTP
        success, message = OTPService.verify_otp(email, otp)
        
        if not success:
            return jsonify({'error': message}), 400
        
        # Generate reset token (valid for 15 minutes)
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        reset_token = create_token(user.id, expiry_minutes=15)
        
        return jsonify({
            'message': 'OTP verified successfully',
            'reset_token': reset_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """
    Reset password with verified token
    Required: reset_token, new_password
    """
    try:
        data = request.get_json()
        reset_token = data.get('reset_token')
        new_password = data.get('new_password')
        
        if not reset_token or not new_password:
            return jsonify({'error': 'Reset token and new password are required'}), 400
        
        # Validate password strength
        if len(new_password) < 8:
            return jsonify({'error': 'Password must be at least 8 characters long'}), 400
        
        # Verify reset token
        try:
            payload = jwt.decode(reset_token, Config.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Reset token has expired. Please request a new one.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid reset token'}), 401
        
        # Find user and update password
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user.set_password(new_password)
        db.session.commit()
        
        # Send confirmation email
        EmailService.send_password_reset_confirmation(user.email, user.name)
        
        return jsonify({
            'message': 'Password reset successfully. You can now login with your new password.'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """
    Get current user info from token
    Requires: Authorization header with Bearer token
    """
    try:
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No token provided'}), 401
        
        token = auth_header.split(' ')[1]
        user_id = verify_token(token)
        
        if not user_id:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/profile/update', methods=['PUT'])
def update_profile():
    """
    Update user profile
    Requires: Authorization header with Bearer token
    """
    try:
        user = get_current_user_from_token()
        
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        
        data = request.get_json()
        
        # Update allowed fields
        if 'name' in data:
            user.name = data['name']
        if 'phone' in data:
            user.phone = data['phone']
        if 'profile_photo' in data:
            user.profile_photo = data['profile_photo']
        # Default complaint location (optional)
        if 'address' in data:
            user.address = data['address']
        if 'city' in data:
            user.city = data['city']
        if 'state' in data:
            user.state = data['state']
        if 'pincode' in data:
            user.pincode = data['pincode']
        # Residential address (permanent)
        if 'residential_address' in data:
            user.residential_address = data['residential_address']
        if 'residential_city' in data:
            user.residential_city = data['residential_city']
        if 'residential_state' in data:
            user.residential_state = data['residential_state']
        if 'residential_pincode' in data:
            user.residential_pincode = data['residential_pincode']
        if 'date_of_birth' in data:
            user.date_of_birth = data['date_of_birth']
        if 'gender' in data:
            user.gender = data['gender']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def get_current_user_from_token():
    """
    Helper function to get current user from request token
    Returns: User object or None
    """
    try:
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ')[1]
        user_id = verify_token(token)
        
        if not user_id:
            return None
        
        return User.query.get(user_id)
        
    except:
        return None
