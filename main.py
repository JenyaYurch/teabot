from catalog_parser import parse_catalog, update_database
from db import init_db
from bot import start_bot
from scheduler import schedule_catalog_update

if __name__ == "__main__":
    # Initialize database
    init_db()
    # Schedule catalog updates
    schedule_catalog_update()
    # Start Telegram bot
    start_bot() 