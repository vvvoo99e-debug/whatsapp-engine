from flask import Flask
import threading
import os
import time

app = Flask(__name__)

# رقمك اللي بدك تربطه
MY_PHONE_NUMBER = "962785467150"

def run_whatsapp():
    # محاكاة تشغيل المكتبة لطلب الكود
    print("🚀 محرك بايثون بدأ العمل...")
    time.sleep(5)
    print(f"⏳ جاري طلب كود الربط للرقم: {MY_PHONE_NUMBER}")
    
    # ملاحظة: هنا ستحتاج لتشغيل أمر الربط الفعلي من المكتبة
    # للتبسيط الآن، سأجعله يطبع رسالة تنبيه لك في الـ Logs
    print("\n----------------------------------")
    print("🔥 المحرك جاهز! يرجى مراجعة شاشة Render Logs الآن")
    print("----------------------------------\n")

@app.route('/')
def index():
    return "WhatsApp Engine is Active! 🚀"

if __name__ == "__main__":
    # تشغيل الواتساب في خيط منفصل
    threading.Thread(target=run_whatsapp).start()
    
    # تشغيل سيرفر الويب
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)
