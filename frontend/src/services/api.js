// frontend/src/services/api.js

import axios from 'axios';

const API_URL = 'http://localhost:5000/api';  // Adjust if Flask runs on a different host or port

export const predictDisease = async (language, symptoms) => {
    try {
        const response = await axios.post(`${API_URL}/predict`, {
            language,
            symptoms
        });
        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : { error: 'Server Error' };
    }
};
