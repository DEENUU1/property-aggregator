import requests
from bs4 import BeautifulSoup
from typing import List, Optional

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"


def get_content(category: str, type_: str, page_num: int = 1):
    url = f"https://www.otodom.pl/pl/wyniki/{type_}/{category}/cala-polska?viewType=listing&page={page_num}"
    try:
        response = requests.get(url, headers={"User-Agent": USER_AGENT})
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


def is_next_page(content: str) -> bool:
    soup = BeautifulSoup(content, "html.parser")
    next_button = soup.find("li", {"aria-label": "Go to next Page"})
    if next_button:
        return True
    return False


if __name__ == "__main__":
    CATEGORIES = ["mieszkanie", "kawalerka", "dom", "inwestycja", "pokoj", "dzialka", "lokal", "haleimagazyny", "garaz"]
    TYPE = ["wynajem", "sprzedaz"]

    for t in TYPE:
        for category in CATEGORIES:
            page_num = 1
            init_content = get_content(
                category=category,
                type_=t,
                page_num=page_num
            )

            next_page = is_next_page(init_content)
            while is_next_page:
                content = get_content(
                    category=category,
                    type_=t,
                    page_num=page_num
                )
                next_page = is_next_page(content)
                page_num += 1
                print(page_num)
