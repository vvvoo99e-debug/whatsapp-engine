const { default: makeWASocket, useMultiFileAuthState, Browsers, DisconnectReason } = require('@whiskeysockets/baileys');
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
        logger: pino({ level: 'silent' }) // صامت عشان ما يزعجك بالترمنال
    });

    // طلب الكود إذا الحساب مش مسجل
    if (!sock.authState.creds.registered) {
        console.log("⏳ جاري طلب كود الربط...");
        
        // 3 ثواني كافية جداً، ما في داعي لـ 8 ثواني
        setTimeout(async () => {
            try {
                const code = await sock.requestPairingCode(MY_PHONE_NUMBER);
                console.log(`\n🔥 كود الربط الخاص بك هو: ${code}\n`);
            } catch (err) {
                console.log('❌ فشل طلب الكود. (تأكد أنك حذفت مجلد auth_session قبل التشغيل)');
            }
        }, 3000); 
    }

    sock.ev.on('connection.update', (update) => {
        const { connection, lastDisconnect } = update;
        
        if (connection === 'open') {
            console.log("🚀 تم الربط بنجاح!");
        } else if (connection === 'close') {
            // هون بنفحص سبب الإغلاق عشان ما يدخل بدوامة تعليق
            const shouldReconnect = lastDisconnect?.error?.output?.statusCode !== DisconnectReason.loggedOut;
            console.log("⚠️ انقطع الاتصال، جاري إعادة المحاولة:", shouldReconnect);
            
            if (shouldReconnect) {
                connectToWhatsApp();
            } else {
                console.log("❌ تم تسجيل الخروج. يرجى حذف مجلد auth_session والبدء من جديد.");
            }
        }
    });

    sock.ev.on('creds.update', saveCreds);
}

connectToWhatsApp();
app.get('/', (req, res) => res.send('Server Active 🚀'));
app.listen(process.env.PORT || 3000, () => console.log("🌐 السيرفر شغال وينتظر الربط..."));
