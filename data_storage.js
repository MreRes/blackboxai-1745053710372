// Placeholder JavaScript data storage module
// Replace with actual database integration (e.g., SQLite, MongoDB, PostgreSQL)

class DataStorage {
    constructor() {
        this.users = new Map(); // userId -> user data
        this.incomes = new Map(); // userId -> array of income records
        this.outcomes = new Map(); // userId -> array of outcome records
        this.budgets = new Map(); // userId -> array of budgets
        this.goals = new Map(); // userId -> array of goals
    }

    getUserIdByPhone(phone) {
        // For demo, return fixed userId
        return 1;
    }

    addIncome(userId, amount, description, senderPhone) {
        if (!this.incomes.has(userId)) this.incomes.set(userId, []);
        this.incomes.get(userId).push({ amount, description, senderPhone, date: new Date() });
    }

    addOutcome(userId, amount, description, senderPhone) {
        if (!this.outcomes.has(userId)) this.outcomes.set(userId, []);
        this.outcomes.get(userId).push({ amount, description, senderPhone, date: new Date() });
    }

    getReport(userId) {
        const incomes = this.incomes.get(userId) || [];
        const outcomes = this.outcomes.get(userId) || [];
        const totalIncome = incomes.reduce((sum, i) => sum + i.amount, 0);
        const totalOutcome = outcomes.reduce((sum, o) => sum + o.amount, 0);
        const balance = totalIncome - totalOutcome;
        return { total_income: totalIncome, total_outcome: totalOutcome, balance };
    }

    addBudget(userId, category, amount, period) {
        if (!this.budgets.has(userId)) this.budgets.set(userId, []);
        this.budgets.get(userId).push({ category, amount, period });
    }

    getBudgets(userId) {
        return this.budgets.get(userId) || [];
    }

    addGoal(userId, name, targetAmount) {
        if (!this.goals.has(userId)) this.goals.set(userId, []);
        this.goals.get(userId).push({ name, target_amount: targetAmount, current_amount: 0 });
    }

    getGoals(userId) {
        return this.goals.get(userId) || [];
    }
}

module.exports = DataStorage;
