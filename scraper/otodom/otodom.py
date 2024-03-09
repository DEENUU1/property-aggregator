from dataclasses import dataclass
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"


@dataclass
class Param:
    key: str
    value: str


@dataclass
class Offer:
    url: str
    title: str
    full_price: Optional[str] = None
    full_location: Optional[str] = None
    images: List[Optional[str]] = None
    params: List[Optional[Param]] = None


def get_content(category: str, type_: str, page_num: int = 1) -> Optional[str]:
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


def parse_page(content: str) -> List[Optional[Offer]]:
    soup = BeautifulSoup(content, "html.parser")
    offers = soup.find_all("article")

    parsed_offers = []

    if not offers:
        return parsed_offers

    for offer in offers:
        url = offer.find("a", {"data-testid": "listing-item-link"})
        title = offer.find("p", {"data-cy": "listing-item-title"})

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

        dt_tags = soup.find_all('dt')
        dd_tags = soup.find_all('dd')
        for dt_tag, dd_tag in zip(dt_tags, dd_tags):
            key = dt_tag.text.strip()
            value = dd_tag.text.strip()
            parsed_param = Param(key=key, value=value)
            params.append(parsed_param)

        offer = Offer(
            url=url,
            title=title,
            full_price=full_price,
            full_location=full_location,
            images=images,
            params=params
        )
        parsed_offers.append(offer)

    return parsed_offers


if __name__ == "__main__":
    CATEGORIES = ["mieszkanie", "kawalerka", "dom", "inwestycja", "pokoj", "dzialka", "lokal", "haleimagazyny", "garaz"]
    TYPE = ["wynajem", "sprzedaz"]

    init_content = get_content(
        category=CATEGORIES[0],
        type_=TYPE[0],
    )
    parsed_page = parse_page(init_content)
    print(parsed_page)
    # for t in TYPE:
    #     for category in CATEGORIES:
    #         page_num = 1
    #         init_content = get_content(
    #             category=category,
    #             type_=t,
    #             page_num=page_num
    #         )
    #
    #         next_page = is_next_page(init_content)
    #         while is_next_page:
    #             content = get_content(
    #                 category=category,
    #                 type_=t,
    #                 page_num=page_num
    #             )
    #             next_page = is_next_page(content)
    #             page_num += 1
    #             print(page_num)
