import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os

# ======= GOOGLE SHEET SETUP =======
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1CNB0--jOclzm5ieyHVVaXzdIuyzwV9CNb-7PloXvRfE/edit?usp=sharing").sheet1

# ======= COMMAND: /chi =======
async def chi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = ' '.join(context.args)
        if len(text.strip().split()) < 2:
            await update.message.reply_text("Gõ như vầy: /chi 50000 cà phê")
            return
        so_tien = text.strip().split()[0]
        ly_do = ' '.join(text.strip().split()[1:])
        thoi_gian = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sheet.append_row([thoi_gian, so_tien, ly_do])
        await update.message.reply_text(f"✅ Đã lưu: {so_tien} – {ly_do}")
    except Exception as e:
        await update.message.reply_text("❌ Lỗi rồi! " + str(e))

# ======= ĐOẠN CHAT VUI VẺ =======
async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.lower()
    if "buồn" in msg:
        await update.message.reply_text("Có gì đâu mà buồn, tui luôn ở đây nè 🥺")
    else:
        await update.message.reply_text("Tui nghe nè, nói tiếp đi nhen 🐣")

# ======= MAIN BOT SETUP =======
if __name__ == '__main__':
    app = ApplicationBuilder().token("7713715969:AAGH32WEh_CtoWmfnBUKgCbOXhDRse1lMww").build()
    app.add_handler(CommandHandler("chi", chi))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, talk))
    print("Bot is running...")
    app.run_polling()
