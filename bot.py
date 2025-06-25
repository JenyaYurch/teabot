from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Welcome to Tea Suggester Bot! Use /suggest to get a tea recommendation!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Available commands:\n/start - Register\n/suggest - Get tea suggestion\n/help - Show help')

async def suggest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: Integrate with recommendation engine
    await update.message.reply_text('Here is a tea suggestion for you!')

def start_bot():
    token = os.getenv('TELEGRAM_TOKEN')
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('suggest', suggest))
    app.run_polling() 