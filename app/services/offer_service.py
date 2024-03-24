from typing import Dict, Any, List

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from enums.offer_sort import OfferSortEnum
from models.offer import Offer
from repositories.city_repository import CityRepository
from repositories.offer_repository import OfferRepository
from repositories.region_repository import RegionRepository
from schemas.location import RegionInput, CityInput
from schemas.offer import OfferScraper, OfferList
from services.user_service import UserService


class OfferService:
    """
    Service class for handling offers.
    """

    def __init__(self, session: Session):
        """
        Initialize the service.

        Args:
            session (Session): Database session.
        """
        self.repository = OfferRepository(session)
        self.region_repository = RegionRepository(session)
        self.city_repository = CityRepository(session)
        self.user_service = UserService(session)

    def create(self, offers: List[OfferScraper]) -> List[Offer]:
        """
        Create a new offers.

        Args:
            offers (List[OfferScraper]): Details of the offer to be created.

        Returns:
            List[Offer}: Details of the created offers.
        """
        result = []
        for offer in offers:

            if self.repository.offer_exists_by_url(offer.details_url):
                raise HTTPException(status_code=400, detail="Offer already exists")

            if not self.region_repository.region_exists_by_name(offer.region_name):
                self.region_repository.create(RegionInput(name=offer.region_name))
            region = self.region_repository.get_by_name(offer.region_name)

            if not self.city_repository.city_exists_by_name(offer.city_name):
                self.city_repository.create(CityInput(name=offer.city_name, region_id=region.id))
            city = self.city_repository.get_by_name(offer.city_name)

            result.append(self.repository.create(offer, city.id))
        return result

    def delete(self, _id: int, user_id: UUID4) -> bool:
        """
        Delete an offer.

        Args:
            _id (int): ID of the offer to be deleted.
            user_id (UUID4): ID of the user performing the action.

        Returns:
            bool: True if deletion is successful, False otherwise.
        """
        if not self.user_service.is_superuser(user_id):
            raise HTTPException(status_code=403, detail="Forbidden")

        if not self.repository.offer_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Offer not found")
        offer = self.repository.get_offer_by_id(_id)
        self.repository.delete(offer)
        return True

    def get_all(
            self,
            offset: int = 1,
            page_size: int = 15,
            category: str = None,
            sub_category: str = None,
            building_type: str = None,
            price_min: int = None,
            price_max: int = None,
            area_min: int = None,
            area_max: int = None,
            rooms: int = None,
            furniture: bool = None,
            floor: int = None,
            query: str = None,
            sort_by: OfferSortEnum = OfferSortEnum.NEWEST
    ) -> OfferList:
        """
        Retrieve a list of offers based on filtering criteria.

        Args:
            offset (int): Offset for pagination.
            page_size (int): Number of offers per page.
            category (str): Offer category.
            sub_category (str): Offer sub-category.
            building_type (str): Type of building.
            price_min (int): Minimum price.
            price_max (int): Maximum price.
            area_min (int): Minimum area.
            area_max (int): Maximum area.
            rooms (int): Number of rooms.
            furniture (bool): Indicates whether the offer is furnished.
            floor (int): Floor number.
            query (str): Search query.
            sort_by (OfferSortEnum): Sorting criteria.

        Returns:
            OfferList: List of offers based on the provided criteria.
        """
        return self.repository.get_all(
            offset,
            page_size,
            category,
            sub_category,
            building_type,
            price_min,
            price_max,
            area_min,
            area_max,
            rooms,
            furniture,
            floor,
            query,
            sort_by
        )

    def get_by_id(self, _id: UUID4) -> Dict[str, Any]:
        """
        Retrieve details of an offer by its ID.

        Args:
            _id (UUID4): ID of the offer.

        Returns:
            Dict[str, Any]: Details of the offer.
        """
        if not self.repository.offer_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Offer not found")
        return self.repository.get_details(_id)
