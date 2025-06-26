from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from db import Session, User
from recommendation_engine import RecommendationEngine
import os

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = Session()
    telegram_id = str(update.effective_user.id)
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    if not user:
        user = User(telegram_id=telegram_id, preferences={}, history=[])
        session.add(user)
        session.commit()
        await update.message.reply_text('Welcome! Your profile has been created. Use /suggest to get a tea recommendation!')
    else:
        await update.message.reply_text('Welcome back! Use /suggest to get a tea recommendation!')
    session.close()

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Available commands:\n/start - Register\n/suggest - Get tea suggestion\n/help - Show help')

async def suggest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = str(update.effective_user.id)
    teas = RecommendationEngine.suggest_teas(telegram_id)
    if not teas:
        await update.message.reply_text('No teas found for your preferences. Please update your preferences or try again later.')
        return
    msg = 'Here are some tea suggestions for you:\n'
    for tea in teas:
        msg += f"\n{tea.name} ({tea.category}) - {tea.price} BYN\n{tea.description}\n"
    await update.message.reply_text(msg)

def start_bot():
    token = os.getenv('TELEGRAM_TOKEN')
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('suggest', suggest))
    app.run_polling()