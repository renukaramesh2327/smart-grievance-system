"""
Comment Escalation Service
Handles automatic escalation of citizen comments when officers don't respond in time
"""
from datetime import datetime
from backend.models import GrievanceComment, Grievance, User, Notification
from backend.extensions import db
from backend.services.email_service import EmailService

# Role hierarchy for escalation (role_level -> role_name)
ROLE_HIERARCHY = {
    1: 'FIELD_OFFICER',
    2: 'SECTION_OFFICER',
    3: 'DEPARTMENT_HEAD',
    4: 'DISTRICT_HEAD',
    5: 'STATE_HEAD',
    6: 'ADMIN'
}

def get_superior_officer(current_officer, grievance):
    """
    Get the superior officer in the hierarchy for escalation
    
    Args:
        current_officer: User object of current officer
        grievance: Grievance object
    
    Returns:
        User object of superior officer or None
    """
    if not current_officer:
        return None
    
    # Get current role level from grievance
    current_level = grievance.current_role_level
    
    # Get next level in hierarchy
    next_level = current_level + 1
    
    if next_level > 6:  # Already at ADMIN level
        return None
    
    next_role = ROLE_HIERARCHY.get(next_level)
    
    if not next_role:
        return None
    
    # Find officer at next level in same department (prefer higher role_level when set)
    # Hierarchy: Field(1) -> Section(2) -> DeptHead(3) -> District(4) -> State(5) -> Admin(6)
    superior = None
    if next_level <= 5:
        superior = User.query.filter(
            User.role == 'OFFICER',
            User.department == grievance.assigned_department,
            User.id != current_officer.id,
            User.role_level > 0,
            User.role_level >= next_level
        ).order_by(User.role_level.asc()).first()
    
    # Fallback: any officer in same department
    if not superior:
        superior = User.query.filter_by(
            role='OFFICER',
            department=grievance.assigned_department
        ).filter(User.id != current_officer.id).first()
    
    # If no officer in department, escalate to admin
    if not superior:
        superior = User.query.filter_by(role='ADMIN').first()
    
    return superior


def check_and_escalate_comments():
    """
    Check all citizen comments that haven't been responded to
    and escalate to superior if deadline passed
    
    This should be run periodically (e.g., every hour via cron job or scheduler)
    """
    now = datetime.utcnow()
    
    # Find all citizen comments that:
    # 1. Have a response deadline
    # 2. Deadline has passed
    # 3. Haven't been escalated yet
    # 4. Haven't received a response from officer
    
    overdue_comments = GrievanceComment.query.filter(
        GrievanceComment.user_role == 'CITIZEN',
        GrievanceComment.response_deadline.isnot(None),
        GrievanceComment.response_deadline < now,
        GrievanceComment.escalated == False
    ).all()
    
    escalated_count = 0
    
    for comment in overdue_comments:
        # Check if officer has responded after this comment
        grievance = Grievance.query.get(comment.grievance_id)
        
        if not grievance:
            continue
        
        # Check if there's an officer response after this citizen comment
        officer_response = GrievanceComment.query.filter(
            GrievanceComment.grievance_id == comment.grievance_id,
            GrievanceComment.created_at > comment.created_at,
            GrievanceComment.user_role.in_(['OFFICER', 'ADMIN'])
        ).first()
        
        if officer_response:
            # Officer has responded, mark as handled
            comment.escalated = True  # Mark as handled (no escalation needed)
            continue
        
        # No response from officer - ESCALATE!
        current_officer = User.query.get(comment.notified_officer_id)
        
        if not current_officer:
            continue
        
        superior = get_superior_officer(current_officer, grievance)
        
        if superior:
            # Mark comment as escalated
            comment.escalated = True
            comment.escalated_at = now
            comment.escalated_to_officer_id = superior.id
            
            # Send email to superior
            EmailService.send_email(
                superior.email,
                f'⚠️ ESCALATED: Comment on Grievance #{grievance.id} - No Response from {current_officer.name}',
                f"""
Dear {superior.name},

This is an escalation alert. A citizen comment on Grievance #{grievance.id} has not been responded to by {current_officer.name} within the required timeframe.

Citizen's Comment:
"{comment.comment_text}"

Comment was sent: {comment.notification_sent_at.strftime('%Y-%m-%d %H:%M')}
Response deadline: {comment.response_deadline.strftime('%Y-%m-%d %H:%M')}

Please review and take necessary action immediately.

View grievance: http://localhost:8000/track.html?id={grievance.id}

Best regards,
Smart Grievance System
                """
            )
            
            # Create in-app notification for superior
            notification = Notification(
                user_id=superior.id,
                title=f'⚠️ Escalated: Grievance #{grievance.id}',
                message=f'Comment from citizen not responded by {current_officer.name}. Requires immediate attention.',
                notification_type='escalation',
                related_grievance_id=grievance.id
            )
            db.session.add(notification)
            
            # Notify the original officer about escalation
            EmailService.send_email(
                current_officer.email,
                f'⚠️ Your case has been escalated - Grievance #{grievance.id}',
                f"""
Dear {current_officer.name},

Your assigned grievance #{grievance.id} has been escalated to {superior.name} due to no response within the required 24-hour timeframe.

Please coordinate with your superior and respond promptly to citizen comments in the future.

View grievance: http://localhost:8000/track.html?id={grievance.id}

Best regards,
Smart Grievance System
                """
            )
            
            escalated_count += 1
    
    # Commit all changes
    if escalated_count > 0:
        db.session.commit()
        print(f"✓ Escalated {escalated_count} overdue comments")
    
    return escalated_count


def escalate_comment_manually(comment_id):
    """
    Manually escalate a specific comment
    Used when admin wants to force escalation
    
    Args:
        comment_id: ID of the comment to escalate
    
    Returns:
        dict with success status and message
    """
    comment = GrievanceComment.query.get(comment_id)
    
    if not comment:
        return {'success': False, 'message': 'Comment not found'}
    
    if comment.user_role != 'CITIZEN':
        return {'success': False, 'message': 'Only citizen comments can be escalated'}
    
    if comment.escalated:
        return {'success': False, 'message': 'Comment already escalated'}
    
    grievance = Grievance.query.get(comment.grievance_id)
    
    if not grievance:
        return {'success': False, 'message': 'Grievance not found'}
    
    current_officer = User.query.get(comment.notified_officer_id)
    
    if not current_officer:
        return {'success': False, 'message': 'No officer assigned'}
    
    superior = get_superior_officer(current_officer, grievance)
    
    if not superior:
        return {'success': False, 'message': 'No superior officer found for escalation'}
    
    # Mark as escalated
    comment.escalated = True
    comment.escalated_at = datetime.utcnow()
    comment.escalated_to_officer_id = superior.id
    
    # Send notifications
    EmailService.send_email(
        superior.email,
        f'⚠️ MANUALLY ESCALATED: Grievance #{grievance.id}',
        f"""
Dear {superior.name},

A comment on Grievance #{grievance.id} has been manually escalated to you.

Citizen's Comment:
"{comment.comment_text}"

Please review and take action.

View grievance: http://localhost:8000/track.html?id={grievance.id}

Best regards,
Smart Grievance System
        """
    )
    
    db.session.commit()
    
    return {
        'success': True,
        'message': f'Comment escalated to {superior.name}',
        'escalated_to': superior.name
    }
