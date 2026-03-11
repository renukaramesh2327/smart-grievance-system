#!/usr/bin/env python3
"""
Database Migration Script
Adds new profile fields to User model
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.extensions import db
from backend.models import User, Grievance, OTPRequest, GrievanceUpdate, GrievanceComment
from backend.config import Config

# Initialize Flask app
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    print("🔄 Updating database schema...")
    
    # SQLite doesn't support ALTER TABLE ADD COLUMN for all types
    # We need to use raw SQL for adding columns
    from sqlalchemy import text, inspect
    
    inspector = inspect(db.engine)
    
    # Check existing columns in users table
    existing_columns = [col['name'] for col in inspector.get_columns('users')]
    
    # New columns to add
    new_user_columns = {
        'office_number': 'VARCHAR(50)',
        'office_email': 'VARCHAR(120)',
        'office_location': 'VARCHAR(500)',
        'office_building': 'VARCHAR(200)',
        'designation': 'VARCHAR(100)',
        'profile_photo': 'TEXT',
        'address': 'VARCHAR(500)',
        'city': 'VARCHAR(100)',
        'state': 'VARCHAR(100)',
        'pincode': 'VARCHAR(10)',
        'residential_address': 'TEXT',
        'residential_city': 'VARCHAR(100)',
        'residential_state': 'VARCHAR(100)',
        'residential_pincode': 'VARCHAR(10)',
        'date_of_birth': 'VARCHAR(20)',
        'gender': 'VARCHAR(20)',
        'role_level': 'INTEGER DEFAULT 0',
        'ward': 'VARCHAR(100)',
        'district': 'VARCHAR(100)',
        'jurisdiction_type': 'VARCHAR(50)'
    }
    
    print("\n📋 Adding new columns to User table:")
    for col_name, col_type in new_user_columns.items():
        if col_name not in existing_columns:
            try:
                db.session.execute(text(f'ALTER TABLE users ADD COLUMN {col_name} {col_type}'))
                db.session.commit()
                print(f"  ✓ Added {col_name}")
            except Exception as e:
                print(f"  ⚠ {col_name} - {str(e)}")
        else:
            print(f"  ✓ {col_name} (already exists)")
    
    # Check grievances table
    grievance_columns = [col['name'] for col in inspector.get_columns('grievances')]
    
    new_grievance_columns = {
        'assigned_officer_id': 'INTEGER',
        'complainant_dob': 'VARCHAR(20)',
        'complainant_gender': 'VARCHAR(50)',
        'images': 'TEXT',
        'is_flagged': 'BOOLEAN DEFAULT 0',
        'moderation_score': 'INTEGER DEFAULT 0',
        'current_role_level': 'INTEGER',
        'escalation_level': 'INTEGER DEFAULT 0',
        'ward': 'VARCHAR(100)',
        'district': 'VARCHAR(100)',
        'sla_hours': 'INTEGER',
        'sla_deadline': 'DATETIME',
        'sla_breached': 'BOOLEAN DEFAULT 0',
        'last_action_at': 'DATETIME',
        'moderation_severity': 'VARCHAR(20)',
        'moderation_flags': 'TEXT',
        'ai_image_detected': 'BOOLEAN DEFAULT 0',
        'ai_detection_confidence': 'REAL DEFAULT 0.0',
        'ai_detection_details': 'TEXT'
    }
    
    print("\n📋 Adding new columns to Grievance table:")
    for col_name, col_type in new_grievance_columns.items():
        if col_name not in grievance_columns:
            try:
                db.session.execute(text(f'ALTER TABLE grievances ADD COLUMN {col_name} {col_type}'))
                db.session.commit()
                print(f"  ✓ Added {col_name}")
            except Exception as e:
                print(f"  ⚠ {col_name} - {str(e)}")
        else:
            print(f"  ✓ {col_name} (already exists)")
    
    print("\n✅ Database schema updated successfully!")
    
    # --- Add Fraud Tracking Fields to User Table ---
    print("\n📋 Adding fraud tracking fields to User table:")
    existing_columns = [col['name'] for col in inspector.get_columns('users')]
    
    fraud_tracking_columns = {
        'fraud_warnings': 'INTEGER DEFAULT 0',
        'account_suspended': 'BOOLEAN DEFAULT 0',
        'suspension_reason': 'TEXT'
    }
    
    for col_name, col_type in fraud_tracking_columns.items():
        if col_name not in existing_columns:
            try:
                with db.engine.connect() as connection:
                    connection.execute(db.text(f'ALTER TABLE users ADD COLUMN {col_name} {col_type}'))
                    connection.commit()
                print(f"  ✓ Added {col_name}")
            except Exception as e:
                print(f"  ⚠ {col_name} - {str(e)}")
        else:
            print(f"  ✓ {col_name} (already exists)")
    
    # --- Create Notifications Table ---
    # Re-fetch existing tables after updates
    existing_tables = inspector.get_table_names()
    
    if 'notifications' not in existing_tables:
        print("\n📋 Creating Notifications table:")
        try:
            with db.engine.connect() as connection:
                connection.execute(db.text('''
                    CREATE TABLE notifications (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        title VARCHAR(200) NOT NULL,
                        message TEXT NOT NULL,
                        notification_type VARCHAR(50) NOT NULL,
                        related_grievance_id INTEGER,
                        is_read BOOLEAN DEFAULT 0,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id),
                        FOREIGN KEY (related_grievance_id) REFERENCES grievances(id)
                    )
                '''))
                connection.commit()
            print("  ✓ Notifications table created")
        except Exception as e:
            print(f"  ⚠ Error creating notifications table: {str(e)}")
    else:
        print("\n✓ Notifications table already exists")
    
    # --- Create Fraud Reports Table ---
    existing_tables = inspector.get_table_names()
    
    if 'fraud_reports' not in existing_tables:
        print("\n📋 Creating Fraud Reports table:")
        try:
            with db.engine.connect() as connection:
                connection.execute(db.text('''
                    CREATE TABLE fraud_reports (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        grievance_id INTEGER NOT NULL,
                        reported_by_officer_id INTEGER NOT NULL,
                        complainant_user_id INTEGER NOT NULL,
                        fraud_type VARCHAR(50) NOT NULL,
                        description TEXT NOT NULL,
                        evidence TEXT,
                        site_visit_notes TEXT,
                        status VARCHAR(20) DEFAULT 'Pending',
                        action_taken VARCHAR(100),
                        admin_notes TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        reviewed_at DATETIME,
                        FOREIGN KEY (grievance_id) REFERENCES grievances(id),
                        FOREIGN KEY (reported_by_officer_id) REFERENCES users(id),
                        FOREIGN KEY (complainant_user_id) REFERENCES users(id)
                    )
                '''))
                connection.commit()
            print("  ✓ Fraud Reports table created")
        except Exception as e:
            print(f"  ⚠ Error creating fraud_reports table: {str(e)}")
    else:
        print("\n✓ Fraud Reports table already exists")
    
    print("\n✅ Migration complete!")
