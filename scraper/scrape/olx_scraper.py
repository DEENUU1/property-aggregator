from .scrape_strategy import ScrapeStrategy
from typing import Any, Dict, Optional
import requests
from service import olx_service
from data.olx import Olx
import json


class OlxScraper(ScrapeStrategy):
    __service = olx_service.OlxService()

    @staticmethod
    def __get_content(url: str) -> Optional[Dict[str, Any]]:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
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
    def __get_next_page_url(content: Dict[str, Any]) -> Optional[str]:
        links = content.get("links", None)
        if not links:
            return None
        next_url = links.get("next", None)
        if not next_url:
            return None
        url = next_url.get("href")
        return url

    def scrape(self):
        print("Run OLX scraper")

        CATEGORIES = {
            ("Mieszkanie",
             0): "https://www.olx.pl/api/v1/offers/?offset=40&limit=40&category_id=14&filter_refiners=spell_checker&sl=18c34ade124x23bc10a5",
            # TODO add url for each category and subcategory
            # ("Mieszkanie", 1): "https://www.olx.pl/api/v1/offers/?offset=80&limit=40&category_id=15&filter_refiners=spell_checker&sl=18c34ade124x23bc10a5",
            # ("Dom", 0): "",
            # ("Dom", 1): "",
            # ("Działka", 0): "",
            # ("Działka", 1): "",
            # ("Biura i lokale", 0): "",
            # ("Biura i lokale", 1): "",
            # ("Garaże i parkingi", 0): "",
            # ("Garaże i parkingi", 1): "",
            # ("Stancje i pokoje", 0): "",
            # ("Stancje i pokoje", 1): "",
            # ("Hale i magazyny", 0): "",
            # ("Hale i magazyny", 1): "",
            # ("Pozostałe", 0): "",
            # ("Pozostałe", 1): ""
        }

        for key, value in CATEGORIES.items():
            category, sub_category = key

            next_page = value
            while next_page:
                print(f"Scraping {next_page}")

                content = self.__get_content(next_page)
                if content:
                    data = Olx(category=category, sub_category=sub_category, data=json.dumps(content))
                    self.__service.create(data)
                    print("Save scraped data to MongoDB")

                next_page = self.__get_next_page_url(content)
                if not next_page:
                    break
