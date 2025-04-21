// AI model integration updated to use local AI inference server

const axios = require('axios');

const LOCAL_AI_API_URL = 'http://localhost:6000/api/ai';

class FinancialPlannerAI {
    constructor() {
        this.apiUrl = LOCAL_AI_API_URL;
    }

    async generateResponse(text) {
        try {
            const response = await axios.post(this.apiUrl, { text });
            if (response.data && response.data.response) {
                return response.data.response;
            } else {
                return "Maaf, saya tidak dapat memahami pesan Anda.";
            }
        } catch (error) {
            console.error('Error calling local AI server:', error);
            return "Maaf, terjadi kesalahan saat memproses pesan Anda.";
        }
    }
}

module.exports = FinancialPlannerAI;
