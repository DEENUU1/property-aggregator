from sqlalchemy.orm import Session
from models.user import User
from sqlalchemy import func
from typing import Dict, List
from collections import defaultdict


class UserStatisticRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_number_of_userss_by_month(self) -> List[Dict[str, int]]:
        users_count = self.session.query(
            func.strftime('%Y-%m', User.created_at).label('month_year'),
            func.count('*').label('count')
        ).group_by(func.strftime('%Y-%m', User.created_at)).all()

        result = [{'month_year': row[0], 'count': row[1]} for row in users_count]
        return result
