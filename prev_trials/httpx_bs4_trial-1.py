import argparse
import asyncio
import json

import httpx
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from icecream import ic

SAMPLE_LOCATIONS = [
    "San Francisco, CA",
    "Palo Alto, CA",
    "Oakland, CA",
    "New York, NY",
    "San Carlos, CA",
    "Seattle, WA",
]
SAMPLE_CATEGORIES = ["contractors", "restaurants", "electricians", "nightlife", "delivery", "reservations"]

BASE_SEARCH_URL = "https://www.yelp.com/search?find_desc={}&find_loc={}"
SEARCH_SNIPPET_URL = (
    "https://www.yelp.com/search/snippet?find_desc={}&find_loc={}&parent_request_id{}=&request_origin={}&start={}"
)

BASE_HEADERS = {"User-Agent": UserAgent().random}


def parse_search_keywords() -> tuple:
    parser = argparse.ArgumentParser(
        description="Web scraping script",
        epilog="Thanks for using %(prog)s! :)",
    )
    parser.add_argument("--category", help="Category name, i.e. contractors")
    parser.add_argument("--location", help="Location, i.e. San Francisco, CA")

    args = parser.parse_args()
    return args.category, args.location


def get_search_results_page(client: httpx.Client, category: str, location: str) -> BeautifulSoup:
    response = client.get("https://www.yelp.com/search", params={"find_desc": category, "find_loc": location})
    soup = BeautifulSoup(response.content, "lxml")
    return soup


def get_search_results_from_api(
    client: httpx.Client, category: str, location: str, offset=0, parent_request_id="", request_origin="user"
) -> dict:
    response = client.get(
        "https://www.yelp.com/search/snippet",
        params={
            "find_desc": category,
            "find_loc": location,
            "start": offset,
            "parent_request_id": parent_request_id,
            "request_origin": request_origin,
        },
    )

    # Assuming response.content contains valid JSON data
    if response.status_code == 200:
        return json.loads(response.content.decode("utf-8"))


async def main(category: str, location: str):
    async with httpx.AsyncClient(headers=BASE_HEADERS, http2=True, timeout=10, follow_redirects=True) as client:

        offset = 0
        parent_request_id = ""
        request_origin = "user"

        response = await client.get(
            "https://www.yelp.com/search/snippet",
            params={
                "find_desc": category,
                "find_loc": location,
                "start": offset,
                "parent_request_id": parent_request_id,
                "request_origin": request_origin,
            },
        )

        breakpoint()
        ic(response)

        if response.status_code == 200:
            with open("output-2.json", "w") as file:
                json.dump(response.json(), file, indent=4)


if __name__ == "__main__":
    category, location = parse_search_keywords()

    asyncio.run(main(category, location))
