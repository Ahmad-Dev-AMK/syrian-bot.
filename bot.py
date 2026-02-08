import os
import logging
import asyncio
import subprocess
import requests
from telegram import Update
from telegram.constants import ParseMode, ChatAction
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# ==========================================
# 🔐 حط المفتاح الجديد هون ضروري!
# ==========================================
GOOGLE_API_KEY = "AIzaSyDeWqLZW22CPBzyA8H_DihJx55Wcwy2W1Y" 
TELEGRAM_TOKEN = "8460625950:AAFz-56F1eya4vDVo14u94mkfb3Ik4rFE_I"
# ==========================================

# إعداد Gemini 1.5 Flash (المستقر والسريع)
genai.configure(api_key=GOOGLE_API_KEY)
generation_config = {"temperature": 0.7, "max_output_tokens": 8192}

system_instruction = "You are a helpful Cybersecurity Assistant. Use Syrian dialect."

# ✅ استخدام الموديل المستقر
model = genai.GenerativeModel("gemini-flash-latest", generation_config=generation_config, system_instruction=system_instruction)
chat_session = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_id = update.effective_user.id
    
    # 1. طباعة أن الرسالة وصلت
    print(f"📩 وصلني من المستخدم: {user_text}") 

    if user_id not in chat_session:
        chat_session[user_id] = model.start_chat(history=[])
    
    chat = chat_session[user_id]
    
    # إشعار "جاري الكتابة"
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    try:
        print("⏳ جاري إرسال الطلب لجوجل...")
        response = chat.send_message(user_text)
        print("✅ جوجل رد عليي!")
        print(f"🤖 خيار الرد هو: {response.text}")
        print("------------------------------------------------")
        await update.message.reply_text(response.text, parse_mode=ParseMode.MARKDOWN)
        print("📤 تم إرسال الرد للتليجرام.")
        
    except Exception as e:
        print(f"❌ صار خطأ كارثي: {e}") # رح يطبعلك سبب الخطأ بالتفصيل
        await update.message.reply_text(f"⚠️ خطأ: {e}")

async def start(update, context):
    await update.message.reply_text("🔥 البوت شغال يا معلم! جرب احكي معي.")

if __name__ == '__main__':
    print("🚀 البوت انطلق... ناطر رسائل...")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()