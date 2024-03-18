from sqlalchemy.orm import Session
from models.offer import Offer
from sqlalchemy import func


class OfferStatisticRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_number_of_offers_by_month(self):
        offer_counts = self.session.query(
            func.strftime('%Y-%m', Offer.created_at).label('month_year'),
            func.count('*').label('count')
        ).group_by(func.strftime('%Y-%m', Offer.created_at)).all()

        result = [{'month_year': row[0], 'count': row[1]} for row in offer_counts]
        return result
