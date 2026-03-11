from flask import Blueprint, request, jsonify
from datetime import datetime
import json
from backend.models import Grievance, GrievanceUpdate, GrievanceComment, User, FraudReport, Notification
from backend.extensions import db
from backend.routes.auth import get_current_user_from_token
from backend.services.classifier import classifier
from backend.services.email_service import EmailService
from backend.services.ai_image_detector import AIImageDetector
from backend.services.comment_escalation import check_and_escalate_comments, escalate_comment_manually
from backend.services.audit_service import log_audit
from backend.security import require_firewall, SecurityFirewall, SecurityLogger

grievances_bp = Blueprint('grievances', __name__)

# Departments that REQUIRE images (physical/infrastructure issues)
DEPARTMENTS_REQUIRING_IMAGES = {
    'Water Supply', 'Electricity', 'Sanitation & Solid Waste',
    'Sewerage & Drainage', 'Roads & Potholes', 'Streetlights',
    'Traffic', 'Public Health', 'Food Safety', 'Environment',
    'Telecom / Network'
}

# Departments where images are OPTIONAL (administrative/document issues)
DEPARTMENTS_OPTIONAL_IMAGES = {
    'Police', 'Cyber Crime', 'Education', 'Land & Revenue',
    'Ration Card / PDS', 'RTO / Transport'
}

def does_department_require_images(department):
    """Check if a department requires mandatory images"""
    return department in DEPARTMENTS_REQUIRING_IMAGES

