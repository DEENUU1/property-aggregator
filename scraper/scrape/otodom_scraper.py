from .scrape_strategy import ScrapeStrategy
import requests
from bs4 import BeautifulSoup
from typing import Optional
from data.otodom import Otodom
from service.otodom_service import OtodomService


class OtodomScraper(ScrapeStrategy):
    """
    OtodomScraper class for scraping data from Otodom website.

    Attributes:
        __service (OtodomService): An instance of OtodomService.
        __USER_AGENT (str): User agent string for HTTP requests.
        __CATEGORIES (list): List of available categories on Otodom.
        __TYPE (list): List of available types (rental/sale) on Otodom.
    """

    __service = OtodomService()

    __USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
    __CATEGORIES = ["mieszkanie", "kawalerka", "dom", "inwestycja", "pokoj", "dzialka", "lokal", "haleimagazyny",
                  "garaz"]
    __TYPE = ["wynajem", "sprzedaz"]

    def __get_content(self, category: str, type_: str, page_num: int = 1) -> Optional[str]:
        """
        Get content from a specified Otodom URL.

        Args:
            category (str): The category of the property.
            type_ (str): The type of transaction (rental/sale).
            page_num (int): The page number to scrape. Defaults to 1.

        Returns:
            Optional[str]: The scraped content as a string, or None if failed.
        """
        url = f"https://www.otodom.pl/pl/wyniki/{type_}/{category}/cala-polska?viewType=listing&page={page_num}"
        try:
            response = requests.get(url, headers={"User-Agent": self.__USER_AGENT})
            response.raise_for_status()
            return response.text
        except requests.exceptions.HTTPError as e:
            print(e)
            return None
        except requests.exceptions.RequestException as e:
            print(e)
            return None
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def __is_next_page(content: str) -> bool:
        """
        Check if there's a next page in the scraped content.

        Args:
            content (str): The scraped content.

        Returns:
            bool: True if there's a next page, False otherwise.
        """
        soup = BeautifulSoup(content, "html.parser")
        next_button = soup.find("li", {"aria-label": "Go to next Page"})
        if next_button:
            return True
        return False

    def scrape(self) -> None:
        """Scrape data from Otodom."""
        for t in self.__TYPE:
            for category in self.__CATEGORIES:
                page_num = 1
                next_page = True
                while next_page:
                    print(f"Scrape {page_num} page of {category} {t} data from otodom.pl")

                    content = self.__get_content(
                        category=category,
                        type_=t,
                        page_num=page_num
                    )
                    if content:
                        data = Otodom(category=category, sub_category=t, data=content)
                        self.__service.create(data)
                        print("Content saved to MongoDB")

                    next_page = self.__is_next_page(content)
                    page_num += 1

