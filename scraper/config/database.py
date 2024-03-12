from typing import Any, Mapping, Union

from pymongo import MongoClient
from pymongo.database import Database

from .settings import settings


def client() -> MongoClient:
    """Connects to the MongoDB client."""
    return MongoClient(settings.MONGO_CONNECTION_STRING)


def get_db() -> Database[Union[Mapping[str, Any], Any]]:
    """Gets the MongoDB database."""
    return client()[settings.MONGO_DATABASE_NAME]


def get_collection(collection_name: str) -> Any:
    """
    Gets the MongoDB collection.

    :param collection_name: Name of the collection to retrieve.
    :type collection_name: str
    :return: MongoDB collection object.
    :rtype: Any
    :raises KeyError: If the provided collection name is invalid.
    """
    try:
        return get_db()[collection_name]
    except KeyError:
        raise KeyError("Invalid collection name")
    except Exception as e:
        print(e)
        return None
