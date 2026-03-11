"""
Additional models for advanced add-on features
Audit Trail, Ratings, Gamification
"""
from datetime import datetime
from backend.extensions import db


class AuditLog(db.Model):
    """Audit trail - log every significant action"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False)  # login, logout, create_grievance, update_status, etc.
    entity_type = db.Column(db.String(50), nullable=True)  # grievance, user, comment
    entity_id = db.Column(db.Integer, nullable=True)
    details = db.Column(db.Text, nullable=True)  # JSON with change details
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'details': self.details,
            'ip_address': self.ip_address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class GrievanceRating(db.Model):
    """Rating and feedback after grievance resolution"""
    __tablename__ = 'grievance_ratings'
    
    id = db.Column(db.Integer, primary_key=True)
    grievance_id = db.Column(db.Integer, db.ForeignKey('grievances.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    feedback_text = db.Column(db.Text, nullable=True)
    resolution_speed = db.Column(db.Integer, nullable=True)  # 1-5
    officer_helpfulness = db.Column(db.Integer, nullable=True)  # 1-5
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'grievance_id': self.grievance_id,
            'rating': self.rating,
            'feedback_text': self.feedback_text,
            'resolution_speed': self.resolution_speed,
            'officer_helpfulness': self.officer_helpfulness,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
