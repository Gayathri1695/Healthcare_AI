import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

# Ensure directories exist
os.makedirs('dataset', exist_ok=True)
os.makedirs('trained_model', exist_ok=True)

# 1. Generate Synthetic Dataset
symptoms = ['fever', 'cough', 'fatigue', 'headache', 'nausea', 'sore_throat', 'shortness_of_breath', 'chest_pain', 'dizziness']
diseases = ['Flu', 'COVID-19', 'Common Cold', 'Migraine', 'Food Poisoning', 'Heart Condition', 'Anemia']

# Rules for synthetic generation
rules = {
    'Flu': [1, 1, 1, 1, 0, 1, 0, 0, 0],
    'COVID-19': [1, 1, 1, 1, 0, 1, 1, 0, 0],
    'Common Cold': [0, 1, 1, 1, 0, 1, 0, 0, 0],
    'Migraine': [0, 0, 1, 1, 1, 0, 0, 0, 1],
    'Food Poisoning': [1, 0, 1, 1, 1, 0, 0, 0, 1],
    'Heart Condition': [0, 0, 1, 0, 0, 0, 1, 1, 1],
    'Anemia': [0, 0, 1, 1, 0, 0, 1, 0, 1]
}

data = []
labels = []
np.random.seed(42)

for _ in range(2000):
    disease = np.random.choice(diseases)
    base_symptoms = np.array(rules[disease])
    # Add some noise (10% chance to flip a symptom)
    noise = np.random.choice([0, 1], size=len(symptoms), p=[0.9, 0.1])
    noisy_symptoms = np.abs(base_symptoms - noise) # Flip bits
    data.append(noisy_symptoms)
    labels.append(disease)

df = pd.DataFrame(data, columns=symptoms)
df['Disease'] = labels

df.to_csv('dataset/symptoms_dataset.csv', index=False)
print("Generated Synthetic Dataset: dataset/symptoms_dataset.csv")

# 2. Train Models
X = df.drop('Disease', axis=1)
y = df['Disease']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Decision Tree': DecisionTreeClassifier(random_state=42),
    'Naive Bayes': GaussianNB()
}

best_model = None
best_accuracy = 0
best_model_name = ""

print("\nModel Accuracies:")
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"{name}: {acc*100:.2f}%")
    
    if acc > best_accuracy:
        best_accuracy = acc
        best_model = model
        best_model_name = name

print(f"\nBest Model: {best_model_name} with {best_accuracy*100:.2f}% accuracy")

# 3. Save the best model
joblib.dump(best_model, 'trained_model/disease_prediction_model.pkl')
joblib.dump(list(X.columns), 'trained_model/symptoms_list.pkl')
print("Model and symptoms list saved successfully in 'trained_model/'")
