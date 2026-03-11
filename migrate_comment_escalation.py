"""
Database migration script to add comment escalation fields
Run this once to update the database schema
"""
from backend.app import create_app
from backend.extensions import db

app = create_app()

with app.app_context():
    # Add new columns to grievance_comments table
    with db.engine.connect() as conn:
        try:
            # Check if columns exist before adding
            result = conn.execute(db.text("PRAGMA table_info(grievance_comments)"))
            existing_columns = [row[1] for row in result]
            
            if 'notified_officer_id' not in existing_columns:
                print("Adding notified_officer_id column...")
                conn.execute(db.text("""
                    ALTER TABLE grievance_comments 
                    ADD COLUMN notified_officer_id INTEGER
                """))
                conn.commit()
                print("✓ Added notified_officer_id")
            
            if 'notification_sent_at' not in existing_columns:
                print("Adding notification_sent_at column...")
                conn.execute(db.text("""
                    ALTER TABLE grievance_comments 
                    ADD COLUMN notification_sent_at DATETIME
                """))
                conn.commit()
                print("✓ Added notification_sent_at")
            
            if 'response_deadline' not in existing_columns:
                print("Adding response_deadline column...")
                conn.execute(db.text("""
                    ALTER TABLE grievance_comments 
                    ADD COLUMN response_deadline DATETIME
                """))
                conn.commit()
                print("✓ Added response_deadline")
            
            if 'escalated' not in existing_columns:
                print("Adding escalated column...")
                conn.execute(db.text("""
                    ALTER TABLE grievance_comments 
                    ADD COLUMN escalated BOOLEAN DEFAULT 0
                """))
                conn.commit()
                print("✓ Added escalated")
            
            if 'escalated_at' not in existing_columns:
                print("Adding escalated_at column...")
                conn.execute(db.text("""
                    ALTER TABLE grievance_comments 
                    ADD COLUMN escalated_at DATETIME
                """))
                conn.commit()
                print("✓ Added escalated_at")
            
            if 'escalated_to_officer_id' not in existing_columns:
                print("Adding escalated_to_officer_id column...")
                conn.execute(db.text("""
                    ALTER TABLE grievance_comments 
                    ADD COLUMN escalated_to_officer_id INTEGER
                """))
                conn.commit()
                print("✓ Added escalated_to_officer_id")
            
            print("\n✅ Migration completed successfully!")
            print("Comment escalation tracking is now enabled.")
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            conn.rollback()
