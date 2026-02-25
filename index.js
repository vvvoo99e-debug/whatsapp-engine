const { default: makeWASocket, useMultiFileAuthState, Browsers } = require('@whiskeysockets/baileys');
const pino = require('pino');
const express = require('express');
const app = express();

const MY_PHONE_NUMBER = "962785467150"; 
let isRequesting = false; // لمنع تكرار طلب الكود

async function connectToWhatsApp() {
    const { state, saveCreds } = await useMultiFileAuthState('auth_session');
    const sock = makeWASocket({
        auth: state,
        printQRInTerminal: false,
        browser: Browsers.macOS('Desktop'),
        logger: pino({ level: 'silent' })
    });

    if (!sock.authState.creds.registered && !isRequesting) {
        isRequesting = true; // قفل الطلب عشان ما يطلع كود ثاني
        console.log("⏳ جاري طلب كود الربط (مرة واحدة فقط)...");
        setTimeout(async () => {
            try {
                const code = await sock.requestPairingCode(MY_PHONE_NUMBER);
                console.log(`\n🔥 كود الربط الثابت هو: ${code}\n`);
            } catch (err) {
                console.log('❌ فشل الطلب، جاري المحاولة بعد قليل...');
                isRequesting = false;
            }
        }, 8000); // زيادة الوقت لضمان استقرار السيرفر
    }

    sock.ev.on('connection.update', (update) => {
        const { connection } = update;
        if (connection === 'open') {
            console.log("🚀 تم الربط بنجاح!");
            isRequesting = false;
        }
        if (connection === 'close') connectToWhatsApp();
    });

    sock.ev.on('creds.update', saveCreds);
}

connectToWhatsApp();
app.get('/', (req, res) => res.send('Server Active 🚀'));
app.listen(process.env.PORT || 3000);
