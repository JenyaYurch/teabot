from db import Session, Tea, User, Feedback
import random

class RecommendationEngine:
    @staticmethod
    def suggest_teas(telegram_id, limit=3):
        session = Session()
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if not user:
            session.close()
            return []
        # Use preferences if set, else suggest random teas
        query = session.query(Tea)
        prefs = user.preferences or {}
        if prefs.get('category'):
            query = query.filter(Tea.category == prefs['category'])
        if prefs.get('price_max'):
            query = query.filter(Tea.price <= prefs['price_max'])
        teas = query.all()
        if not teas:
            teas = session.query(Tea).all()
        # Exclude teas already in user history
        history = user.history or []
        teas = [t for t in teas if t.id not in history]
        if not teas:
            teas = session.query(Tea).all()
        result = random.sample(teas, min(limit, len(teas))) if teas else []
        session.close()
        return result

    @staticmethod
    def process_feedback(telegram_id, tea_id, rating, comment=None):
        session = Session()
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if not user:
            session.close()
            return
        feedback = Feedback(user_id=user.id, tea_id=tea_id, rating=rating, comment=comment)
        session.add(feedback)
        # Add tea to user history
        history = user.history or []
        if tea_id not in history:
            history.append(tea_id)
            user.history = history
        session.commit()
        session.close()
