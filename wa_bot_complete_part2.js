async function processMessage(message, sender) {
    const incomePattern = /(pemasukan|income|masuk|terima|dapat|nambah|tambah|deposit|credit).*?([\d.,]+)/i;
    const outcomePattern = /(pengeluaran|keluar|pakai|bayar|kurang|utang|debit|withdraw).*?([\d.,]+)/i;

    function parseAmount(text) {
        const cleaned = text.replace(/[.,]/g, '');
        const num = parseFloat(cleaned);
        return isNaN(num) ? null : num;
    }

    async function addIncome(userId, amount, description) {
        return retryRequest(() => axios.post(`${API_BASE_URL}/income`, { userId, amount, description, sender }));
    }
    async function addOutcome(userId, amount, description) {
        return retryRequest(() => axios.post(`${API_BASE_URL}/outcome`, { userId, amount, description, sender }));
    }
    async function getReport(userId) {
        return retryRequest(() => axios.get(`${API_BASE_URL}/report/${userId}`));
    }
    async function addBudget(userId, category, amount, period) {
        return retryRequest(() => axios.post(`${API_BASE_URL}/budget`, { userId, category, amount, period }));
    }
    async function getBudgets(userId) {
        return retryRequest(() => axios.get(`${API_BASE_URL}/budgets/${userId}`));
    }
    async function addGoal(userId, name, targetAmount) {
        return retryRequest(() => axios.post(`${API_BASE_URL}/goal`, { userId, name, targetAmount }));
    }
    async function getGoals(userId) {
        return retryRequest(() => axios.get(`${API_BASE_URL}/goals/${userId}`));
    }
    async function generateAIResponse(text) {
        return retryRequest(() => axios.post(`${API_BASE_URL}/ai`, { text }));
    }

    // Simulate user ID retrieval by phone (sender)
    const userId = 1;

    let response = "Maaf, saya tidak mengerti pesan Anda.";

    if (incomePattern.test(message)) {
        const match = incomePattern.exec(message);
        const amount = parseAmount(match[2]);
        if (amount !== null) {
            await addIncome(userId, amount, message);
            const report = await getReport(userId);
            response = `Pemasukan sebesar Rp ${amount} telah dicatat. Saldo Anda saat ini sebesar Rp ${report.data.balance}.`;
        } else {
            response = "Maaf, saya tidak dapat mengenali jumlah pemasukan.";
        }
    } else if (outcomePattern.test(message)) {
        const match = outcomePattern.exec(message);
        const amount = parseAmount(match[2]);
        if (amount !== null) {
            await addOutcome(userId, amount, message);
            const report = await getReport(userId);
            response = `Pengeluaran sebesar Rp ${amount} telah dicatat. Saldo Anda saat ini sebesar Rp ${report.data.balance}.`;
        } else {
            response = "Maaf, saya tidak dapat mengenali jumlah pengeluaran.";
        }
    } else if (['laporan', 'report', 'rekap'].includes(message.toLowerCase())) {
        const report = await getReport(userId);
        response = `Laporan Keuangan:\nPemasukan: Rp ${report.data.total_income}\nPengeluaran: Rp ${report.data.total_outcome}\nSaldo: Rp ${report.data.balance}\n\nUntuk laporan lengkap, kunjungi: http://localhost:5000`;
    } else if (message.toLowerCase().startsWith('add budget')) {
        const parts = message.split(' ');
        if (parts.length >= 5) {
            const category = parts[2];
            const amount = parseFloat(parts[3]);
            const period = parts[4];
            await addBudget(userId, category, amount, period);
            response = `Budget untuk kategori '${category}' sebesar Rp ${amount} per ${period} telah ditambahkan.`;
        } else {
            response = "Format perintah budget salah. Gunakan: add budget <kategori> <jumlah> <periode>";
        }
    } else if (message.toLowerCase().startsWith('show budgets')) {
        const budgets = await getBudgets(userId);
        if (budgets.length > 0) {
            response = "Daftar Budget:\n";
            budgets.forEach(b => {
                response += `- ${b.category}: Rp ${b.amount} per ${b.period}\n`;
            });
        } else {
            response = "Belum ada budget yang tercatat.";
        }
    } else if (message.toLowerCase().startsWith('add goal')) {
        const parts = message.split(' ');
        if (parts.length >= 4) {
            const name = parts[2];
            const targetAmount = parseFloat(parts[3]);
            await addGoal(userId, name, targetAmount);
            response = `Goal '${name}' dengan target Rp ${targetAmount} telah ditambahkan.`;
        } else {
            response = "Format perintah goal salah. Gunakan: add goal <nama> <target_jumlah>";
        }
    } else if (message.toLowerCase().startsWith('show goals')) {
        const goals = await getGoals(userId);
        if (goals.length > 0) {
            response = "Daftar Goals:\n";
            goals.forEach(g => {
                response += `- ${g.name}: Target Rp ${g.target_amount}, Saat ini Rp ${g.current_amount}\n`;
            });
        } else {
            response = "Belum ada goal yang tercatat.";
        }
    } else {
        response = await generateAIResponse(message);
    }

    return response;
}

startBot();