@grievances_bp.route('/predict-department', methods=['POST'])
def predict_department():
    """
    Predict department for a complaint text (for dynamic UI updates)
    Required: complaint_text
    """
    try:
        user = get_current_user_from_token()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        
        data = request.get_json()
        complaint_text = data.get('complaint_text')
        
        if not complaint_text:
            return jsonify({'error': 'Complaint text is required'}), 400
        
        # Predict department
        predicted_department = classifier.predict(complaint_text)
        
        # Check if images are required
        images_required = does_department_require_images(predicted_department)
        
        return jsonify({
            'department': predicted_department,
            'images_required': images_required
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@grievances_bp.route('/submit', methods=['POST'])
@require_firewall(max_requests=20, window_minutes=60)  # Max 20 grievances per hour
def submit_grievance():
    """
    Submit a new grievance
    Required: complaint_text
    Optional: location
    """
    try:
        user = get_current_user_from_token()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        
        data = request.get_json()
        complaint_text = data.get('complaint_text')
        location = data.get('location', '')
        images = data.get('images', [])
        
        if not complaint_text or len(complaint_text.strip()) < 20:
            return jsonify({'error': 'Complaint text must be at least 20 characters'}), 400
        
        if not location or len(location.strip()) < 10:
            return jsonify({'error': 'Please provide a detailed location'}), 400
        
        # Predict department using ML first
        predicted_department = classifier.predict(complaint_text)
        
        # CONDITIONAL: Validate images based on department type
        images_required = does_department_require_images(predicted_department)
        
        if images_required and (not images or len(images) == 0):
            return jsonify({
                'error': f'At least 1 image is mandatory for {predicted_department} complaints. Visual evidence is required to verify and process this type of complaint.'
            }), 400
        
        if images and len(images) > 5:
            return jsonify({'error': 'Maximum 5 images allowed'}), 400
        
        # AI-GENERATED IMAGE DETECTION (Anti-Fraud Measure)
        ai_image_detected = False
        ai_detection_confidence = 0.0
        ai_detection_details = None
        
        if images and len(images) > 0:
            ai_detection_result = AIImageDetector.batch_detect(images)
            
            if ai_detection_result['ai_detected_count'] > 0:
                # AI-generated images detected
                ai_images = [r for r in ai_detection_result['results'] if r['is_ai_generated']]
                
                # Get highest confidence detection
                highest_confidence = max(ai_images, key=lambda x: x['confidence'])
                
                if highest_confidence['confidence'] >= 85:
                    # Very high confidence AI detection - REJECT with helpful message
                    return jsonify({
                        'error': 'AI-Generated Image Detected',
                        'message': f'Image #{highest_confidence["image_index"]} appears to be created by AI software (Confidence: {highest_confidence["confidence"]}%).\n\n'
                                   f'Reason: {highest_confidence["reasons"][0] if highest_confidence["reasons"] else "AI generation signatures found in image metadata"}\n\n'
                                   f'Please upload REAL PHOTOS taken with your phone or camera showing the actual issue. '
                                   f'Officers will visit the site to verify, so authentic photos are required.',
                        'image_index': highest_confidence['image_index'],
                        'confidence': highest_confidence['confidence'],
                        'ai_detection': True,
                        'action_required': 'Please remove the AI-generated image and upload a real photo of the complaint location.'
                    }), 400
                elif highest_confidence['confidence'] >= 60:
                    # Medium confidence - FLAG for officer verification
                    print(f"⚠️  FLAGGED: Possible AI-generated image in complaint (confidence: {highest_confidence['confidence']}%)")
                    ai_image_detected = True
                    ai_detection_confidence = highest_confidence['confidence']
                    ai_detection_details = json.dumps({
                        'image_index': highest_confidence['image_index'],
                        'confidence': highest_confidence['confidence'],
                        'reasons': highest_confidence['reasons'],
                        'warnings': highest_confidence['warnings'],
                        'note': 'Flagged for officer verification during site visit'
                    })
        
        # Get complainant info from user profile
        complainant_dob = user.date_of_birth
        complainant_gender = user.gender
        
        # Store images as JSON
        images_json = json.dumps(images) if images else None
        
        # Create grievance
        grievance = Grievance(
            user_id=user.id,
            complaint_text=complaint_text,
            predicted_department=predicted_department,
            assigned_department=predicted_department,
            status='Received',
            location=location,
            images=images_json,
            complainant_dob=complainant_dob,
            complainant_gender=complainant_gender,
            ai_image_detected=ai_image_detected,
            ai_detection_confidence=ai_detection_confidence,
            ai_detection_details=ai_detection_details
        )
        
        db.session.add(grievance)
        db.session.flush()  # Get the grievance ID
        
        # Create first update - Received
        update1 = GrievanceUpdate(
            grievance_id=grievance.id,
            status='Received',
            message='Your complaint has been received and is being processed.',
            updated_by_role='SYSTEM',
            updated_by_name='Smart Grievance System'
        )
        db.session.add(update1)
        
        # Create second update - Assigned to Department
        update2 = GrievanceUpdate(
            grievance_id=grievance.id,
            status='Assigned to Department',
            message=f'Your complaint has been assigned to {predicted_department} department for review.',
            updated_by_role='SYSTEM',
            updated_by_name='Smart Grievance System'
        )
        db.session.add(update2)
        
        # Update grievance status
        grievance.status = 'Assigned to Department'
        
        db.session.commit()
        
        # Send email notification
        EmailService.send_grievance_notification(
            user.email,
            grievance.id,
            predicted_department,
            'Assigned to Department',
            f'Your complaint has been assigned to {predicted_department} department.'
        )
        
        log_audit(user.id, 'create_grievance', 'grievance', grievance.id, json.dumps({'department': predicted_department}))
        
        return jsonify({
            'message': 'Grievance submitted successfully',
            'grievance_id': grievance.id,
            'department': predicted_department,
            'status': grievance.status
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@grievances_bp.route('/my-grievances', methods=['GET'])
def get_my_grievances():
    """
    Get all grievances for current user
    """
    try:
        user = get_current_user_from_token()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        
        grievances = Grievance.query.filter_by(user_id=user.id).order_by(Grievance.created_at.desc()).all()
        
        return jsonify({
            'grievances': [g.to_dict() for g in grievances]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@grievances_bp.route('/<int:grievance_id>', methods=['GET'])
def get_grievance(grievance_id):
    """
    Get grievance details with timeline
    """
    try:
        user = get_current_user_from_token()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        
        grievance = Grievance.query.get(grievance_id)
        
        if not grievance:
            return jsonify({'error': 'Grievance not found'}), 404
        
        # Check authorization
        if user.role == 'CITIZEN' and grievance.user_id != user.id:
            return jsonify({'error': 'Unauthorized to view this grievance'}), 403
        
        if user.role == 'OFFICER' and grievance.assigned_department != user.department:
            return jsonify({'error': 'Unauthorized to view this grievance'}), 403
        
        include_officer = user.role in ['OFFICER', 'ADMIN']
        return jsonify({
            'grievance': grievance.to_dict(include_updates=True, include_comments=True, include_officer=include_officer)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@grievances_bp.route('/department/<department>', methods=['GET'])
def get_department_grievances(department):
    """
    Get all grievances for a department (Officer only)
    """
    try:
        user = get_current_user_from_token()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        
        if user.role not in ['OFFICER', 'ADMIN']:
            return jsonify({'error': 'Only officers can access this endpoint'}), 403
        
        # Officers can only see their department
        if user.role == 'OFFICER' and user.department != department:
            return jsonify({'error': 'Unauthorized to view this department'}), 403
        
        grievances = Grievance.query.filter_by(
            assigned_department=department
        ).order_by(Grievance.created_at.desc()).all()
        
        return jsonify({
            'grievances': [g.to_dict() for g in grievances]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@grievances_bp.route('/<int:grievance_id>/update', methods=['POST'])
def update_grievance(grievance_id):
    """
    Update grievance status (Officer/Admin only)
    Required: status, message
    """
    try:
        user = get_current_user_from_token()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        
        if user.role not in ['OFFICER', 'ADMIN']:
            return jsonify({'error': 'Only officers can update grievances'}), 403
        
        data = request.get_json()
        new_status = data.get('status')
        message = data.get('message')
        
        if not new_status or not message:
            return jsonify({'error': 'status and message are required'}), 400
        
        # Valid statuses
        valid_statuses = [
            'Received',
            'Assigned to Department',
            'Under Progress',
            'Investigation',
            'Reviewed',
            'Resolved',
            'Closed'
        ]
        
        if new_status not in valid_statuses:
            return jsonify({'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'}), 400
        
        grievance = Grievance.query.get(grievance_id)
        
        if not grievance:
            return jsonify({'error': 'Grievance not found'}), 404
        
        # Check authorization
        if user.role == 'OFFICER' and grievance.assigned_department != user.department:
            return jsonify({'error': 'Unauthorized to update this grievance'}), 403
        
        # Store old status for notification
        old_status = grievance.status
        
        # Create update entry
        update = GrievanceUpdate(
            grievance_id=grievance.id,
            status=new_status,
            message=message,
            updated_by_role=user.role,
            updated_by_name=user.name
        )
        db.session.add(update)
        
        # Update grievance status
        grievance.status = new_status
        grievance.updated_at = datetime.utcnow()
        
        # Assign officer if status is "Assigned to Department" and not already assigned
        if new_status == 'Assigned to Department' and not grievance.assigned_officer_id:
            grievance.assigned_officer_id = user.id
        
        db.session.commit()
        
        # Send email notification to citizen with detailed update
        citizen = User.query.get(grievance.user_id)
        if citizen:
            EmailService.send_status_update_notification(
                user_email=citizen.email,
                user_name=citizen.name,
                grievance_id=grievance.id,
                old_status=old_status,
                new_status=new_status,
                update_message=message,
                department=grievance.assigned_department,
                officer_name=user.name
            )
        
        log_audit(user.id, 'update_grievance', 'grievance', grievance_id, json.dumps({'old_status': old_status, 'new_status': new_status}))
        
        return jsonify({
            'message': 'Grievance updated successfully',
            'grievance': grievance.to_dict(include_updates=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@grievances_bp.route('/<int:grievance_id>/comments', methods=['GET'])
def get_comments(grievance_id):
    """
    Get all comments for a grievance
    """
    try:
        user = get_current_user_from_token()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        
        grievance = Grievance.query.get(grievance_id)
        
        if not grievance:
            return jsonify({'error': 'Grievance not found'}), 404
        
        # Check authorization
        if user.role == 'CITIZEN' and grievance.user_id != user.id:
            return jsonify({'error': 'Unauthorized to view this grievance'}), 403
        
        if user.role == 'OFFICER' and grievance.assigned_department != user.department:
            return jsonify({'error': 'Unauthorized to view this grievance'}), 403
        
        comments = GrievanceComment.query.filter_by(
            grievance_id=grievance_id
        ).order_by(GrievanceComment.created_at.asc()).all()
        
        return jsonify({
            'comments': [comment.to_dict() for comment in comments]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@grievances_bp.route('/<int:grievance_id>/comments', methods=['POST'])
def add_comment(grievance_id):
    """
    Add a comment to a grievance (Citizen or Officer)
    Required: comment_text
    """
    try:
        user = get_current_user_from_token()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        
        data = request.get_json()
        comment_text = data.get('comment_text')
        
        if not comment_text or len(comment_text.strip()) < 5:
            return jsonify({'error': 'Comment must be at least 5 characters'}), 400
        
        grievance = Grievance.query.get(grievance_id)
        
        if not grievance:
            return jsonify({'error': 'Grievance not found'}), 404
        
        # Check authorization
        if user.role == 'CITIZEN' and grievance.user_id != user.id:
            return jsonify({'error': 'Unauthorized to comment on this grievance'}), 403
        
        if user.role == 'OFFICER' and grievance.assigned_department != user.department:
            return jsonify({'error': 'Unauthorized to comment on this grievance'}), 403
        
        # Create comment
        comment = GrievanceComment(
            grievance_id=grievance_id,
            user_id=user.id,
            comment_text=comment_text,
            user_role=user.role,
            user_name=user.name
        )
        
        db.session.add(comment)
        
        # Send email notification to the appropriate party
        if user.role == 'CITIZEN':
            # Notify ONLY the currently assigned officer (not all officers)
            if grievance.assigned_officer_id:
                assigned_officer = User.query.get(grievance.assigned_officer_id)
                
                if assigned_officer:
                    # Track notification for escalation
                    from datetime import timedelta
                    comment.notified_officer_id = assigned_officer.id
                    comment.notification_sent_at = datetime.utcnow()
                    comment.response_deadline = datetime.utcnow() + timedelta(hours=24)  # 24 hours to respond
                    
                    EmailService.send_email(
                        assigned_officer.email,
                        f'🔔 New Comment on Grievance #{grievance_id} - Response Required',
                        f"""
Dear {assigned_officer.name},

A citizen has added a new comment on Grievance #{grievance_id} assigned to you:

"{comment_text}"

⚠️ Please respond within 24 hours to avoid escalation to your superior.

View and respond at: http://localhost:8000/track.html?id={grievance_id}

Best regards,
Smart Grievance System
                        """
                    )
                    
                    # Create in-app notification
                    notification = Notification(
                        user_id=assigned_officer.id,
                        title=f'New Comment on Grievance #{grievance_id}',
                        message=f'Citizen has commented: "{comment_text[:100]}..." - Response required within 24 hours.',
                        notification_type='comment',
                        related_grievance_id=grievance_id
                    )
                    db.session.add(notification)
            else:
                # If no specific officer assigned, notify department head
                dept_head = User.query.filter_by(
                    department=grievance.assigned_department,
                    role='OFFICER'
                ).order_by(User.id.asc()).first()  # Get first officer as fallback
                
                if dept_head:
                    comment.notified_officer_id = dept_head.id
                    comment.notification_sent_at = datetime.utcnow()
                    
                    EmailService.send_email(
                        dept_head.email,
                        f'New Comment on Grievance #{grievance_id}',
                        f"""
Dear {dept_head.name},

A citizen has added a comment on an unassigned grievance #{grievance_id}:

"{comment_text}"

View at: http://localhost:8000/track.html?id={grievance_id}

Best regards,
Smart Grievance System
                        """
                    )
        else:
            # Notify citizen
            citizen = User.query.get(grievance.user_id)
            if citizen:
                EmailService.send_email(
                    citizen.email,
                    f'New Response on Your Grievance #{grievance_id}',
                    f"""
Dear {citizen.name},

{user.name} from {grievance.assigned_department} department has responded to your grievance:

"{comment_text}"

View and respond at: http://localhost:5000/track.html?id={grievance_id}

Best regards,
Smart Grievance System
                    """
                )
        
        return jsonify({
            'message': 'Comment added successfully',
            'comment': comment.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@grievances_bp.route('/<int:grievance_id>/report-fraud', methods=['POST'])
def report_fraud(grievance_id):
    """
    Report a grievance as fraudulent (Officer only)
    Officers can report complaints after site visit verification
    """
    try:
        user = get_current_user_from_token()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        
        if user.role != 'OFFICER':
            return jsonify({'error': 'Only officers can report fraudulent complaints'}), 403
        
        data = request.get_json()
        fraud_type = data.get('fraud_type')
        description = data.get('description')
        site_visit_notes = data.get('site_visit_notes', '')
        evidence = data.get('evidence', '')
        
        if not fraud_type or not description:
            return jsonify({'error': 'fraud_type and description are required'}), 400
        
        # Valid fraud types
        valid_fraud_types = [
            'false_complaint',
            'fake_images',
            'wrong_location',
            'exaggerated',
            'duplicate',
            'malicious'
        ]
        
        if fraud_type not in valid_fraud_types:
            return jsonify({'error': f'Invalid fraud_type. Must be one of: {", ".join(valid_fraud_types)}'}), 400
        
        grievance = Grievance.query.get(grievance_id)
        if not grievance:
            return jsonify({'error': 'Grievance not found'}), 404
        
        # Check if officer is assigned to this grievance's department
        if grievance.assigned_department != user.department:
            return jsonify({'error': 'You can only report fraud for grievances in your department'}), 403
        
        # Check if already reported
        existing_report = FraudReport.query.filter_by(
            grievance_id=grievance_id,
            reported_by_officer_id=user.id
        ).first()
        
        if existing_report:
            return jsonify({'error': 'You have already reported this grievance as fraudulent'}), 400
        
        # Create fraud report
        fraud_report = FraudReport(
            grievance_id=grievance_id,
            reported_by_officer_id=user.id,
            complainant_user_id=grievance.user_id,
            fraud_type=fraud_type,
            description=description,
            site_visit_notes=site_visit_notes,
            evidence=evidence,
            status='Pending'
        )
        db.session.add(fraud_report)
        
        # Update grievance status
        grievance.status = 'Under Investigation - Fraud Reported'
        grievance.updated_at = datetime.utcnow()
        
        # Create update entry
        update = GrievanceUpdate(
            grievance_id=grievance_id,
            status='Under Investigation - Fraud Reported',
            message=f'Officer {user.name} has reported this complaint as potentially fraudulent after site visit. Admin review pending.',
            updated_by_role='OFFICER',
            updated_by_name=user.name
        )
        db.session.add(update)
        
        # Notify admin
        admins = User.query.filter_by(role='ADMIN').all()
        for admin in admins:
            admin_notification = Notification(
                user_id=admin.id,
                title=f'Fraud Report - Grievance #{grievance_id}',
                message=f'Officer {user.name} reported grievance #{grievance_id} as {fraud_type.replace("_", " ")}. Immediate review required.',
                notification_type='fraud_report',
                related_grievance_id=grievance_id,
                is_read=False
            )
            db.session.add(admin_notification)
        
        # Notify complainant (warning)
        complainant = User.query.get(grievance.user_id)
        if complainant:
            complainant_notification = Notification(
                user_id=complainant.id,
                title=f'Complaint Under Review - Grievance #{grievance_id}',
                message=f'Your complaint is under investigation for verification. An officer visited the site and raised concerns. Admin will review and contact you if needed.',
                notification_type='fraud_warning',
                related_grievance_id=grievance_id,
                is_read=False
            )
            db.session.add(complainant_notification)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Fraud report submitted successfully. Admin will review.',
            'fraud_report_id': fraud_report.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@grievances_bp.route('/fraud-reports', methods=['GET'])
def get_fraud_reports():
    """
    Get fraud reports (Admin only)
    """
    try:
        user = get_current_user_from_token()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        
        if user.role != 'ADMIN':
            return jsonify({'error': 'Admin access required'}), 403
        
        reports = FraudReport.query.order_by(FraudReport.created_at.desc()).all()
        
        reports_data = []
        for report in reports:
            report_dict = report.to_dict()
            
            # Add officer details
            officer = User.query.get(report.reported_by_officer_id)
            if officer:
                report_dict['officer_name'] = officer.name
                report_dict['officer_department'] = officer.department
            
            # Add complainant details
            complainant = User.query.get(report.complainant_user_id)
            if complainant:
                report_dict['complainant_name'] = complainant.name
                report_dict['complainant_email'] = complainant.email
                report_dict['complainant_warnings'] = complainant.fraud_warnings
                report_dict['complainant_suspended'] = complainant.account_suspended
            
            # Add grievance details
            grievance = Grievance.query.get(report.grievance_id)
            if grievance:
                report_dict['grievance_text'] = grievance.complaint_text[:200]
                report_dict['grievance_department'] = grievance.assigned_department
            
            reports_data.append(report_dict)
        
        return jsonify({
            'fraud_reports': reports_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@grievances_bp.route('/fraud-reports/<int:report_id>/action', methods=['POST'])
def take_fraud_action(report_id):
    """
    Take action on fraud report (Admin only)
    """
    try:
        user = get_current_user_from_token()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        
        if user.role != 'ADMIN':
            return jsonify({'error': 'Admin access required'}), 403
        
        data = request.get_json()
        action = data.get('action')  # 'verify', 'dismiss', 'warn', 'suspend'
        admin_notes = data.get('admin_notes', '')
        
        if not action:
            return jsonify({'error': 'action is required'}), 400
        
        report = FraudReport.query.get(report_id)
        if not report:
            return jsonify({'error': 'Fraud report not found'}), 404
        
        complainant = User.query.get(report.complainant_user_id)
        if not complainant:
            return jsonify({'error': 'Complainant not found'}), 404
        
        if action == 'verify':
            # Fraud verified - issue warning
            report.status = 'Verified'
            report.action_taken = 'Warning Issued'
            complainant.fraud_warnings += 1
            
            # Notify complainant
            notification = Notification(
                user_id=complainant.id,
                title='Warning: Fraudulent Complaint Verified',
                message=f'Your complaint (Grievance #{report.grievance_id}) has been verified as fraudulent. This is warning #{complainant.fraud_warnings}. Repeated fraudulent complaints will result in account suspension.',
                notification_type='fraud_verified',
                related_grievance_id=report.grievance_id,
                is_read=False
            )
            db.session.add(notification)
            
        elif action == 'suspend':
            # Suspend account
            report.status = 'Verified'
            report.action_taken = 'Account Suspended'
            complainant.fraud_warnings += 1
            complainant.account_suspended = True
            complainant.suspension_reason = f'Multiple fraudulent complaints. Latest: Grievance #{report.grievance_id}'
            
            # Notify complainant
            notification = Notification(
                user_id=complainant.id,
                title='Account Suspended - Fraudulent Activity',
                message=f'Your account has been suspended due to repeated fraudulent complaints. Contact admin for appeal.',
                notification_type='account_suspended',
                related_grievance_id=report.grievance_id,
                is_read=False
            )
            db.session.add(notification)
            
        elif action == 'dismiss':
            # Fraud report dismissed - complaint was genuine
            report.status = 'Dismissed'
            report.action_taken = 'Report Dismissed - Complaint Genuine'
            
        else:
            return jsonify({'error': 'Invalid action'}), 400
        
        report.admin_notes = admin_notes
        report.reviewed_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': f'Action taken successfully: {action}',
            'complainant_warnings': complainant.fraud_warnings,
            'account_suspended': complainant.account_suspended
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@grievances_bp.route('/check-comment-escalations', methods=['POST'])
def check_comment_escalations():
    """
    Check for overdue comments and escalate them (Admin/System only)
    This endpoint should be called periodically by a cron job or scheduler
    """
    try:
        user = get_current_user_from_token()
        
        # Only admin can manually trigger escalation checks
        if user and user.role != 'ADMIN':
            return jsonify({'error': 'Admin access required'}), 403
        
        # Run escalation check
        escalated_count = check_and_escalate_comments()
        
        return jsonify({
            'message': 'Escalation check completed',
            'escalated_count': escalated_count
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@grievances_bp.route('/comments/<int:comment_id>/escalate', methods=['POST'])
def manually_escalate_comment(comment_id):
    """
    Manually escalate a specific comment (Admin only)
    """
    try:
        user = get_current_user_from_token()
        
        if not user or user.role != 'ADMIN':
            return jsonify({'error': 'Admin access required'}), 403
        
        result = escalate_comment_manually(comment_id)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
