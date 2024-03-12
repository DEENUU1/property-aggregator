from typing import List, Dict, Any, Optional

from data.location import Location
from data.offer import Offer
from data.subcategory_enum import SubCategoryEnum

from .parse_strategy import ParseStrategy


class OlxParser(ParseStrategy):

    @staticmethod
    def __get_param_value(params: List[Dict[str, Any]], key: str) -> Any:
        """
        Retrieve parameter value based on key from a list of parameters.

        Args:
            params (List[Dict[str, Any]]): List of parameters.
            key (str): Key to search for.

        Returns:
            Any: Value corresponding to the key, if found.
        """
        for param in params:
            if key in param["key_name"]:
                return param["value"]

    @staticmethod
    def __remove_html_tags(text: Optional[str]) -> Optional[str]:
        """
        Remove HTML tags from text.

        Args:
            text (Optional[str]): Text possibly containing HTML tags.

        Returns:
            Optional[str]: Text with HTML tags removed.
        """
        html_tags = ["<br />", "</ul>", "<ul>", "<li>", "/li>", "<p>", "</p>", "<strong>", "</strong>"]

        if not text:
            return None
        for tag in html_tags:
            text = text.replace(tag, "")
        return text

    @staticmethod
    def __map_floor(floor: Optional[str]) -> Optional[int]:
        """
        Map floor string to integer.

        Args:
            floor (Optional[str]): Floor information as a string.

        Returns:
            Optional[int]: Mapped floor as an integer.
        """
        if not floor:
            return None

        mapper = {
            "8": 8,
            "7": 7,
            "6": 6,
            "2": 2,
            "Parter": 0,
            "1": 1,
            "3": 3,
            "5": 5,
            "10": 10,
            "Powyżej 10": 10,
            "4": 4,
        }
        if floor not in mapper:
            return None
        return mapper[floor]

    @staticmethod
    def __map_sub_category(sub_category: int) -> str:
        """
        Map sub-category integer to SubCategoryEnum.

        Args:
            sub_category (int): Sub-category information as integer.

        Returns:
            str: Mapped sub-category.
        """
        sub_categories = {
            0: SubCategoryEnum.WYNAJEM,
            1: SubCategoryEnum.SPRZEDAZ
        }
        return sub_categories[sub_category]

    @staticmethod
    def __map_room_number(room_numer: Optional[str]) -> Optional[int]:
        """
        Map room number string to integer.

        Args:
            room_numer (Optional[str]): Room number information as a string.

        Returns:
            Optional[int]: Mapped room number as an integer.
        """
        if not room_numer:
            return None

        mapper = {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4
        }

        if room_numer not in mapper:
            return None
        return mapper[room_numer]

    def parse(self, data, *args, **kwargs) -> Optional[List[Offer]]:
        """
        Parse OLX data and return a list of Offer objects.

        Args:
            data: Data to be parsed.
            category: Category of the data.
            sub_category: Sub-category of the data.

        Returns:
            List[Offer]: List of parsed Offer objects.
        """
        content = data
        category, sub_category = kwargs["category"], kwargs["sub_category"]

        offers = content.get("data", None)
        if not offers:
            return

        parsed_offers = []

        for offer in offers:
            url = offer.get("url", None)
            title = offer.get("title", None)

            # Return if there is no url or title in parsed offer
            if url is None or title is None:
                continue

            description = offer.get("description", None)

            location_data = offer.get("location")
            city_name = location_data.get("city").get("name")
            region_name = location_data.get("region").get("name")

            # Create Location object
            location = Location(city=city_name, region=region_name)

            photo_data = offer.get("photos", None)
            photos = []
            for photo in photo_data:
                link = photo.get("link", None)
                width = photo.get("width", None)
                height = photo.get("height", None)

                # Add width and height values to link
                full_link = link.format(width=width, height=height)
                photos.append(full_link)

            params_data = offer.get("params", None)
            parsed_params = []
            for param in params_data:
                # List of labels from which script should take values
                label_keys = ["roomsize", "floor_select", "builttype", "floor", "type"]

                key_name = param.get("key", None)
                if key_name == "price":
                    value = param.get("value", None).get("value", None)
                elif key_name in label_keys:
                    value = param.get("value").get("label")
                else:
                    value = param.get("value").get("key")
                    # If value is "yes" or "no", convert to boolean
                    if value == "yes" or value == "no":
                        value = True if value == "yes" else False

                param = {"key_name": key_name, "value": value}
                parsed_params.append(param)

            meters = self.__get_param_value(parsed_params, "m"),
            rent = self.__get_param_value(parsed_params, "rent")
            if rent:
                rent = float(rent)

            # Create Offer object
            offer = Offer(
                title=title,
                url=url,
                category=category,
                sub_category=self.__map_sub_category(sub_category),
                building_type=self.__get_param_value(parsed_params, "builttype"),
                price=float(self.__get_param_value(parsed_params, "price")),
                rent=rent,
                description=self.__remove_html_tags(description),
                price_per_meter=float(self.__get_param_value(parsed_params, "price_per_m")),
                area=float(meters[0]),
                building_floor=self.__map_floor(self.__get_param_value(parsed_params, "floor_select")),
                floor=self.__map_floor(self.__get_param_value(parsed_params, "floor")),
                room_number=self.__map_room_number(self.__get_param_value(parsed_params, "rooms")),
                has_furnitures=self.__get_param_value(parsed_params, "furniture"),
                photos=photos,
                location=location,
            )
            parsed_offers.append(offer)
        return parsed_offers
