from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from db import Session, User
from recommendation_engine import RecommendationEngine
import os

PREF_CATEGORY, PREF_STRENGTH, PREF_FLAVOR, PREF_PRICE = range(4)

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
    await update.message.reply_text(
        'Available commands:'
        '\n/start - Register or login'
        '\n/suggest - Get tea suggestion based on your preferences'
        '\n/setprefs - Set or update your tea preferences'
        '\n/help - Show this help message'
        '\n/cancel - Cancel current operation'
    )

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

async def setprefs_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    categories = ['Green', 'Black', 'Oolong', 'Pu-erh', 'White', 'Herbal', 'Other']
    reply_markup = ReplyKeyboardMarkup([[c] for c in categories], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text('What tea category do you prefer?', reply_markup=reply_markup)
    return PREF_CATEGORY

async def setprefs_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['category'] = update.message.text
    strengths = ['Light', 'Medium', 'Strong']
    reply_markup = ReplyKeyboardMarkup([[s] for s in strengths], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text('What strength do you prefer?', reply_markup=reply_markup)
    return PREF_STRENGTH

async def setprefs_strength(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['strength'] = update.message.text
    flavors = ['Floral', 'Fruity', 'Smoky', 'Nutty', 'Earthy', 'Spicy', 'Other']
    reply_markup = ReplyKeyboardMarkup([[f] for f in flavors], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text('What flavor notes do you like?', reply_markup=reply_markup)
    return PREF_FLAVOR

async def setprefs_flavor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['flavor'] = update.message.text
    await update.message.reply_text('What is your maximum price per tea (BYN)?', reply_markup=ReplyKeyboardRemove())
    return PREF_PRICE

async def setprefs_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        price = float(update.message.text)
    except ValueError:
        await update.message.reply_text('Please enter a valid number for price.')
        return PREF_PRICE
    context.user_data['price_max'] = price
    # Save preferences to DB
    session = Session()
    telegram_id = str(update.effective_user.id)
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    if user:
        user.preferences = {
            'category': context.user_data['category'],
            'strength': context.user_data['strength'],
            'flavor': context.user_data['flavor'],
            'price_max': context.user_data['price_max']
        }
        session.commit()
        await update.message.reply_text('Your preferences have been saved!')
    else:
        await update.message.reply_text('User not found. Please use /start first.')
    session.close()
    return ConversationHandler.END

async def setprefs_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Preference setup cancelled.')
    return ConversationHandler.END

def start_bot():
    token = os.getenv('TELEGRAM_TOKEN')
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('suggest', suggest))
    setprefs_handler = ConversationHandler(
        entry_points=[CommandHandler('setprefs', setprefs_start)],
        states={
            PREF_CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, setprefs_category)],
            PREF_STRENGTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, setprefs_strength)],
            PREF_FLAVOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, setprefs_flavor)],
            PREF_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, setprefs_price)],
        },
        fallbacks=[CommandHandler('cancel', setprefs_cancel)]
    )
    app.add_handler(setprefs_handler)
    app.run_polling()