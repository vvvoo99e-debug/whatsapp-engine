const { default: makeWASocket, useMultiFileAuthState, Browsers } = require('@whiskeysockets/baileys');
const pino = require('pino');
const express = require('express');
const app = express();

const MY_PHONE_NUMBER = "962785467150"; 

async function connectToWhatsApp() {
    const { state, saveCreds } = await useMultiFileAuthState('auth_session');
    const sock = makeWASocket({
        auth: state,
        printQRInTerminal: false,
        browser: Browsers.macOS('Desktop'),
        logger: pino({ level: 'silent' })
    });

    if (!sock.authState.creds.registered) {
        console.log("⏳ جاري طلب كود الربط...");
        setTimeout(async () => {
            try {
                const code = await sock.requestPairingCode(MY_PHONE_NUMBER);
                console.log(`\n🔥 كود الربط الخاص بك هو: ${code}\n`);
            } catch (err) {
                console.log('❌ فشل الطلب، جاري المحاولة...');
            }
        }, 5000);
    }

    sock.ev.on('connection.update', (update) => {
        const { connection } = update;
        if (connection === 'open') console.log("🚀 تم الربط بنجاح!");
        if (connection === 'close') connectToWhatsApp();
    });

    sock.ev.on('creds.update', saveCreds);
}

connectToWhatsApp();
app.get('/', (req, res) => res.send('Server Active 🚀'));
app.listen(process.env.PORT || 3000);
