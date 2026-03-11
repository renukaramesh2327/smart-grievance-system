"""Add-on routes: Public dashboard, Ratings, Audit, Export, QR"""
from flask import Blueprint, jsonify, request, send_file
from datetime import datetime, timedelta
from io import BytesIO
import json
import qrcode
from sqlalchemy import func
from backend.models import Grievance, User
from backend.models_addons import AuditLog, GrievanceRating
from backend.extensions import db
from backend.services.audit_service import log_audit
from backend.routes.auth import get_current_user_from_token

addons_bp = Blueprint('addons', __name__)


@addons_bp.route('/public/stats', methods=['GET'])
def public_stats():
    """Public dashboard - aggregated stats (no auth required)"""
    try:
        total = Grievance.query.count()
        resolved = Grievance.query.filter(Grievance.status.in_(['Resolved', 'Closed'])).count()
        pending = total - resolved
        dept_counts = db.session.query(
            Grievance.assigned_department,
            func.count(Grievance.id)
        ).group_by(Grievance.assigned_department).all()
        
        # Avg resolution time (days) for resolved grievances
        resolved_grievances = Grievance.query.filter(
            Grievance.status.in_(['Resolved', 'Closed']),
            Grievance.created_at.isnot(None),
            Grievance.updated_at.isnot(None)
        ).all()
        total_days = sum((g.updated_at - g.created_at).total_seconds() / 86400 for g in resolved_grievances)
        avg_resolution_days = round(total_days / len(resolved_grievances), 1) if resolved_grievances else 0
        
        return jsonify({
            'total_grievances': total,
            'resolved': resolved,
            'pending': pending,
            'resolution_rate': round(resolved / total * 100, 1) if total else 0,
            'avg_resolution_days': avg_resolution_days,
            'by_department': {d: c for d, c in dept_counts},
            'updated_at': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@addons_bp.route('/grievances/<int:grievance_id>/rate', methods=['POST'])
def submit_rating(grievance_id):
    """Submit rating for resolved grievance"""
    try:
        user = get_current_user_from_token()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        
        data = request.get_json()
        rating = data.get('rating', 0)
        feedback_text = data.get('feedback_text', '')
        
        if not 1 <= rating <= 5:
            return jsonify({'error': 'Rating must be 1-5'}), 400
        
        grievance = Grievance.query.get(grievance_id)
        if not grievance:
            return jsonify({'error': 'Grievance not found'}), 404
        if grievance.user_id != user.id:
            return jsonify({'error': 'Can only rate your own grievances'}), 403
        if grievance.status not in ['Resolved', 'Closed']:
            return jsonify({'error': 'Can only rate resolved grievances'}), 400
        
        existing = GrievanceRating.query.filter_by(grievance_id=grievance_id, user_id=user.id).first()
        if existing:
            existing.rating = rating
            existing.feedback_text = feedback_text
            existing.resolution_speed = data.get('resolution_speed')
            existing.officer_helpfulness = data.get('officer_helpfulness')
        else:
            r = GrievanceRating(
                grievance_id=grievance_id,
                user_id=user.id,
                rating=rating,
                feedback_text=feedback_text,
                resolution_speed=data.get('resolution_speed'),
                officer_helpfulness=data.get('officer_helpfulness')
            )
            db.session.add(r)
        
        db.session.commit()
        log_audit(user.id, 'rate_grievance', 'grievance', grievance_id, json.dumps({'rating': rating}))
        return jsonify({'message': 'Thank you for your feedback!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@addons_bp.route('/grievances/<int:grievance_id>/rating', methods=['GET'])
def get_rating(grievance_id):
    """Get rating for a grievance"""
    try:
        user = get_current_user_from_token()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        
        r = GrievanceRating.query.filter_by(grievance_id=grievance_id, user_id=user.id).first()
        if not r:
            return jsonify({'rating': None}), 200
        return jsonify(r.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@addons_bp.route('/grievances/<int:grievance_id>/qr', methods=['GET'])
def get_qr_code(grievance_id):
    """Generate QR code for grievance tracking"""
    try:
        grievance = Grievance.query.get(grievance_id)
        if not grievance:
            return jsonify({'error': 'Not found'}), 404
        
        base_url = request.host_url.rstrip('/')
        track_url = f"{base_url}/track.html?id={grievance_id}"
        
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(track_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#1e40af", back_color="white")
        
        buf = BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@addons_bp.route('/admin/audit/export', methods=['GET'])
def export_audit():
    """Export audit log (Admin only)"""
    try:
        user = get_current_user_from_token()
        if not user or user.role != 'ADMIN':
            return jsonify({'error': 'Admin required'}), 403
        
        days = int(request.args.get('days', 7))
        since = datetime.utcnow() - timedelta(days=days)
        logs = AuditLog.query.filter(AuditLog.created_at >= since).order_by(AuditLog.created_at.desc()).limit(5000).all()
        
        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
            from reportlab.lib.styles import getSampleStyleSheet
            
            buf = BytesIO()
            doc = SimpleDocTemplate(buf, pagesize=letter)
            styles = getSampleStyleSheet()
            elements = []
            elements.append(Paragraph("Audit Log Report", styles['Title']))
            elements.append(Paragraph(f"Period: Last {days} days", styles['Normal']))
            
            data = [['Time', 'User ID', 'Action', 'Entity', 'IP']]
            for log in logs:
                data.append([
                    log.created_at.strftime('%Y-%m-%d %H:%M') if log.created_at else '',
                    str(log.user_id or ''),
                    log.action or '',
                    f"{log.entity_type or ''}#{log.entity_id or ''}",
                    log.ip_address or ''
                ])
            
            t = Table(data)
            t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey), ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke)]))
            elements.append(t)
            doc.build(elements)
            buf.seek(0)
            return send_file(buf, mimetype='application/pdf', as_attachment=True, download_name=f'audit_log_{days}days.pdf')
        except ImportError:
            return jsonify({'logs': [l.to_dict() for l in logs]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@addons_bp.route('/admin/export/grievances', methods=['GET'])
def export_grievances():
    """Export grievances to Excel (Admin/Officer)"""
    try:
        user = get_current_user_from_token()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        
        from openpyxl import Workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Grievances"
        ws.append(['ID', 'Department', 'Status', 'Location', 'Created', 'Updated'])
        
        if user.role == 'ADMIN':
            grievances = Grievance.query.order_by(Grievance.created_at.desc()).limit(1000).all()
        else:
            grievances = Grievance.query.filter_by(assigned_department=user.department).order_by(Grievance.created_at.desc()).limit(500).all()
        
        for g in grievances:
            ws.append([g.id, g.assigned_department, g.status, g.location or '', 
                      g.created_at.strftime('%Y-%m-%d') if g.created_at else '',
                      g.updated_at.strftime('%Y-%m-%d') if g.updated_at else ''])
        
        buf = BytesIO()
        wb.save(buf)
        buf.seek(0)
        log_audit(user.id, 'export_grievances', details=json.dumps({'count': len(grievances)}))
        return send_file(buf, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                        as_attachment=True, download_name=f'grievances_export_{datetime.now().strftime("%Y%m%d")}.xlsx')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
