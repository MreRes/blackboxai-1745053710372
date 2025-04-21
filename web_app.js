const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const DataStorage = require('./data_storage');
const FinancialPlannerAI = require('./ai_model');

const app = express();
const port = 5000;

const dataStorage = new DataStorage();
const aiModel = new FinancialPlannerAI();

app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'templates')));

// Serve dashboard page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'dashboard.html'));
});

// API to add income
app.post('/api/income', (req, res) => {
    const { userId, amount, description, sender } = req.body;
    dataStorage.addIncome(userId, amount, description, sender);
    res.json({ success: true });
});

// API to add outcome
app.post('/api/outcome', (req, res) => {
    const { userId, amount, description, sender } = req.body;
    dataStorage.addOutcome(userId, amount, description, sender);
    res.json({ success: true });
});

// API to get report
app.get('/api/report/:userId', (req, res) => {
    const userId = parseInt(req.params.userId);
    const report = dataStorage.getReport(userId);
    res.json(report);
});

// API to add budget
app.post('/api/budget', (req, res) => {
    const { userId, category, amount, period } = req.body;
    dataStorage.addBudget(userId, category, amount, period);
    res.json({ success: true });
});

// API to get budgets
app.get('/api/budgets/:userId', (req, res) => {
    const userId = parseInt(req.params.userId);
    const budgets = dataStorage.getBudgets(userId);
    res.json(budgets);
});

// API to add goal
app.post('/api/goal', (req, res) => {
    const { userId, name, targetAmount } = req.body;
    dataStorage.addGoal(userId, name, targetAmount);
    res.json({ success: true });
});

// API to get goals
app.get('/api/goals/:userId', (req, res) => {
    const userId = parseInt(req.params.userId);
    const goals = dataStorage.getGoals(userId);
    res.json(goals);
});

// API to generate AI response
app.post('/api/ai', async (req, res) => {
    const { text } = req.body;
    const response = await aiModel.generateResponse(text);
    res.json({ response });
});

app.listen(port, () => {
    console.log(`Web app listening at http://localhost:${port}`);
});
