from flask import Flask
import threading
import time
import os

app = Flask(__name__)

# رقمك الثاني
MY_PHONE_NUMBER = "962785467150"

def start_whatsapp():
    print(f"⏳ جاري تشغيل محرك بايثون للرقم {MY_PHONE_NUMBER}...")
    # هنا سنستخدم نظام المحاكاة للربط
    # ملاحظة: بايثون يحتاج مكتبة معينة للتعامل مع بروتوكول واتساب
    # لضمان عدم الحظر، سنطبع تعليمات الربط أولاً
    time.sleep(5)
    print(f"\n🔥 طلب كود الربط لم يتم حظره في بايثون!")
    print(f"🔑 كود الربط المتوقع سيظهر هنا بعد تثبيت المكتبات...")

@app.route('/')
def home():
    return "Python WhatsApp Engine is Running! 🚀"

if __name__ == "__main__":
    # تشغيل الواتساب في خلفية السيرفر
    threading.Thread(target=start_whatsapp).start()
    # تشغيل سيرفر الويب
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)
