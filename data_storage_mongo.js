// MongoDB-based data storage module for WhatsApp financial planner bot

const { MongoClient, ObjectId } = require('mongodb');

class DataStorageMongo {
    constructor(uri, dbName) {
        this.client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });
        this.dbName = dbName;
        this.db = null;
    }

    async connect() {
        await this.client.connect();
        this.db = this.client.db(this.dbName);
        console.log('Connected to MongoDB');
    }

    async close() {
        await this.client.close();
    }

    async getUserIdByPhone(phone) {
        const users = this.db.collection('users');
        let user = await users.findOne({ phone });
        if (!user) {
            const result = await users.insertOne({ phone });
            user = await users.findOne({ _id: result.insertedId });
        }
        return user._id.toString();
    }

    async addIncome(userId, amount, description, senderPhone) {
        const incomes = this.db.collection('incomes');
        await incomes.insertOne({
            userId: ObjectId(userId),
            amount,
            description,
            senderPhone,
            date: new Date()
        });
    }

    async addOutcome(userId, amount, description, senderPhone) {
        const outcomes = this.db.collection('outcomes');
        await outcomes.insertOne({
            userId: ObjectId(userId),
            amount,
            description,
            senderPhone,
            date: new Date()
        });
    }

    async getReport(userId) {
        const incomes = this.db.collection('incomes');
        const outcomes = this.db.collection('outcomes');

        const incomeAgg = await incomes.aggregate([
            { $match: { userId: ObjectId(userId) } },
            { $group: { _id: null, total: { $sum: "$amount" } } }
        ]).toArray();

        const outcomeAgg = await outcomes.aggregate([
            { $match: { userId: ObjectId(userId) } },
            { $group: { _id: null, total: { $sum: "$amount" } } }
        ]).toArray();

        const totalIncome = incomeAgg.length > 0 ? incomeAgg[0].total : 0;
        const totalOutcome = outcomeAgg.length > 0 ? outcomeAgg[0].total : 0;
        const balance = totalIncome - totalOutcome;

        return { total_income: totalIncome, total_outcome: totalOutcome, balance };
    }

    async addBudget(userId, category, amount, period) {
        const budgets = this.db.collection('budgets');
        await budgets.insertOne({
            userId: ObjectId(userId),
            category,
            amount,
            period
        });
    }

    async getBudgets(userId) {
        const budgets = this.db.collection('budgets');
        return await budgets.find({ userId: ObjectId(userId) }).toArray();
    }

    async addGoal(userId, name, targetAmount) {
        const goals = this.db.collection('goals');
        await goals.insertOne({
            userId: ObjectId(userId),
            name,
            target_amount: targetAmount,
            current_amount: 0
        });
    }

    async getGoals(userId) {
        const goals = this.db.collection('goals');
        return await goals.find({ userId: ObjectId(userId) }).toArray();
    }
}

module.exports = DataStorageMongo;
