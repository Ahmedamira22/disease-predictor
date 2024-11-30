import React, { useState } from 'react';
import { predictDisease } from './services/api';
import { useTranslation } from 'react-i18next';
import './App.css';

function App() {
    const { t, i18n } = useTranslation();
    const [language, setLanguage] = useState('english');
    const [symptoms, setSymptoms] = useState('');
    const [result, setResult] = useState(null);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleLanguageChange = (e) => {
        setLanguage(e.target.value);
        i18n.changeLanguage(e.target.value === 'english' ? 'en' : e.target.value === 'french' ? 'fr' : 'ar');
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setResult(null);

        try {
            const data = await predictDisease(language, symptoms);
            setResult(data);
        } catch (err) {
            setError(err.error || 'An error occurred.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="App">
            <h1>{t('Disease Predictor')}</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="language">{t('Choose your language')}:</label>
                    <select id="language" value={language} onChange={handleLanguageChange}>
                        <option value="english">English</option>
                        <option value="french">Français</option>
                        <option value="arabic">عربي</option>
                    </select>
                </div>
                <div>
                    <label htmlFor="symptoms">{t('Please type your symptoms (comma-separated)')}:</label>
                    <input
                        type="text"
                        id="symptoms"
                        value={symptoms}
                        onChange={(e) => setSymptoms(e.target.value)}
                        placeholder={t('e.g., fever, cough')}
                        required
                    />
                </div>
                <button type="submit" disabled={loading}>
                    {loading ? t('Predicting...') : t('Predict Disease')}
                </button>
            </form>

            {error && <div className="error">{error}</div>}

            {result && (
                <div className="result">
                    <h2>{t('Predicted Disease')}: {result.predicted_disease}</h2>
                    <h3>{t('Precautions')}:</h3>
                    <ul>
                        {result.precautions.map((precaution, index) => (
                            <li key={index}>{precaution}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}

export default App;
