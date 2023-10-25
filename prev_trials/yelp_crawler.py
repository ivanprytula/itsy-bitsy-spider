# flake8: noqa
import argparse
import asyncio
import json
import logging
from typing import Dict, List, Tuple
import subprocess

import httpx
from fake_useragent import UserAgent
from icecream import ic  # noqa
from parsel import Selector

logging.basicConfig(
    format="%(levelname)s [%(asctime)s] %(name)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG
)

BASE_HEADERS = {
    "authority": "www.yelp.com",
    "user-agent": UserAgent().random,
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "en-US;en;q=0.9",
    "accept-encoding": "gzip, deflate, br",
}

SEARCH_SNIPPET_URL = "https://www.yelp.com/search/snippet"


def parse_search_keywords() -> tuple:
    parser = argparse.ArgumentParser(
        description="Web scraping script",
        epilog="Thanks for using %(prog)s! :)",
    )
    parser.add_argument("--category", help="Category name, i.e. contractors")
    parser.add_argument("--location", help="Location, i.e. San Francisco, CA")

    args = parser.parse_args()
    return args.category, args.location


def parse_search(search_results: Dict) -> Tuple[List[Dict], Dict]:
    results = search_results.get("searchPageProps").get("mainContentComponentsListProps")
    businesses = [r for r in results if r.get("searchResultBusiness") and not r.get("adLoggingInfo")]
    search_meta = next(r for r in results if r.get("type") == "pagination")["props"]
    return businesses, search_meta


async def _search_on_one_page(keyword: str, location: str, session: httpx.AsyncClient, offset=0):
    """scrape single page of yelp search"""
    # final url example:
    # https://www.yelp.com/search/snippet?find_desc=contractors&find_loc=San%20Francisco%2C&start=&parent_request_id=&request_origin=user
    response = await session.get(
        SEARCH_SNIPPET_URL,
        params={
            "find_desc": keyword,
            "find_loc": location,
            "start": offset,
            "parent_request_id": "",
            "request_origin": "user",
        },
    )
    assert response.status_code == 200
    # breakpoint()

    if response.status_code == 200:
        # Process the response content incrementally
        buffer = b""
        async for chunk in response.aiter_bytes():
            buffer += chunk

            # Check if the buffer contains a complete JSON object
            try:
                json_data = json.loads(buffer.decode("utf-8"))
                # Do something with the JSON data (e.g., save to a file)
                buffer = b""  # Clear the buffer
                return json_data
            except json.JSONDecodeError:
                try:
                    curl_command = f'curl -s "https://www.yelp.com/search/snippet?find_desc={keyword}&find_loc=San+Francisco%2C+CA%2C+United+States&start={offset}&parent_request_id=&request_origin=user"'
                    ic(curl_command)
                    completed_process = subprocess.run(
                        curl_command, shell=True, check=True, capture_output=True, text=True
                    )
                    return completed_process.stdout
                except subprocess.CalledProcessError as e:
                    logging.error(f"Error executing curl: {e.stderr}")

                pass  # Incomplete JSON, continue accumulating data

        else:
            logging.error(f"Error: {response.status_code}")


async def search_all_pages(category: str, location: str, session: httpx.AsyncClient):
    """Scrape all pages in order to get business preview data."""
    first_page = await _search_on_one_page(category, location, session=session)
    ic(first_page)

    first_page = json.loads(first_page)

    # grab 1st page + total num of pages
    businesses, search_meta = parse_search(first_page)

    tasks = []
    for page in range(10, search_meta["totalResults"], 10):
        tasks.append(_search_on_one_page(category, location, session=session, offset=page))

    for result in await asyncio.gather(*tasks):
        businesses.extend(parse_search(result)[0])
    return businesses


def parse_company(resp: httpx.Response):
    sel = Selector(text=resp.text)
    xpath = lambda xp: sel.xpath(xp).get(default="").strip()  # noqa

    return dict(
        name=xpath("//h1/text()"),
        website=xpath('//p[contains(text(),"Business website")]/following-sibling::p/a/text()'),
    )


async def run_crawler(category, location):
    timeout = httpx.Timeout(10.0, connect=60.0)
    limits = httpx.Limits(max_connections=10, keepalive_expiry=None)
    async with httpx.AsyncClient(
        headers=BASE_HEADERS, http2=True, timeout=timeout, follow_redirects=True, limits=limits
    ) as session:
        results = await search_all_pages(category, location, session=session)

        with open("output-2.json", "w") as file:
            json.dump(results, file, indent=4)


if __name__ == "__main__":
    category, location = parse_search_keywords()

    asyncio.run(run_crawler(category, location))
