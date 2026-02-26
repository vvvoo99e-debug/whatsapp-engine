from flask import Flask
import threading
import os
import time
from playwright.sync_api import sync_playwright

app = Flask(__name__)
MY_PHONE_NUMBER = "962785467150"

def run_whatsapp():
    print("🚀 بدء تشغيل متصفح Chrome المخفي...")
    try:
        with sync_playwright() as p:
            # تشغيل المتصفح المخفي
            browser = p.chromium.launch(headless=True)
            # تحديد لغة المتصفح لتكون إنجليزية لتسهيل البحث عن الأزرار
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                locale="en-US"
            )
            page = context.new_page()
            
            print("⏳ جاري فتح واتساب ويب...")
            page.goto("https://web.whatsapp.com/", timeout=60000)
            time.sleep(15) # انتظار تحميل الصفحة بالكامل
            
            print("🔥 تم تحميل الصفحة! جاري طلب كود الربط...")
            
            # الضغط على زر "الربط برقم الهاتف"
            page.click('span[role="button"]:has-text("Link with phone number")', timeout=15000)
            time.sleep(2)
            
            # إدخال رقم الهاتف
            page.fill('input[type="text"]', MY_PHONE_NUMBER)
            page.keyboard.press("Enter")
            time.sleep(8) # انتظار ظهور الكود
            
            # استخراج الكود المكون من 8 أحرف
            code_elements = page.query_selector_all('div[data-testid="pairing-code"] span')
            if code_elements:
                code = "".join([el.inner_text() for el in code_elements])
                print("\n" + "="*40)
                print(f"🔥 كود الربط الخاص بك هو: {code}")
                print("="*40 + "\n")
            else:
                print("❌ لم يتم العثور على الكود، قد يكون واتساب طلب مسح QR بدلاً من ذلك.")
                
            # إبقاء المتصفح مفتوحاً لإتمام الربط
            time.sleep(120)
            browser.close()
            
    except Exception as e:
        print(f"❌ حدث خطأ أثناء محاولة جلب الكود: {str(e)}")

@app.route('/')
def index():
    return "WhatsApp Python Engine with Chrome is Running! 🚀"

if __name__ == "__main__":
    threading.Thread(target=run_whatsapp).start()
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)
