import joblib
import os
from backend.config import Config
from backend.utils.text_clean import clean_text

class GrievanceClassifier:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.loaded = False
    
    def load_model(self):
        """Load the trained model and vectorizer"""
        try:
            if os.path.exists(Config.MODEL_PATH) and os.path.exists(Config.VECTORIZER_PATH):
                self.model = joblib.load(Config.MODEL_PATH)
                self.vectorizer = joblib.load(Config.VECTORIZER_PATH)
                self.loaded = True
                print("✓ ML Model and Vectorizer loaded successfully")
            else:
                print("⚠ ML Model not found. Please run ml/train.py first")
                self.loaded = False
        except Exception as e:
            print(f"✗ Error loading ML model: {e}")
            self.loaded = False
    
    def predict(self, complaint_text):
        """
        Predict department for a complaint
        Returns: department name or 'General' if model not loaded
        """
        if not self.loaded:
            print("⚠ Model not loaded, returning default department")
            return "General"
        
        try:
            # Clean the text
            cleaned_text = clean_text(complaint_text)
            
            # Vectorize
            text_vectorized = self.vectorizer.transform([cleaned_text])
            
            # Predict
            prediction = self.model.predict(text_vectorized)[0]
            
            return prediction
        except Exception as e:
            print(f"✗ Error predicting department: {e}")
            return "General"

# Global classifier instance
classifier = GrievanceClassifier()
