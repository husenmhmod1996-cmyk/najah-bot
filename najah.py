import logging
import sqlite3
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# التوكن الخاص ببوت النجاح
TOKEN = "8919237890:AAHdYhq2UK8cYHxEVOJHkZpkkdj9Bvv_-Wo"

# إعداد قاعدة البيانات محلياً داخل المشروع
DB_NAME = "najah.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            user_id INTEGER PRIMARY KEY,
            full_name TEXT,
            grade TEXT,
            points INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

init_db()

# إعداد السجل (Logging)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE user_id = ?", (user.id,))
    existing = cursor.fetchone()
    
    if not existing:
        cursor.execute("INSERT INTO students (user_id, full_name, grade, points) VALUES (?, ?, ?, ?)", 
                       (user.id, user.full_name, "غير محدد", 0))
        conn.commit()
    conn.close()
    
    await update.message.reply_text(
        f"أهلاً بك يا أستاذ/طالب {user.full_name} في 🎓 **بوت النجاح التعليمي** 🇸🇾\n\n"
        "هذا البوت مخصص لمساعدتك في المناهج الدراسية السورية.\n"
        "استخدم الأوامر التالية للبدء:\n"
        "/help - المساعدة\n"
        "/info - معلوماتك الدراسية"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 **قائمة مساعدة بوت النجاح:**\n\n"
        "• البوت يعمل كمساعد تعليمي للمراحل الدراسية.\n"
        "• يمكنك طرح الأسئلة أو متابعة الملخصات.\n"
        "• للمزيد، تواصل مع إدارة المنصة."
    )

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT grade, points FROM students WHERE user_id = ?", (user.id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        grade, points = row
        await update.message.reply_text(f"👤 بياناتك:\n• الاسم: {user.full_name}\n• الصف: {grade}\n• النقاط: {points}")
    else:
        await update.message.reply_text("الرجاء الضغط على /start لتسجيل بياناتك أولاً.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"وصلتني رسالتك: '{text}'\nجاري تجهيز الإجابة التعليمية المناسبة لمساعدتك في دراستك.")

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info_command))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot is running successfully...")
    application.run_polling()

if __name__ == '__main__':
    main()
  
