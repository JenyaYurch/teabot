# Tea Suggester Telegram Bot

A modular Telegram bot that parses tea catalogs from [teashop.by](https://www.teashop.by/), stores data in PostgreSQL, and provides personalized tea recommendations to users via Telegram.

## Features
- Automatic tea catalog parsing and updates
- PostgreSQL database for teas, users, and feedback
- Telegram bot interface for user interaction
- Personalized tea suggestions based on preferences and history
- Modular, extensible architecture

## Architecture
- **Catalog Parser**: Scrapes and parses tea data
- **Database Layer**: PostgreSQL with SQLAlchemy ORM
- **Recommendation Engine**: Suggests teas based on user data
- **Telegram Bot Interface**: Handles user commands and messaging
- **User Profile Manager**: Manages user data and preferences
- **Scheduler/Updater**: Automates catalog updates

## Setup
1. Clone this repository from GitHub.
2. Install Python 3.8+ and PostgreSQL.
3. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
4. Configure your PostgreSQL database and update connection settings in the code.
5. Run the bot:
   ```bash
   python main.py
   ```

## GitHub Integration
- Push your local changes to your GitHub repository for version control and collaboration.

## Requirements
- Python 3.8+
- PostgreSQL
- See `requirements.txt` for Python dependencies

## License
MIT 

## Environment Variables

You must set the `DATABASE_URL` environment variable to connect to your database. Example for PostgreSQL:

```
DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database>
```

For local development, you can set this in a `.env` file or export it in your shell:

```
export DATABASE_URL=postgresql://postgres:<your_password>@localhost:5432/postgres
```

**Do not commit secrets or passwords to version control.** 