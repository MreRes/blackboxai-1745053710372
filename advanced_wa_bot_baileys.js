/**
 * Advanced WhatsApp Bot using Baileys with full feature parity to the Python Selenium bot.
 * Features:
 * - Session persistence with multi-file auth state
 * - Message parsing for income, outcome, budgets, goals, reports
 * - Integration with AI model and data storage via REST API calls
 * - Error handling and reconnect logic
 * - QR code login with terminal display
 * 
 * Usage:
 * 1. Run `npm init -y`
 * 2. Run `npm install @adiwajshing/baileys qrcode-terminal axios pino`
 * 3. Run `node advanced_wa_bot_baileys.js`
 */
const { default: makeWASocket, useMultiFileAuthState, DisconnectReason, fetchLatestBaileysVersion } = require('@adiwajshing/baileys')
const P = require('pino')
const qrcode = require('qrcode-terminal')
const axios = require('axios')

const API_BASE_URL = 'http://localhost:5000/api' // Adjust to your backend API URL

// Initialize logger with timestamp and info level
const logger = P({
    level: 'info',
    timestamp: P.stdTimeFunctions.isoTime
})

async function startBot() {
    try {
        const { state, saveCreds } = await useMultiFileAuthState('baileys_auth_info')
        const { version, isLatest } = await fetchLatestBaileysVersion()
        logger.info(`Using WA version v${version.join('.')}, isLatest: ${isLatest}`)

        const sock = makeWASocket({
            version,
            logger,
            printQRInTerminal: true,
            auth: state
        })

        sock.ev.on('creds.update', saveCreds)

        sock.ev.on('connection.update', (update) => {
            const { connection, lastDisconnect, qr } = update
            if (qr) {
                qrcode.generate(qr, { small: true })
                logger.info('Scan the QR code above with your WhatsApp mobile app.')
            }
            if (connection === 'close') {
                const shouldReconnect = (lastDisconnect.error)?.output?.statusCode !== DisconnectReason.loggedOut
                logger.warn('Connection closed due to', lastDisconnect.error, ', reconnecting:', shouldReconnect)
                if (shouldReconnect) {
                    startBot()
                } else {
                    logger.error('Logged out. Please delete the auth folder and restart.')
                }
            } else if (connection === 'open') {
                logger.info('Connected to WhatsApp')
            }
        })

        sock.ev.on('messages.upsert', async (m) => {
            if (m.type !== 'notify') return
            for (const msg of m.messages) {
                if (!msg.message || msg.key.fromMe) continue
                const sender = msg.key.remoteJid
                const messageContent = msg.message.conversation || msg.message.extendedTextMessage?.text || ''
                logger.info(`Received message from ${sender}: ${messageContent}`)

                try {
                    const responseText = await processMessage(messageContent, sender)
                    await sock.sendMessage(sender, { text: responseText })
                    logger.info(`Sent response to ${sender}`)
                } catch (err) {
                    logger.error('Error processing message:', err)
                    await sock.sendMessage(sender, { text: 'Maaf, terjadi kesalahan saat memproses pesan Anda.' })
                }
            }
        })
    } catch (err) {
        logger.error('Fatal error in bot startup:', err)
        process.exit(1)
    }
}
async function processMessage(message, sender) {
    const incomePattern = /(pemasukan|income|masuk|terima|dapat|nambah|tambah|deposit|credit).*?([\d.,]+)/i
    const outcomePattern = /(pengeluaran|keluar|pakai|bayar|kurang|utang|debit|withdraw).*?([\d.,]+)/i

    function parseAmount(text) {
        const cleaned = text.replace(/[.,]/g, '')
        const num = parseFloat(cleaned)
        return isNaN(num) ? null : num
    }

    async function addIncome(userId, amount, description) {
        const res = await axios.post(`${API_BASE_URL}/income`, { userId, amount, description, sender })
        return res.data
    }
    async function addOutcome(userId, amount, description) {
        const res = await axios.post(`${API_BASE_URL}/outcome`, { userId, amount, description, sender })
        return res.data
    }
    async function getReport(userId) {
        const res = await axios.get(`${API_BASE_URL}/report/${userId}`)
        return res.data
    }
    async function addBudget(userId, category, amount, period) {
        const res = await axios.post(`${API_BASE_URL}/budget`, { userId, category, amount, period })
        return res.data
    }
    async function getBudgets(userId) {
        const res = await axios.get(`${API_BASE_URL}/budgets/${userId}`)
        return res.data
    }
    async function addGoal(userId, name, targetAmount) {
        const res = await axios.post(`${API_BASE_URL}/goal`, { userId, name, targetAmount })
        return res.data
    }
    async function getGoals(userId) {
        const res = await axios.get(`${API_BASE_URL}/goals/${userId}`)
        return res.data
    }
    async function generateAIResponse(text) {
        const res = await axios.post(`${API_BASE_URL}/ai`, { text })
        return res.data.response
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

startBot()
