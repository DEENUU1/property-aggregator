from collections import defaultdict
from typing import Dict, List

from sqlalchemy import func
from sqlalchemy.orm import Session

from models.offer import Offer


class OfferStatisticRepository:
    """
    Repository class for retrieving statistics related to offers.
    """

    def __init__(self, session: Session):
        """
        Initialize the repository with a database session.

        Args:
            session (Session): The database session.
        """
        self.session = session

    def get_number_of_offers_by_month(self) -> List[Dict[str, int]]:
        """
        Get the number of offers created per month.

        Returns:
            List[Dict[str, int]]: A list of dictionaries containing month-year and count.
        """
        offer_counts = self.session.query(
            func.strftime('%Y-%m', Offer.created_at).label('month_year'),
            func.count('*').label('count')
        ).group_by(func.strftime('%Y-%m', Offer.created_at)).all()

        result = [{'month_year': row[0], 'count': row[1]} for row in offer_counts]
        return result

    def count_offers_by_category(self) -> Dict[str, int]:
        """
        Count the number of offers by category.

        Returns:
            Dict[str, int]: A dictionary containing category and its count.
        """
        category_counts = defaultdict(int)
        offers = self.session.query(Offer).all()
        for offer in offers:
            category_counts[offer.category.value] += 1
        return category_counts

    def count_offers_by_subcategory(self) -> Dict[str, int]:
        """
        Count the number of offers by subcategory.

        Returns:
            Dict[str, int]: A dictionary containing subcategory and its count.
        """
        subcategory_counts = defaultdict(int)
        offers = self.session.query(Offer).all()
        for offer in offers:
            subcategory_counts[offer.sub_category.value] += 1
        return subcategory_counts
