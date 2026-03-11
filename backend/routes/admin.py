from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from sqlalchemy import func
from backend.models import User, Grievance, GrievanceUpdate, Notification
from backend.extensions import db
from backend.routes.auth import get_current_user_from_token
from backend.services.email_service import EmailService
from backend.services.model_retrain import retrain_model, get_retrain_status

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/create-officer', methods=['POST'])
def create_officer():
    """
    Create a new officer account (Admin only)
    Required: name, email, phone, password, department
    """
    try:
        user = get_current_user_from_token()
        if not user or user.role != 'ADMIN':
            return jsonify({'error': 'Admin access required'}), 403
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'password', 'department']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create officer
        officer = User(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            role='OFFICER',
            department=data['department'],
            email_verified=True,  # Auto-verify officers
            phone_verified=True
        )
        officer.set_password(data['password'])
        
        db.session.add(officer)
        db.session.commit()
        
        return jsonify({
            'message': 'Officer created successfully',
            'officer': officer.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/officers', methods=['GET'])
def get_officers():
    """
    Get all officers (Admin only)
    """
    try:
        user = get_current_user_from_token()
        if not user or user.role != 'ADMIN':
            return jsonify({'error': 'Admin access required'}), 403
        
        officers = User.query.filter_by(role='OFFICER').all()
        
        return jsonify({
            'officers': [officer.to_dict() for officer in officers]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users', methods=['GET'])
def get_users():
    """
    Get all users/citizens (Admin only)
    """
    try:
        user = get_current_user_from_token()
        if not user or user.role != 'ADMIN':
            return jsonify({'error': 'Admin access required'}), 403
        
        # Get all citizens
        citizens = User.query.filter_by(role='CITIZEN').all()
        
        # Get grievance count for each citizen
        users_data = []
        for citizen in citizens:
            user_dict = citizen.to_dict()
            grievance_count = Grievance.query.filter_by(user_id=citizen.id).count()
            user_dict['grievance_count'] = grievance_count
            users_data.append(user_dict)
        
        return jsonify({
            'users': users_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/analytics', methods=['GET'])
def get_analytics():
    """
    Get system analytics (Admin only)
    Returns:
    - counts_by_status
    - counts_by_department
    - avg_resolution_time_days
    - total_grievances
    - total_users
    """
    try:
        user = get_current_user_from_token()
        if not user or user.role != 'ADMIN':
            return jsonify({'error': 'Admin access required'}), 403
        
        # Count by status
        status_counts = db.session.query(
            Grievance.status,
            func.count(Grievance.id)
        ).group_by(Grievance.status).all()
        
        counts_by_status = {status: count for status, count in status_counts}
        
        # Count by department
        dept_counts = db.session.query(
            Grievance.assigned_department,
            func.count(Grievance.id)
        ).group_by(Grievance.assigned_department).all()
        
        counts_by_department = {dept: count for dept, count in dept_counts}
        
        # Calculate average resolution time for closed/resolved grievances
        resolved_grievances = Grievance.query.filter(
            Grievance.status.in_(['Resolved', 'Closed'])
        ).all()
        
        total_resolution_time = 0
        resolved_count = 0
        
        for grievance in resolved_grievances:
            if grievance.created_at and grievance.updated_at:
                resolution_time = (grievance.updated_at - grievance.created_at).total_seconds()
                total_resolution_time += resolution_time
                resolved_count += 1
        
        avg_resolution_time_days = 0
        if resolved_count > 0:
            avg_resolution_time_seconds = total_resolution_time / resolved_count
            avg_resolution_time_days = round(avg_resolution_time_seconds / (24 * 3600), 2)
        
        # Total counts
        total_grievances = Grievance.query.count()
        total_users = User.query.filter_by(role='CITIZEN').count()
        total_officers = User.query.filter_by(role='OFFICER').count()
        
        return jsonify({
            'counts_by_status': counts_by_status,
            'counts_by_department': counts_by_department,
            'avg_resolution_time_days': avg_resolution_time_days,
            'total_grievances': total_grievances,
            'total_users': total_users,
            'total_officers': total_officers
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/all-grievances', methods=['GET'])
def get_all_grievances():
    """
    Get all grievances with complete user and officer information (Admin only)
    """
    try:
        user = get_current_user_from_token()
        if not user or user.role != 'ADMIN':
            return jsonify({'error': 'Admin access required'}), 403
        
        # Get query parameters for filtering
        status = request.args.get('status')
        department = request.args.get('department')
        
        query = Grievance.query
        
        if status:
            query = query.filter_by(status=status)
        
        if department:
            query = query.filter_by(assigned_department=department)
        
        grievances = query.order_by(Grievance.created_at.desc()).all()
        
        # Build detailed grievance data with complete user and officer information
        grievances_data = []
        for g in grievances:
            grievance_dict = g.to_dict(include_officer=True)
            
            # Add complete complainant (user) information
            complainant = User.query.get(g.user_id)
            if complainant:
                grievance_dict['complainant'] = {
                    'id': complainant.id,
                    'name': complainant.name,
                    'email': complainant.email,
                    'phone': complainant.phone,
                    'residential_address': complainant.residential_address,
                    'residential_city': complainant.residential_city,
                    'residential_state': complainant.residential_state,
                    'residential_pincode': complainant.residential_pincode,
                    'date_of_birth': complainant.date_of_birth,
                    'gender': complainant.gender,
                    'email_verified': complainant.email_verified,
                    'phone_verified': complainant.phone_verified,
                    'created_at': complainant.created_at.isoformat() if complainant.created_at else None
                }
            
            grievances_data.append(grievance_dict)
        
        return jsonify({
            'grievances': grievances_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/departments', methods=['GET'])
def get_departments():
    """
    Get list of all departments
    """
    try:
        user = get_current_user_from_token()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        
        # Get unique departments from grievances and officers
        dept_from_grievances = db.session.query(Grievance.assigned_department).distinct().all()
        dept_from_officers = db.session.query(User.department).filter(User.role == 'OFFICER').distinct().all()
        
        departments = set()
        for (dept,) in dept_from_grievances:
            if dept:
                departments.add(dept)
        for (dept,) in dept_from_officers:
            if dept:
                departments.add(dept)
        
        return jsonify({
            'departments': sorted(list(departments))
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/assign-officer', methods=['POST'])
def assign_officer():
    """
    Assign an officer to a grievance (Admin only)
    Required: grievance_id, officer_id
    Sends email notification to officer and user
    """
    try:
        user = get_current_user_from_token()
        if not user or user.role != 'ADMIN':
            return jsonify({'error': 'Admin access required'}), 403
        
        data = request.get_json()
        grievance_id = data.get('grievance_id')
        officer_id = data.get('officer_id')
        
        if not grievance_id or not officer_id:
            return jsonify({'error': 'grievance_id and officer_id are required'}), 400
        
        # Get grievance
        grievance = Grievance.query.get(grievance_id)
        if not grievance:
            return jsonify({'error': 'Grievance not found'}), 404
        
        # Get officer
        officer = User.query.get(officer_id)
        if not officer or officer.role != 'OFFICER':
            return jsonify({'error': 'Officer not found'}), 404
        
        # Get citizen
        citizen = User.query.get(grievance.user_id)
        if not citizen:
            return jsonify({'error': 'Citizen not found'}), 404
        
        # Store old officer (if any)
        old_officer_id = grievance.assigned_officer_id
        
        # Assign officer
        grievance.assigned_officer_id = officer_id
        grievance.status = 'Assigned to Department'
        grievance.updated_at = datetime.utcnow()
        
        # Create update entry
        update = GrievanceUpdate(
            grievance_id=grievance.id,
            status='Assigned to Department',
            message=f'Case assigned to Officer {officer.name} ({officer.designation or "Officer"}) by Admin.',
            updated_by_role='ADMIN',
            updated_by_name=user.name
        )
        db.session.add(update)
        
        # Create in-app notification for officer
        officer_notification = Notification(
            user_id=officer_id,
            title=f'🚨 New Case Assigned - Grievance #{grievance.id}',
            message=f'You have been assigned a new case in {grievance.assigned_department} department. Complainant: {citizen.name}. Please review and take action.',
            notification_type='assignment',
            related_grievance_id=grievance.id,
            is_read=False
        )
        db.session.add(officer_notification)
        
        # Create in-app notification for citizen
        citizen_notification = Notification(
            user_id=citizen.id,
            title=f'Officer Assigned - Grievance #{grievance.id}',
            message=f'Your complaint has been assigned to {officer.name} ({officer.designation or "Officer"}) for resolution.',
            notification_type='assignment',
            related_grievance_id=grievance.id,
            is_read=False
        )
        db.session.add(citizen_notification)
        
        db.session.commit()
        
        # Send email notification to officer
        EmailService.send_officer_assignment_notification(
            officer_email=officer.office_email or officer.email,
            officer_name=officer.name,
            grievance_id=grievance.id,
            complaint_text=grievance.complaint_text,
            department=grievance.assigned_department,
            user_name=citizen.name,
            user_phone=citizen.phone
        )
        
        # Send email notification to citizen
        EmailService.send_status_update_notification(
            user_email=citizen.email,
            user_name=citizen.name,
            grievance_id=grievance.id,
            old_status=grievance.status if old_officer_id else 'Received',
            new_status='Assigned to Department',
            update_message=f'Your complaint has been assigned to {officer.name} ({officer.designation or "Officer"}) for resolution.',
            department=grievance.assigned_department,
            officer_name=officer.name
        )
        
        return jsonify({
            'message': 'Officer assigned successfully',
            'grievance': grievance.to_dict(include_officer=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/notifications', methods=['GET'])
def get_notifications():
    """
    Get notifications for the current user
    """
    try:
        user = get_current_user_from_token()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        
        # Get unread count
        unread_count = Notification.query.filter_by(user_id=user.id, is_read=False).count()
        
        # Get all notifications (limit to last 50)
        notifications = Notification.query.filter_by(user_id=user.id)\
            .order_by(Notification.created_at.desc())\
            .limit(50)\
            .all()
        
        return jsonify({
            'unread_count': unread_count,
            'notifications': [n.to_dict() for n in notifications]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/notifications/<int:notification_id>/mark-read', methods=['PUT'])
def mark_notification_read(notification_id):
    """
    Mark a notification as read
    """
    try:
        user = get_current_user_from_token()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        
        notification = Notification.query.get(notification_id)
        if not notification:
            return jsonify({'error': 'Notification not found'}), 404
        
        if notification.user_id != user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        notification.is_read = True
        db.session.commit()
        
        return jsonify({'message': 'Notification marked as read'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/retrain-model', methods=['POST'])
def trigger_retrain():
    """
    Trigger ML model retraining (Admin only).
    Retrains on data/indian_grievance_dataset.csv and reloads the classifier.
    """
    try:
        user = get_current_user_from_token()
        if not user or user.role != 'ADMIN':
            return jsonify({'error': 'Admin access required'}), 403
        
        success, message = retrain_model()
        if success:
            status = get_retrain_status()
            return jsonify({
                'message': message,
                'metadata': status
            }), 200
        return jsonify({'error': message}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/reset-lockout/<email>', methods=['POST'])
def reset_login_lockout(email):
    """Reset login lockout for an email (Admin only)."""
    try:
        user = get_current_user_from_token()
        if not user or user.role != 'ADMIN':
            return jsonify({'error': 'Admin access required'}), 403
        
        from backend.models import FailedLoginAttempt
        attempt = FailedLoginAttempt.query.filter_by(identifier=email).first()
        if attempt:
            attempt.attempt_count = 0
            attempt.lockout_until = None
            db.session.commit()
        
        return jsonify({'message': f'Lockout reset for {email}'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/model-status', methods=['GET'])
def get_model_status():
    """
    Get current ML model training metadata (Admin only).
    """
    try:
        user = get_current_user_from_token()
        if not user or user.role != 'ADMIN':
            return jsonify({'error': 'Admin access required'}), 403
        
        status = get_retrain_status()
        if status:
            return jsonify(status), 200
        return jsonify({'message': 'No training metadata found. Run retrain first.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/notifications/mark-all-read', methods=['PUT'])
def mark_all_notifications_read():
    """
    Mark all notifications as read for current user
    """
    try:
        user = get_current_user_from_token()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        
        Notification.query.filter_by(user_id=user.id, is_read=False).update({'is_read': True})
        db.session.commit()
        
        return jsonify({'message': 'All notifications marked as read'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
