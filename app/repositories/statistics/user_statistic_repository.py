from typing import Dict, List

from sqlalchemy import func
from sqlalchemy.orm import Session

from models.user import User


class UserStatisticRepository:
    """
    Repository class for retrieving statistics related to users.
    """

    def __init__(self, session: Session):
        """
        Initialize the repository with a database session.

        Args:
            session (Session): The database session.
        """
        self.session = session

    def get_number_of_users_by_month(self) -> List[Dict[str, int]]:
        """
        Get the number of users created per month.

        Returns:
            List[Dict[str, int]]: A list of dictionaries containing month-year and count.
        """
        users_count = self.session.query(
            func.strftime('%Y-%m', User.created_at).label('month_year'),
            func.count('*').label('count')
        ).group_by(func.strftime('%Y-%m', User.created_at)).all()

        result = [{'month_year': row[0], 'count': row[1]} for row in users_count]
        return result
