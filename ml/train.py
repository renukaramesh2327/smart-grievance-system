"""
Train the grievance classification model.
Supports: dataset validation, improved vocabulary, multilingual stop words.
"""
import pandas as pd
import joblib
import os
import sys
import warnings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.utils.text_clean import clean_text, get_stop_words

# Config: increased vocabulary for better domain coverage
MAX_FEATURES = 2500
MIN_DF = 1
NGRAM_RANGE = (1, 2)


def validate_dataset(df):
    """
    Validate dataset quality and return (is_valid, warnings_list, errors_list).
    """
    errors = []
    warnings_list = []
    
    # Required columns
    if 'complaint' not in df.columns or 'department' not in df.columns:
        errors.append("Dataset must have 'complaint' and 'department' columns")
        return False, warnings_list, errors
    
    # Remove rows with missing values
    before = len(df)
    df = df.dropna(subset=['complaint', 'department'])
    if len(df) < before:
        warnings_list.append(f"Removed {before - len(df)} rows with missing complaint/department")
    
    # Check minimum samples
    if len(df) < 50:
        errors.append(f"Dataset too small: {len(df)} samples. Need at least 50 for training.")
    
    # Check complaint length
    short_complaints = df['complaint'].str.len() < 10
    if short_complaints.any():
        count = short_complaints.sum()
        warnings_list.append(f"{count} complaints are very short (<10 chars) - may affect quality")
    
    # Check for duplicates
    dupes = df.duplicated(subset=['complaint', 'department']).sum()
    if dupes > 0:
        warnings_list.append(f"{dupes} duplicate complaint-department pairs found")
    
    # Class balance check
    dept_counts = df['department'].value_counts()
    min_samples = dept_counts.min()
    if min_samples < 5:
        warnings_list.append(
            f"Some departments have very few samples (min={min_samples}). "
            "Consider adding more data for: " +
            ", ".join(dept_counts[dept_counts < 5].index.tolist())
        )
    
    # Class imbalance
    max_samples = dept_counts.max()
    if max_samples > min_samples * 5:
        warnings_list.append(
            f"Significant class imbalance: largest class has {max_samples} samples, "
            f"smallest has {min_samples}"
        )
    
    return len(errors) == 0, warnings_list, errors


def train_classifier():
    """Train the grievance classification model."""
    print("=" * 60)
    print("Training Grievance Classification Model")
    print("=" * 60)
    
    # Load dataset
    data_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'data',
        'indian_grievance_dataset.csv'
    )
    
    if not os.path.exists(data_path):
        print(f"✗ Dataset not found at {data_path}")
        return False
    
    df = pd.read_csv(data_path)
    
    # Validate dataset
    print("\n--- Dataset Validation ---")
    is_valid, warnings_list, errors = validate_dataset(df)
    
    for w in warnings_list:
        print(f"⚠ {w}")
    for e in errors:
        print(f"✗ {e}")
    
    if not is_valid:
        print("\n✗ Dataset validation failed. Fix errors before training.")
        return False
    
    df = df.dropna(subset=['complaint', 'department'])
    print(f"✓ Loaded dataset with {len(df)} samples")
    print(f"✓ Departments: {df['department'].nunique()}")
    print("\nDepartment distribution:")
    print(df['department'].value_counts())
    
    # Clean text
    print("\n" + "=" * 60)
    print("Cleaning text (multilingual-aware)...")
    df['cleaned_complaint'] = df['complaint'].apply(clean_text)
    print("✓ Text cleaning completed")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        df['cleaned_complaint'],
        df['department'],
        test_size=0.2,
        random_state=42,
        stratify=df['department']
    )
    
    print(f"✓ Train set: {len(X_train)} samples")
    print(f"✓ Test set: {len(X_test)} samples")
    
    # Create TF-IDF vectorizer with improved settings
    print("\n" + "=" * 60)
    print(f"Creating TF-IDF vectorizer (max_features={MAX_FEATURES}, multilingual stop words)...")
    custom_stop_words = get_stop_words()
    vectorizer = TfidfVectorizer(
        max_features=MAX_FEATURES,
        stop_words=custom_stop_words,
        ngram_range=NGRAM_RANGE,
        min_df=MIN_DF
    )
    
    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)
    print(f"✓ Vocabulary size: {len(vectorizer.vocabulary_)}")
    
    # Train Logistic Regression
    print("\n" + "=" * 60)
    print("Training Logistic Regression model...")
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=FutureWarning)
        model = LogisticRegression(
            max_iter=2000,
            random_state=42,
            solver='lbfgs'
        )
    
    model.fit(X_train_vectorized, y_train)
    print("✓ Model training completed")
    
    # Evaluate
    print("\n" + "=" * 60)
    print("Evaluating model...")
    y_pred = model.predict(X_test_vectorized)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n✓ Accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))
    
    # Save model and vectorizer
    print("\n" + "=" * 60)
    print("Saving model and vectorizer...")
    
    artifacts_dir = os.path.join(os.path.dirname(__file__), 'artifacts')
    os.makedirs(artifacts_dir, exist_ok=True)
    
    model_path = os.path.join(artifacts_dir, 'model.joblib')
    vectorizer_path = os.path.join(artifacts_dir, 'vectorizer.joblib')
    
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)
    
    print(f"✓ Model saved to: {model_path}")
    print(f"✓ Vectorizer saved to: {vectorizer_path}")
    
    # Save training metadata for retraining logic
    metadata_path = os.path.join(artifacts_dir, 'train_metadata.json')
    import json
    metadata = {
        'accuracy': float(accuracy),
        'samples': len(df),
        'departments': int(df['department'].nunique()),
        'vocabulary_size': len(vectorizer.vocabulary_),
    }
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"✓ Metadata saved to: {metadata_path}")
    
    # Test predictions
    print("\n" + "=" * 60)
    print("Testing predictions on sample complaints:")
    print("=" * 60)
    
    test_complaints = [
        "Street lights not working in our area",
        "Water supply is very irregular",
        "Garbage not collected for many days",
        "Road has many potholes",
        "Hospital lacks medicines",
        "Patta document processing delayed",  # Indian term
        "Ration shop dealer overcharging",
    ]
    
    for complaint in test_complaints:
        cleaned = clean_text(complaint)
        vectorized = vectorizer.transform([cleaned])
        prediction = model.predict(vectorized)[0]
        print(f"\nComplaint: {complaint}")
        print(f"Predicted Department: {prediction}")
    
    print("\n" + "=" * 60)
    print("✓ Training completed successfully!")
    print("=" * 60)
    return True


if __name__ == '__main__':
    success = train_classifier()
    sys.exit(0 if success else 1)
