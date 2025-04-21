const axios = require('axios');
const P = require('pino');
const { default: makeWASocket, useMultiFileAuthState, DisconnectReason, fetchLatestBaileysVersion } = require('@adiwajshing/baileys');
const qrcode = require('qrcode-terminal');

const API_BASE_URL = 'http://localhost:5000/api'; // Adjust to your backend API URL

const logger = P({
    level: 'info',
    timestamp: P.stdTimeFunctions.isoTime
});

async function retryRequest(fn, retries = 3, delay = 1000) {
    for (let i = 0; i < retries; i++) {
        try {
            return await fn();
        } catch (error) {
            logger.warn(`Request failed (attempt ${i + 1}): ${error.message}`);
            if (i < retries - 1) {
                await new Promise(res => setTimeout(res, delay * Math.pow(2, i)));
            } else {
                throw error;
            }
        }
    }
}

async function startBot() {
    try {
        const { state, saveCreds } = await useMultiFileAuthState('baileys_auth_info');
        const { version, isLatest } = await fetchLatestBaileysVersion();
        logger.info(`Using WA version v${version.join('.')}, isLatest: ${isLatest}`);

        const sock = makeWASocket({
            version,
            logger,
            printQRInTerminal: true,
            auth: state
        });

        sock.ev.on('creds.update', saveCreds);

        sock.ev.on('connection.update', (update) => {
            const { connection, lastDisconnect, qr } = update;
            if (qr) {
                qrcode.generate(qr, { small: true });
                logger.info('Scan the QR code above with your WhatsApp mobile app.');
            }
            if (connection === 'close') {
                const shouldReconnect = (lastDisconnect.error)?.output?.statusCode !== DisconnectReason.loggedOut;
                logger.warn('Connection closed due to', lastDisconnect.error, ', reconnecting:', shouldReconnect);
                if (shouldReconnect) {
                    startBot();
                } else {
                    logger.error('Logged out. Please delete the auth folder and restart.');
                }
            } else if (connection === 'open') {
                logger.info('Connected to WhatsApp');
            }
        });

        sock.ev.on('messages.upsert', async (m) => {
            if (m.type !== 'notify') return;
            for (const msg of m.messages) {
                if (!msg.message || msg.key.fromMe) continue;
                const sender = msg.key.remoteJid;
                const messageContent = msg.message.conversation || msg.message.extendedTextMessage?.text || '';
                logger.info(`Received message from ${sender}: ${messageContent}`);

                try {
                    const responseText = await processMessage(messageContent, sender);
                    await sock.sendMessage(sender, { text: responseText });
                    logger.info(`Sent response to ${sender}`);
                } catch (err) {
                    logger.error('Error processing message:', err);
                    await sock.sendMessage(sender, { text: 'Maaf, terjadi kesalahan saat memproses pesan Anda.' });
                }
            }
        });
    } catch (err) {
        logger.error('Fatal error in bot startup:', err);
        process.exit(1);
    }
}
