const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const DataStorageMongo = require('./data_storage_mongo');
const FinancialPlannerAI = require('./ai_model');

const app = express();
const port = 5000;

const mongoUri = 'mongodb://localhost:27017'; // Adjust as needed
const dbName = 'financial_planner';

const dataStorage = new DataStorageMongo(mongoUri, dbName);
const aiModel = new FinancialPlannerAI();

dataStorage.connect().catch(err => {
    console.error('Failed to connect to MongoDB:', err);
    process.exit(1);
});

app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'templates')));

// Serve dashboard page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'dashboard.html'));
});

// API to add income
app.post('/api/income', async (req, res) => {
    try {
        const { userId, amount, description, sender } = req.body;
        await dataStorage.addIncome(userId, amount, description, sender);
        res.json({ success: true });
    } catch (err) {
        res.status(500).json({ error: 'Failed to add income' });
    }
});

// API to add outcome
app.post('/api/outcome', async (req, res) => {
    try {
        const { userId, amount, description, sender } = req.body;
        await dataStorage.addOutcome(userId, amount, description, sender);
        res.json({ success: true });
    } catch (err) {
        res.status(500).json({ error: 'Failed to add outcome' });
    }
});
// Continuing from web_app_part1.js

// API to get report
app.get('/api/report/:userId', async (req, res) => {
    try {
        const userId = req.params.userId;
        const report = await dataStorage.getReport(userId);
        res.json(report);
    } catch (err) {
        res.status(500).json({ error: 'Failed to get report' });
    }
});

// API to add budget
app.post('/api/budget', async (req, res) => {
    try {
        const { userId, category, amount, period } = req.body;
        await dataStorage.addBudget(userId, category, amount, period);
        res.json({ success: true });
    } catch (err) {
        res.status(500).json({ error: 'Failed to add budget' });
    }
});

// API to get budgets
app.get('/api/budgets/:userId', async (req, res) => {
    try {
        const userId = req.params.userId;
        const budgets = await dataStorage.getBudgets(userId);
        res.json(budgets);
    } catch (err) {
        res.status(500).json({ error: 'Failed to get budgets' });
    }
});

// API to add goal
app.post('/api/goal', async (req, res) => {
    try {
        const { userId, name, targetAmount } = req.body;
        await dataStorage.addGoal(userId, name, targetAmount);
        res.json({ success: true });
    } catch (err) {
        res.status(500).json({ error: 'Failed to add goal' });
    }
});

// API to get goals
app.get('/api/goals/:userId', async (req, res) => {
    try {
        const userId = req.params.userId;
        const goals = await dataStorage.getGoals(userId);
        res.json(goals);
    } catch (err) {
        res.status(500).json({ error: 'Failed to get goals' });
    }
});

// API to generate AI response
app.post('/api/ai', async (req, res) => {
    try {
        const { text } = req.body;
        const response = await aiModel.generateResponse(text);
        res.json({ response });
    } catch (err) {
        res.status(500).json({ error: 'Failed to generate AI response' });
    }
});

app.listen(port, () => {
    console.log(`Web app listening at http://localhost:${port}`);
});
