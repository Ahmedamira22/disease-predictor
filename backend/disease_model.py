# backend/disease_model.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from thefuzz import fuzz, process
from googletrans import Translator

class DiseasePredictor:
    def __init__(self):
        # Load datasets
        self.disease_file_path = 'diseases.csv'  # Ensure this path is correct
        self.precaution_file_path = 'Disease_precaution.csv'
        self.df = pd.read_csv(self.disease_file_path)
        self.precaution_df = pd.read_csv(self.precaution_file_path)
        
        # Extract symptoms
        self.symptom_columns = [col for col in self.df.columns if col.startswith('Symptom_')]
        self.all_symptoms = pd.unique(self.df[self.symptom_columns].values.ravel('K'))
        self.all_symptoms = [symptom.lower() for symptom in self.all_symptoms if pd.notna(symptom)]
        self.all_symptoms.sort()
        
        # Initialize Translator
        self.translator = Translator()
        
        # Precompute disease symptom vectors
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.disease_symptoms = self.df[self.symptom_columns].apply(lambda row: ' '.join(row.dropna().astype(str)), axis=1)
        self.disease_vec = self.vectorizer.fit_transform(self.disease_symptoms)
    
    def translate_to_english(self, text, src_lang):
        try:
            translation = self.translator.translate(text, src=self.get_lang_code(src_lang), dest='en')
            return translation.text
        except Exception as e:
            print(f"Translation error: {e}")
            return text  # Fallback to original text
    
    def translate_from_english(self, text, target_lang):
        try:
            translation = self.translator.translate(text, src='en', dest=self.get_lang_code(target_lang))
            return translation.text
        except Exception as e:
            print(f"Translation error: {e}")
            return text  # Fallback to original text
    
    def get_lang_code(self, language):
        lang_map = {
            'english': 'en',
            'french': 'fr',
            'arabic': 'ar'
        }
        return lang_map.get(language, 'en')
    
    def normalize_symptom_input(self, input_str, symptom_list):
        normalized_input = []
        input_symptoms = input_str.split(",")
    
        for symptom in input_symptoms:
            symptom = symptom.strip().lower()
            
            # Check for exact or fuzzy match
            if symptom in symptom_list:
                normalized_input.append(symptom)
            else:
                best_match = process.extractOne(symptom, symptom_list, scorer=fuzz.ratio)
                if best_match and best_match[1] > 80:
                    normalized_input.append(best_match[0])
        
        return normalized_input
    
    def predict_disease(self, selected_symptoms):
        user_symptoms_str = ' '.join(selected_symptoms)
        user_vec = self.vectorizer.transform([user_symptoms_str])
        cosine_similarities = cosine_similarity(user_vec, self.disease_vec).flatten()
        best_match_idx = cosine_similarities.argmax()
        predicted_disease = self.df.iloc[best_match_idx]['Disease']
        return predicted_disease
    
    def get_precautions(self, disease):
        precaution_row = self.precaution_df[self.precaution_df['Disease'] == disease]
        if not precaution_row.empty:
            precautions = []
            for col in ['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']:
                precaution_value = precaution_row[col].values[0]
                if pd.notna(precaution_value):
                    precautions.append(precaution_value)
            return precautions
        else:
            return []


