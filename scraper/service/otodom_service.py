from data.otodom import Otodom
from repository.otodom_repository import OtodomRepository

from config.database import get_collection


class OtodomService:
    """A class to provide services related to Otodom data."""

    def __init__(self):
        """Initialize the Otodom service with an Otodom repository."""
        self.repository = OtodomRepository(get_collection("otodom"))

    def create(self, data: Otodom):
        """
        Create a new Otodom data entry.

        Parameters:
        - data (Otodom): The Otodom data to be created.

        Returns:
        - None
        """
        return self.repository.create(data)

    def get_all_unparsed(self):
        """
        Retrieve all unparsed Otodom data.

        Returns:
        - List[Optional[Otodom]]: A list of unparsed Otodom data entries.
        """
        return self.repository.get_all_unparsed()

    def update_parsed(self, _id: str):
        """
        Update the 'parsed' field of an Otodom data entry.

        Parameters:
        - _id (str): The ID of the Otodom data entry to update.

        Returns:
        - None
        """
        obj = self.repository.get_by_id(_id)
        if not obj:
            return
        return self.repository.update_parsed(_id)

    def update_send(self, _id: str):
        """
        Update the 'send' field of an Otodom data entry.

        Parameters:
        - _id (str): The ID of the Otodom data entry to update.

        Returns:
        - None
        """
        obj = self.repository.get_by_id(_id)
        if not obj:
            return
        return self.repository.update_send(_id)
