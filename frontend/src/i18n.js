// frontend/src/i18n.js

import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
    en: {
        translation: {
            "Disease Predictor": "Disease Predictor",
            "Choose your language": "Choose your language",
            "Please type your symptoms (comma-separated)": "Please type your symptoms (comma-separated)",
            "e.g., fever, cough": "e.g., fever, cough",
            "Predict Disease": "Predict Disease",
            "Predicting...": "Predicting...",
            "Predicted Disease": "Predicted Disease",
            "Precautions": "Precautions",
            "An error occurred.": "An error occurred.",
            // Add more translations as needed
        }
    },
    fr: {
        translation: {
            "Disease Predictor": "Prédicteur de Maladies",
            "Choose your language": "Choisissez votre langue",
            "Please type your symptoms (comma-separated)": "Veuillez saisir vos symptômes (séparés par des virgules)",
            "e.g., fever, cough": "par exemple, fièvre, toux",
            "Predict Disease": "Prédire la maladie",
            "Predicting...": "Prédiction en cours...",
            "Predicted Disease": "Maladie Prédite",
            "Precautions": "Précautions",
            "An error occurred.": "Une erreur est survenue.",
            // Add more translations as needed
        }
    },
    ar: {
        translation: {
            "Disease Predictor": "مُتنبئ الأمراض",
            "Choose your language": "اختر لغتك",
            "Please type your symptoms (comma-separated)": "يرجى كتابة الأعراض مفصولة بفواصل",
            "e.g., fever, cough": "على سبيل المثال، حمى، سعال",
            "Predict Disease": "تنبؤ المرض",
            "Predicting...": "جاري التنبؤ...",
            "Predicted Disease": "المرض المتوقع",
            "Precautions": "الاحتياطات",
            "An error occurred.": "حدث خطأ ما.",
            // Add more translations as needed
        }
    }
};

i18n
    .use(initReactI18next)
    .init({
        resources,
        lng: 'en', // default language
        keySeparator: false,
        interpolation: {
            escapeValue: false
        }
    });

export default i18n;
