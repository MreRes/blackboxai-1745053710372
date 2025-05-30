const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const http = require('http');
const { Server } = require('socket.io');
const DataStorageMongo = require('./data_storage_mongo');
const FinancialPlannerAI = require('./ai_model');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

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

// Emit update event to clients
function emitUpdate(eventType, data) {
    io.emit(eventType, data);
}

// API to add income
app.post('/api/income', async (req, res) => {
    try {
        const { userId, amount, description, sender } = req.body;
        await dataStorage.addIncome(userId, amount, description, sender);
        emitUpdate('incomeAdded', { userId, amount, description });
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
        emitUpdate('outcomeAdded', { userId, amount, description });
        res.json({ success: true });
    } catch (err) {
        res.status(500).json({ error: 'Failed to add outcome' });
    }
});

// Other API routes remain unchanged...

// Start server with socket.io
server.listen(port, () => {
    console.log(`Web app listening at http://localhost:${port}`);
});
