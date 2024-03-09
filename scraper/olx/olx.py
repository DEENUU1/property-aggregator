import requests
from typing import Any, List, Dict, Optional

BASE_URL = "https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=3&filter_refiners=spell_checker&sl=18c34ade124x23bc10a5"


def get_content(url):
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


def get_next_page_url(content: Dict[str, Any]) -> Optional[str]:
    links = content.get("links", None)
    if not links:
        return None
    next_url = links.get("next", None)
    if not next_url:
        return None
    return next_url.get("href")


def run():

    init_page = get_content(BASE_URL)
    next_page = get_next_page_url(init_page)

    while next_page:
        content = get_content(next_page)
        next_page = get_next_page_url(content)
        if not next_page:
            break
        print(next_page)



if __name__ == "__main__":
    run()