# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from thefuzz import fuzz, process
from googletrans import Translator
from disease_model import DiseasePredictor

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize DiseasePredictor
predictor = DiseasePredictor()

@app.route('/api/predict', methods=['POST'])
def predict_disease():
    data = request.json
    user_language = data.get('language', 'english').lower()
    symptoms_input = data.get('symptoms', '')

    # Validate language
    if user_language not in ['english', 'french', 'arabic', 'عربي']:
        user_language = 'english'
    
    if user_language == 'عربي':
        user_language = 'arabic'
    
    # Translate symptoms to English if necessary
    translated_symptoms = predictor.translate_to_english(symptoms_input, user_language) if user_language != 'english' else symptoms_input
    
    # Normalize symptoms
    normalized_symptoms = predictor.normalize_symptom_input(translated_symptoms, predictor.all_symptoms)
    
    if not normalized_symptoms:
        return jsonify({'error': 'No valid symptoms provided.'}), 400
    
    # Predict disease
    predicted_disease = predictor.predict_disease(normalized_symptoms)
    
    # Retrieve precautions
    precautions = predictor.get_precautions(predicted_disease)
    
    # Translate results if necessary
    if user_language != 'english':
        predicted_disease = predictor.translate_from_english(predicted_disease, user_language)
        precautions = [predictor.translate_from_english(p, user_language) for p in precautions]
    
    response = {
        'predicted_disease': predicted_disease,
        'precautions': precautions
    }
    
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
 
