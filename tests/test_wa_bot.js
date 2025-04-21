const { describe, it, expect, beforeAll } = require('@jest/globals');
const axios = require('axios');
const FinancialPlannerAI = require('../ai_model');

describe('WhatsApp Bot AI Integration', () => {
    let aiModel;

    beforeAll(() => {
        aiModel = new FinancialPlannerAI();
    });

    it('should generate a response for a simple text', async () => {
        const response = await aiModel.generateResponse('Halo, saya ingin menambah pemasukan 10000');
        expect(typeof response).toBe('string');
        expect(response.length).toBeGreaterThan(0);
    });

    it('should handle empty input gracefully', async () => {
        const response = await aiModel.generateResponse('');
        expect(typeof response).toBe('string');
    });
});

describe('Web API Endpoints', () => {
    const apiBaseUrl = 'http://localhost:5000/api';
    const userId = 1;

    it('should add income successfully', async () => {
        const res = await axios.post(`${apiBaseUrl}/income`, {
            userId,
            amount: 10000,
            description: 'Test income',
            sender: 'test_sender'
        });
        expect(res.data.success).toBe(true);
    });

    it('should get report successfully', async () => {
        const res = await axios.get(`${apiBaseUrl}/report/${userId}`);
        expect(res.data).toHaveProperty('total_income');
        expect(res.data).toHaveProperty('total_outcome');
        expect(res.data).toHaveProperty('balance');
    });
});
