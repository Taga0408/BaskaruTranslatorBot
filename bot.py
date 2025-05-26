from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

questions = [
    {
        "question": "What is the capital of France?",
        "options": ["Paris", "Berlin", "Rome", "Madrid"],
        "answer": "Paris"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Venus"],
        "answer": "Mars"
    }
]

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {"score": 0, "q_index": 0}
    await send_question(update, context)

async def send_question(update, context):
    user_id = update.effective_user.id
    q_index = user_data[user_id]["q_index"]
    
    if q_index < len(questions):
        q = questions[q_index]
        options = "\n".join([f"- {opt}" for opt in q["options"]])
        await update.message.reply_text(f"{q['question']}\n{options}")
    else:
        score = user_data[user_id]["score"]
        await update.message.reply_text(f"✅ Test complete!\nYour score: {score}/{len(questions)}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_data:
        await update.message.reply_text("Please type /start to begin the quiz.")
        return

    q_index = user_data[user_id]["q_index"]
    answer = update.message.text.strip()

    if q_index < len(questions):
        correct = questions[q_index]["answer"]
        if answer.lower() == correct.lower():
            user_data[user_id]["score"] += 1
            await update.message.reply_text("✅ Correct!")
        else:
            await update.message.reply_text(f"❌ Wrong! Correct answer was: {correct}")
        
        user_data[user_id]["q_index"] += 1
        await send_question(update, context)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot started...")
app.run_polling()