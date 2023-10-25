# flake8: noqa
import asyncio

import httpx
from icecream import ic

BASE_SEARCH_URL = "https://www.yelp.com/search?find_desc={}&find_loc={}"
SEARCH_SNIPPET_URL = (
    "https://www.yelp.com/search/snippet?find_desc={}&find_loc={}&parent_request_id{}=&request_origin={}&start={}"
)

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.55"
}


BASE_HEADERS = {
    "authority": "www.yelp.com",
    "user-agent": headers["User-Agent"],
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "accept-language": "en-US;en;q=0.9",
    "accept-encoding": "gzip, deflate, br",
}


async def _search_yelp_page(category: str, location: str, client: httpx.AsyncClient, offset=0):
    # final url example:
    # https://www.yelp.com/search/snippet?find_desc=plumbers&find_loc=Toronto%2C+Ontario%2C+Canada&ns=1&start=210&parent_request_id=54233ce74d09d270&request_origin=user
    resp = await client.get(
        "https://www.yelp.com/search/snippet",
        params={
            "find_desc": category,
            "find_loc": location,
            "start": offset,
            "parent_request_id": "",
            "request_origin": "user",
        },
    )
    assert resp.status_code == 200
    ic(resp)  # OK
    return resp.json()


async def run():
    async with httpx.AsyncClient(headers=BASE_HEADERS, http2=True) as client:
        category = "contractors"
        location = "San Francisco, CA"
        results = await _search_yelp_page(category, location, client=client)


if __name__ == "__main__":
    asyncio.run(run())
