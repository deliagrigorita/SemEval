import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import re

def load_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def preprocess_data(df):
    # Filter out the "neutral" emotion
    df = df[df['emotion'].isin(['Anger', 'Disgust', 'Fear', 'Joy', 'Sadness', 'Surprise'])]
    return df

def train_naive_bayes(X_train, y_train):
    vectorizer = CountVectorizer()
    X_train_counts = vectorizer.fit_transform(X_train)
    clf = MultinomialNB().fit(X_train_counts, y_train)
    return clf, vectorizer

def extract_emotion_cause_pairs(model, vectorizer, X_test, y_test):
    X_test_counts = vectorizer.transform(X_test)
    predicted = model.predict(X_test_counts)

    emotion_cause_pairs = []

    for i, (emotion, text) in enumerate(zip(predicted, X_test)):
        cause_spans = re.findall(r'\bI am gonna go get one of those job things\b', text)  # Adjust the pattern as needed
        for cause_span in cause_spans:
            pair = (f'{i+1}_{emotion.lower()}', f'{i+1}_{cause_span}')
            emotion_cause_pairs.append(pair)

    return emotion_cause_pairs
def main():
    # Load data
    data = load_data('C:\\Users\\40736\\OneDrive\\Desktop\\SemEval\\train.json')
    
    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame([item for conversation in data for item in conversation['conversation']])

    # Preprocess data
    df = preprocess_data(df)

    # Check if the dataset is large enough for splitting
    if len(df) < 2:
        print("Dataset is too small to split. Adjust the dataset or test_size.")
        return

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(df['text'], df['emotion'], test_size=0.2, random_state=42)

    # Train the model
    clf, vectorizer = train_naive_bayes(X_train, y_train)

    # Test the model and extract emotion-cause pairs
    emotion_cause_pairs = extract_emotion_cause_pairs(clf, vectorizer, X_test, y_test)

    # Print the emotion-cause pairs
    print(emotion_cause_pairs)

if __name__ == "__main__":
    main()
