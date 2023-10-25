# [WIP] Itsy bitsy spider

Web crawler and scraper

## Setup

1. Create virtual environment -- `python -m venv .venv`
2. Activate it -- `. .venv/bin/activate`
3. Install dependencies -- `pip install -r requirements.txt`
4. Explore directories with attempts to solve the problem/test task
5. In general, all scripts are run as `python <filename>.py --category="<category>" --location="<location>"`

## Usage

```shell
# with persistence support enabled, e.g. we can continue from where we left off and get only new businesses
scrapy crawl yelp -s JOBDIR=spiders/yelp -a category=Contractors -a location='San Francisco, CA' -o business_data.json

# Then, we can stop the spider safely at any time (by pressing Ctrl-C or sending a signal), and resume it later by issuing the same command
```
