from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext
import os

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Welcome to Tea Suggester Bot! Use /suggest to get a tea recommendation.')

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text('Available commands:\n/start - Register\n/suggest - Get tea suggestion\n/help - Show help')

def suggest(update: Update, context: CallbackContext):
    # TODO: Integrate with recommendation engine
    update.message.reply_text('Here is a tea suggestion for you!')

def start_bot():
    token = os.getenv('TELEGRAM_TOKEN')
    updater = Updater(token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('suggest', suggest))
    updater.start_polling()
    updater.idle() 