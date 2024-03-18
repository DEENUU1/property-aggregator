from typing import Any, List, Optional

from data.otodom import Otodom


class OtodomRepository:
    """A class to interact with an Otodom collection in a database."""

    def __init__(self, collection: Any):
        """
        Initialize the Otodom repository with a database collection.

        Parameters:
        - collection (Any): The collection in the database to interact with.
        """
        self.collection = collection

    def delete_all_parsed(self) -> None:
        """
        Return all parsed Otodom data from the collection.
        :return:
        """
        return self.collection.delete_many({"parsed": True})

    def create(self, data: Otodom) -> None:
        """
        Insert a new Otodom data into the database collection.

        Parameters:
        - data (Otodom): The Otodom data to be inserted into the collection.
        """
        _id = self.collection.insert_one(data.dict()).inserted_id
        return

    def get_all_unparsed(self) -> List[Optional[Otodom]]:
        """
        Retrieve all unparsed Otodom data from the collection.

        Returns:
        - List[Optional[Otodom]]: A list of Otodom data objects that are unparsed.
        """
        return self.collection.find({"parsed": False})

    def get_by_id(self, _id: str) -> Otodom:
        """
        Retrieve Otodom data from the collection by its ID.

        Parameters:
        - _id (str): The ID of the Otodom data to retrieve.

        Returns:
        - Otodom: The Otodom data corresponding to the provided ID.
        """
        return self.collection.find_one({"_id": _id})

    def update_parsed(self, otodom: Otodom) -> None:
        """
        Update the 'parsed' field of Otodom data in the collection.

        Parameters:
        - otodom (Otodom): The Otodom data object to update the 'parsed' field for.
        """
        return self.collection.update_one({"_id": otodom.id}, {"$set": {"parsed": True}})
