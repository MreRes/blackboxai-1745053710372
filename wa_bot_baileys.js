/**
 * WhatsApp Bot using Baileys (WhatsApp Web API) for Node.js
 * This bot replicates the features of the Selenium bot:
 * - Listens for incoming messages
 * - Parses financial commands (income, outcome, budgets, goals, reports)
 * - Integrates with AI model and data storage (via HTTP API or direct calls)
 * - Sends appropriate responses
 * 
 * Requirements:
 * - Node.js installed
 * - Run `npm install @adiwajshing/baileys qrcode-terminal axios`
 * 
 * Usage:
 * node wa_bot_baileys.js
 */

const { default: makeWASocket, useMultiFileAuthState, DisconnectReason, fetchLatestBaileysVersion } = require('@adiwajshing/baileys')
const P = require('pino')
const qrcode = require('qrcode-terminal')
const axios = require('axios')

async function startBot() {
    const { state, saveCreds } = await useMultiFileAuthState('baileys_auth_info')
    const { version, isLatest } = await fetchLatestBaileysVersion()
    console.log(`Using WA version v${version.join('.')}, isLatest: ${isLatest}`)

    const sock = makeWASocket({
        version,
        logger: P({ level: 'silent' }),
        printQRInTerminal: true,
        auth: state
    })

    sock.ev.on('creds.update', saveCreds)

    sock.ev.on('connection.update', (update) => {
        const { connection, lastDisconnect, qr } = update
        if (qr) {
            qrcode.generate(qr, { small: true })
            console.log('Scan the QR code above with your WhatsApp mobile app.')
        }
        if (connection === 'close') {
            const shouldReconnect = (lastDisconnect.error)?.output?.statusCode !== DisconnectReason.loggedOut
            console.log('Connection closed due to', lastDisconnect.error, ', reconnecting:', shouldReconnect)
            if (shouldReconnect) {
                startBot()
            } else {
                console.log('Logged out. Please delete the auth folder and restart.')
            }
        } else if (connection === 'open') {
            console.log('Connected to WhatsApp')
        }
    })

    sock.ev.on('messages.upsert', async (m) => {
        if (m.type !== 'notify') return
        for (const msg of m.messages) {
            if (!msg.message || msg.key.fromMe) continue
            const sender = msg.key.remoteJid
            const messageContent = msg.message.conversation || msg.message.extendedTextMessage?.text || ''
            console.log(`Received message from ${sender}: ${messageContent}`)

            // Parse message and generate response similar to Selenium bot logic
            let responseText = await processMessage(messageContent, sender)

            await sock.sendMessage(sender, { text: responseText })
            console.log(`Sent response to ${sender}`)
        }
    })
}

