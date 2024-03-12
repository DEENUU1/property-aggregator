from typing import Any, List, Optional

from data.olx import Olx


class OlxRepository:
    """A class to interact with an OLX collection in a database."""

    def __init__(self, collection: Any):
        """
        Initialize the OLX repository with a database collection.

        Parameters:
        - collection (Any): The collection in the database to interact with.
        """
        self.collection = collection

    def create(self, data: Olx) -> None:
        """
        Insert a new OLX data into the database collection.

        Parameters:
        - data (Olx): The OLX data to be inserted into the collection.
        """
        _id = self.collection.insert_one(data.dict()).inserted_id
        return

    def get_all_unparsed(self) -> List[Optional[Olx]]:
        """
        Retrieve all unparsed OLX data from the collection.

        Returns:
        - List[Optional[Olx]]: A list of OLX data objects that are unparsed.
        """
        return self.collection.find({"parsed": False})

    def get_by_id(self, _id: str) -> Olx:
        """
        Retrieve OLX data from the collection by its ID.

        Parameters:
        - _id (str): The ID of the OLX data to retrieve.

        Returns:
        - Olx: The OLX data corresponding to the provided ID.
        """
        return self.collection.find_one({"_id": _id})

    def update_parsed(self, olx: Olx) -> None:
        """
        Update the 'parsed' field of OLX data in the collection.

        Parameters:
        - olx (Olx): The OLX data object to update the 'parsed' field for.
        """
        return self.collection.update_one({"_id": olx.id}, {"$set": {"parsed": True}})
