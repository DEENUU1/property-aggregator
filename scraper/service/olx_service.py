from data.olx import Olx
from repository.olx_repository import OlxRepository

from config.database import get_collection


class OlxService:
    """A class to provide services related to OLX data."""

    def __init__(self):
        """Initialize the OLX service with an OLX repository."""
        self.repository = OlxRepository(get_collection("olx"))

    def delete_all_parsed(self):
        """
        Delete all parsed OLX data.

        Returns:
        - None
        """
        return self.repository.delete_all_parsed()

    def create(self, data: Olx):
        """
        Create a new OLX data entry.

        Parameters:
        - data (Olx): The OLX data to be created.

        Returns:
        - None
        """
        return self.repository.create(data)

    def get_all_unparsed(self):
        """
        Retrieve all unparsed OLX data.

        Returns:
        - List[Optional[Olx]]: A list of unparsed OLX data entries.
        """
        return self.repository.get_all_unparsed()

    def update_parsed(self, _id: str):
        """
        Update the 'parsed' field of an OLX data entry.

        Parameters:
        - _id (str): The ID of the OLX data entry to update.

        Returns:
        - None
        """
        obj = self.repository.get_by_id(_id)
        if not obj:
            return
        return self.repository.update_parsed(_id)

    def update_send(self, _id: str):
        """
        Update the 'send' field of an OLX data entry.

        Parameters:
        - _id (str): The ID of the OLX data entry to update.

        Returns:
        - None
        """
        obj = self.repository.get_by_id(_id)
        if not obj:
            return
        return self.repository.update_send(_id)
