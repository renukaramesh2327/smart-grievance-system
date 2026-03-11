"""
Background Scheduler for periodic tasks
- Comment escalation checks: every hour
- ML model retraining: every 7 days (configurable)
"""
import os
import threading
import time
from datetime import datetime
from backend.services.comment_escalation import check_and_escalate_comments
from backend.services.model_retrain import retrain_model

# Retrain every N hours (168 = 7 days). Set RETRAIN_INTERVAL_HOURS=24 for daily.
RETRAIN_INTERVAL_HOURS = int(os.environ.get('RETRAIN_INTERVAL_HOURS', '168'))


class BackgroundScheduler:
    """Simple background scheduler for running periodic tasks"""
    
    def __init__(self, app=None):
        self.app = app
        self.running = False
        self.thread = None
        self._hours_since_retrain = 0
    
    def init_app(self, app):
        """Initialize with Flask app context"""
        self.app = app
    
    def start(self):
        """Start the background scheduler"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        print("✓ Background scheduler started - Comment escalations every hour, model retrain every 7 days")
    
    def stop(self):
        """Stop the background scheduler"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
    
    def _run_scheduler(self):
        """Main scheduler loop - runs every hour"""
        while self.running:
            try:
                # Wait for 1 hour (3600 seconds)
                time.sleep(3600)
                
                if not self.running:
                    break
                
                if not self.app:
                    continue
                
                with self.app.app_context():
                    # Comment escalation (every hour)
                    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running comment escalation check...")
                    escalated_count = check_and_escalate_comments()
                    if escalated_count > 0:
                        print(f"✓ Escalated {escalated_count} overdue comments")
                    else:
                        print("✓ No comments need escalation")
                    
                    # Model retraining (every RETRAIN_INTERVAL_HOURS)
                    self._hours_since_retrain += 1
                    if self._hours_since_retrain >= RETRAIN_INTERVAL_HOURS:
                        self._hours_since_retrain = 0
                        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running scheduled ML model retraining...")
                        success, msg = retrain_model()
                        if success:
                            print(f"✓ {msg}")
                        else:
                            print(f"❌ Retrain failed: {msg}")
                
            except Exception as e:
                print(f"❌ Scheduler error: {e}")
                continue

# Global scheduler instance
scheduler = BackgroundScheduler()