// Function to parse message and generate response
async function processMessage(message, sender) {
    // Define regex patterns for income and outcome
    const incomePattern = /(pemasukan|income|masuk|terima|dapat|nambah|tambah|deposit|credit).*?([\d.,]+)/i
    const outcomePattern = /(pengeluaran|keluar|pakai|bayar|kurang|utang|debit|withdraw).*?([\d.,]+)/i

    // Helper to parse amount string to float
    function parseAmount(text) {
        const cleaned = text.replace(/[.,]/g, '')
        const num = parseFloat(cleaned)
        return isNaN(num) ? null : num
    }

    // Placeholder: Replace with actual API calls or direct integration
    async function addIncome(userId, amount, description) {
        // Example: call your backend API to add income
        // await axios.post('http://localhost:5000/api/income', { userId, amount, description, sender })
        return true
    }
    async function addOutcome(userId, amount, description) {
        // await axios.post('http://localhost:5000/api/outcome', { userId, amount, description, sender })
        return true
    }
    async function getReport(userId) {
        // const res = await axios.get(`http://localhost:5000/api/report/${userId}`)
        // return res.data
        return {
            total_income: 1000000,
            total_outcome: 500000,
            balance: 500000
        }
    }
    async function addBudget(userId, category, amount, period) {
        // await axios.post('http://localhost:5000/api/budget', { userId, category, amount, period })
        return true
    }
    async function getBudgets(userId) {
        // const res = await axios.get(`http://localhost:5000/api/budgets/${userId}`)
        // return res.data
        return [
            { category: 'makanan', amount: 500000, period: 'bulan' }
        ]
    }
    async function addGoal(userId, name, targetAmount) {
        // await axios.post('http://localhost:5000/api/goal', { userId, name, targetAmount })
        return true
    }
    async function getGoals(userId) {
        // const res = await axios.get(`http://localhost:5000/api/goals/${userId}`)
        // return res.data
        return [
            { name: 'Liburan', target_amount: 5000000, current_amount: 1000000 }
        ]
    }
    async function generateAIResponse(text) {
        // Call your AI model API or local function
        // const res = await axios.post('http://localhost:5000/api/ai', { text })
        // return res.data.response
        return "Ini adalah balasan AI untuk pesan Anda."
    }

    // Simulate user ID retrieval by phone (sender)
    const userId = 1

    let response = "Maaf, saya tidak mengerti pesan Anda."

    if (incomePattern.test(message)) {
        const match = incomePattern.exec(message)
        const amount = parseAmount(match[2])
        if (amount !== null) {
            await addIncome(userId, amount, message)
            response = `Pemasukan sebesar Rp ${amount} telah dicatat.`
        } else {
            response = "Maaf, saya tidak dapat mengenali jumlah pemasukan."
        }
    } else if (outcomePattern.test(message)) {
        const match = outcomePattern.exec(message)
        const amount = parseAmount(match[2])
        if (amount !== null) {
            await addOutcome(userId, amount, message)
            response = `Pengeluaran sebesar Rp ${amount} telah dicatat.`
        } else {
            response = "Maaf, saya tidak dapat mengenali jumlah pengeluaran."
        }
    } else if (['laporan', 'report', 'rekap'].includes(message.toLowerCase())) {
        const report = await getReport(userId)
        response = `Laporan Keuangan:\nPemasukan: Rp ${report.total_income}\nPengeluaran: Rp ${report.total_outcome}\nSaldo: Rp ${report.balance}\n\nUntuk laporan lengkap, kunjungi: http://localhost:5000`
    } else if (message.toLowerCase().startsWith('add budget')) {
        const parts = message.split(' ')
        if (parts.length >= 5) {
            const category = parts[2]
            const amount = parseFloat(parts[3])
            const period = parts[4]
            await addBudget(userId, category, amount, period)
            response = `Budget untuk kategori '${category}' sebesar Rp ${amount} per ${period} telah ditambahkan.`
        } else {
            response = "Format perintah budget salah. Gunakan: add budget <kategori> <jumlah> <periode>"
        }
    } else if (message.toLowerCase().startsWith('show budgets')) {
        const budgets = await getBudgets(userId)
        if (budgets.length > 0) {
            response = "Daftar Budget:\n"
            budgets.forEach(b => {
                response += `- ${b.category}: Rp ${b.amount} per ${b.period}\n`
            })
        } else {
            response = "Belum ada budget yang tercatat."
        }
    } else if (message.toLowerCase().startsWith('add goal')) {
        const parts = message.split(' ')
        if (parts.length >= 4) {
            const name = parts[2]
            const targetAmount = parseFloat(parts[3])
            await addGoal(userId, name, targetAmount)
            response = `Goal '${name}' dengan target Rp ${targetAmount} telah ditambahkan.`
        } else {
            response = "Format perintah goal salah. Gunakan: add goal <nama> <target_jumlah>"
        }
    } else if (message.toLowerCase().startsWith('show goals')) {
        const goals = await getGoals(userId)
        if (goals.length > 0) {
            response = "Daftar Goals:\n"
            goals.forEach(g => {
                response += `- ${g.name}: Target Rp ${g.target_amount}, Saat ini Rp ${g.current_amount}\n`
            })
        } else {
            response = "Belum ada goal yang tercatat."
        }
    } else {
        response = await generateAIResponse(message)
    }

    return response
}

startBot().catch(err => console.error('Unexpected error:', err))
