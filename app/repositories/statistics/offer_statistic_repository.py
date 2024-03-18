from sqlalchemy.orm import Session
from models.offer import Offer
from sqlalchemy import func
from typing import Dict, List
from collections import defaultdict


class OfferStatisticRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_number_of_offers_by_month(self) -> List[Dict[str, int]]:
        offer_counts = self.session.query(
            func.strftime('%Y-%m', Offer.created_at).label('month_year'),
            func.count('*').label('count')
        ).group_by(func.strftime('%Y-%m', Offer.created_at)).all()

        result = [{'month_year': row[0], 'count': row[1]} for row in offer_counts]
        return result

    def count_offers_by_category(self) -> Dict[str, int]:
        category_counts = defaultdict(int)
        offers = self.session.query(Offer).all()
        for offer in offers:
            category_counts[offer.category.value] += 1
        return category_counts

    def count_offers_by_subcategory(self) -> Dict[str, int]:
        subcategory_counts = defaultdict(int)
        offers = self.session.query(Offer).all()
        for offer in offers:
            subcategory_counts[offer.sub_category.value] += 1
        return subcategory_counts
