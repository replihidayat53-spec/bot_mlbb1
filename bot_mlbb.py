import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- KONFIGURASI AMAN ---
# Ambil dari Environment Variable (Setting di Render/VPS)
TOKEN = os.getenv('BOT_TOKEN')
API_KEY = os.getenv('CH_API_KEY') 
API_ENDPOINT = "https://api.sikatid.com/v1/cek-ml" # Contoh Endpoint

async def get_data_bisnis(uid, zone):
    params = {
        'key': API_KEY,
        'id': uid,
        'zone': zone
    }
    try:
        # Menggunakan POST atau GET sesuai dokumentasi penyedia
        response = requests.get(API_ENDPOINT, params=params, timeout=15)
        return response.json()
    except:
        return None

async def handle_cek(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Logika ambil ID & Zone dari pesan
    text = update.message.text.replace('/cek ', '').replace('(', ' ').replace(')', '').split()
    if len(text) < 2:
        await update.message.reply_text("❌ Format: `ID Zone`\nContoh: `12345678 1234`")
        return

    uid, zone = text[0], text[1]
    msg = await update.message.reply_text("🔄 **Memproses Data Bisnis...**")

    data = await get_data_bisnis(uid, zone)

    if data and data.get('status') == True:
        # Struktur di bawah ini adalah contoh, sesuaikan dengan hasil API yang Anda beli
        res = (
            f"🛡️ **VERIFIKASI AKUN MLBB**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 **Nickname:** `{data['name']}`\n"
            f"🆔 **ID:** `{uid} ({zone})`\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🏆 **Rank:** {data['rank']}\n"
            f"📊 **Total WR:** {data['wr_total']}%\n"
            f"👕 **Total Skin:** {data['skin']}\n"
            f"🦸 **Total Hero:** {data['hero']}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🛒 *Ingin beli akun ini? Hubungi Admin.*"
        )
        await msg.edit_text(res, parse_mode='Markdown')
    else:
        await msg.edit_text("❌ Gagal! Pastikan ID benar atau Saldo API Anda mencukupi.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("cek", handle_cek))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_cek))
    app.run_polling()

if __name__ == '__main__':
    main()