# Itsy bitsy spider

Web crawler and scraper

## Setup

1. Create virtual environment -- `python -m venv .venv`
2. Activate it -- `. .venv/bin/activate`
3. Install dependencies -- `pip install -r requirements.txt`
4. Explore directories with attempts to solve the problem/test task -- `prev_trials`

## Usage

```shell
cd yelpdata

# with persistence support enabled, e.g. we can continue from where we left off and get only new businesses
scrapy crawl yelp -s JOBDIR=spiders/yelp -a category=Contractors -a location='San Francisco, CA' -o business_data.json
scrapy crawl yelp -a category=reservations -a location='Oakland, CA' -o reservations_business_data.json
scrapy crawl yelp -a category=electricians -a location='Seattle, WA' -o electricians_business_data.json

# Then, we can stop the spider safely at any time (by pressing Ctrl-C or sending a signal), and resume it later by issuing the same command
```

To scrape limited number of pages change values of these configs in `yelpdata/settings.py`:

```python
CLOSESPIDER_PAGECOUNT = 3
CLOSESPIDER_ITEMCOUNT = 25
DUPEFILTER_CLASS = "scrapy.dupefilters.BaseDupeFilter"

# ------------------------
SAMPLE_LOCATIONS = [
    "San Francisco, CA",
    "Palo Alto, CA",
    "Oakland, CA",
    "New York, NY",
    "San Carlos, CA",
    "Seattle, WA",
]
SAMPLE_CATEGORIES = ["contractors", "restaurants", "electricians", "nightlife", "delivery", "reservations"]

```

### WIP

There is also a possibility to get some data faster via API calls. For instance, endpoint below is triggered "under the hood" when we hit search button on UI or paginate.
This endpoint (and similar ones) returns huge nested response - ~over 300 KB and 13K lines. We can paginate and take desired information faster that doing so via direct HTML parsing.
`https://www.yelp.com/search/snippet?find_desc=Contractors&find_loc=San+Francisco%2C+CA%2C+United+States&start=10&parent_request_id=229fe09c0fbca1e3&request_origin=user`
As such response is very cumbersome to work with it requires extra steps and efforts to pick desired data.
To be said, this endpoint also triggered with `Referrer Policy: strict-origin-when-cross-origin` so we need to take care of it also in order to overcome this, e.g. use other cli HTTP client.
