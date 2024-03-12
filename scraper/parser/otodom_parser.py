import re
from typing import Optional, Tuple, List, Dict, Any

from bs4 import BeautifulSoup
from data.category_enum import CategoryEnum
from data.location import Location
from data.offer import Offer
from data.subcategory_enum import SubCategoryEnum

from .parse_strategy import ParseStrategy


class OtodomParser(ParseStrategy):
    @staticmethod
    def __get_city_region(full_location: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Extracts city and region from a full location string.

        Args:
            full_location (str): Full location string.

        Returns:
            Tuple[Optional[str], Optional[str]]: A tuple containing city and region strings.
        """
        city = full_location.split(",")[-2].strip()
        region = full_location.split(", ")[-1].strip()
        if city[0].islower():
            return None, region
        return city, region

    @staticmethod
    def __string_to_int(string: str) -> Optional[int]:
        """
        Converts a string to an integer.

        Args:
            string (str): Input string.

        Returns:
            Optional[int]: Converted integer value or None if conversion fails.
        """
        if string is None:
            return None

        numeric_part = re.sub(r'\D', '', string)

        if not numeric_part:
            return None

        return int(numeric_part)

    @staticmethod
    def __get_param_value(params: List[Dict[str, Any]], key: str) -> Any:
        """
        Retrieves a parameter value from a list of dictionaries.

        Args:
            params (List[Dict[str, Any]]): List of dictionaries containing parameters.
            key (str): Key to search for in the dictionaries.

        Returns:
            Any: Value corresponding to the key, if found.
        """
        for param in params:
            if key in param["key"]:
                return param["value"]

    @staticmethod
    def __map_category(category: str) -> str:
        """
        Maps a category string to its corresponding enum value.

        Args:
            category (str): Input category string.

        Returns:
            str: Corresponding enum value for the category.
        """
        mapper = {
            "mieszkanie": CategoryEnum.MIESZKANIE,
            "kawalerka": CategoryEnum.MIESZKANIE,
            "dom": CategoryEnum.DOM,
            "inwestycja": CategoryEnum.BIURA_I_LOKALE,
            "pokoj": CategoryEnum.POKOJ,
            "dzialka": CategoryEnum.DZIALKA,
            "lokal": CategoryEnum.BIURA_I_LOKALE,
            "haleimagazyny": CategoryEnum.HALE_I_MAGAZYNY,
            "garaz": CategoryEnum.GARAZE_I_PARKINGI
        }
        if category not in mapper:
            return CategoryEnum.POZOSTALE
        return mapper[category]

    @staticmethod
    def __map_sub_category(sub_category: str) -> str:
        """
        Maps a sub-category string to its corresponding enum value.

        Args:
            sub_category (str): Input sub-category string.

        Returns:
            str: Corresponding enum value for the sub-category.
        """
        mapper = {
            "wynajem": SubCategoryEnum.WYNAJEM,
            "sprzedaz": SubCategoryEnum.SPRZEDAZ,
        }
        return mapper[sub_category]

    @staticmethod
    def __process_price(full_price: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Processes the full price string to extract price and rent information.

        Args:
            full_price (str): Full price string.

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: Tuples containing processed price and rent information.
        """

        price, rent = None, None

        if "+" in full_price:
            pattern = re.compile(r'\b\d+\b')
            matches = pattern.findall(full_price)
            result = [int(match) for match in matches]
            price, rent = result[0], result[1]
        else:
            pattern = re.compile(r'\b\d+\b')
            match = pattern.search(full_price)
            result = int(match.group() if match else None)
            price = result

        processed_price = {"price": price, "currency": "zł"}
        processed_rent = {"rent": rent, "currency": "zł/miesiac"}

        return processed_price, processed_rent

    def parse(self, data, *args, **kwargs) -> Optional[List[Offer]]:
        """
        Parses the HTML content to extract relevant offer information.

        Args:
            data (str): HTML content to be parsed.
        Kwargs:
            category (str): Category of the offer.
            sub_category (str): Sub-category of the offer.
        Returns:
            List[Offer]: List of parsed offer objects.
        """
        category, sub_category = kwargs.get("category"), kwargs.get("sub_category")

        content = data
        soup = BeautifulSoup(content, "html.parser")
        offers = soup.find_all("article")

        # Return if there is no offers
        if not offers:
            return

        parsed_offers = []

        for offer in offers:
            url = offer.find("a", {"data-testid": "listing-item-link"})
            title = offer.find("p", {"data-cy": "listing-item-title"})

            # Return if there is no url or title
            if url is None or title is None:
                continue

            full_price = offer.find("span", class_="css-1uwck7i ewvgbgo0")
            full_location = offer.find("p", {"data-testid": "advert-card-address"})

            image_container = offer.find("div", class_="css-7wsc2v")
            images = []
            if image_container:
                img = image_container.find_all("img")
                for image in img:
                    images.append(image.get("src"))

            params = []
            dt_tags, dd_tags = soup.find_all('dt'), soup.find_all('dd')
            for dt_tag, dd_tag in zip(dt_tags, dd_tags):
                key = dt_tag.text.strip()
                value = dd_tag.text.strip()
                parsed_param = {"key": key, "value": value}
                params.append(parsed_param)

            if full_price:
                processed_price, processed_rent = self.__process_price(full_price.text)
            else:
                processed_price, processed_rent = {}, {}
            city, region = self.__get_city_region(full_location.text)
            location = Location(region=region.capitalize(), city=city)
            area = self.__string_to_int(self.__get_param_value(params, "Powierzchnia"))
            room_number = self.__string_to_int(self.__get_param_value(params, "Liczba pokoi"))
            floor = self.__string_to_int(self.__get_param_value(params, "Piętro"))
            full_url = f"otodom.pl{url.get("href")}"

            offer = Offer(
                title=title.text,
                url=full_url,
                category=self.__map_category(category),
                sub_category=self.__map_sub_category(sub_category),
                building_type=None,
                price=processed_price.get("price"),
                rent=processed_rent.get("rent"),
                description=None,
                price_per_meter=None,
                area=area,
                building_floor=None,
                floor=floor,
                room_number=room_number,
                has_furnitures=None,
                photos=images,
                location=location,
            )
            parsed_offers.append(offer)
        return parsed_offers
