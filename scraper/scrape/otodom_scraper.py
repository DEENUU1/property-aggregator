from .scrape_strategy import ScrapeStrategy
import requests
from bs4 import BeautifulSoup
from typing import Optional
from data.otodom import Otodom
from service.otodom_service import OtodomService


class OtodomScraper(ScrapeStrategy):
    __service = OtodomService()

    __USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
    __CATEGORIES = ["mieszkanie", "kawalerka", "dom", "inwestycja", "pokoj", "dzialka", "lokal", "haleimagazyny",
                  "garaz"]
    __TYPE = ["wynajem", "sprzedaz"]

    def __get_content(self, category: str, type_: str, page_num: int = 1) -> Optional[str]:
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
        soup = BeautifulSoup(content, "html.parser")
        next_button = soup.find("li", {"aria-label": "Go to next Page"})
        if next_button:
            return True
        return False

    def scrape(self) -> None:
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

