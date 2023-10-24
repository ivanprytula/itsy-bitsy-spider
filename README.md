# [WIP] Itsy bitsy spider

Web crawler and scraper

## Setup

1. Create virtual environment -- `python -m venv .venv`
2. Activate it -- `. .venv/bin/activate`
3. Install dependencies -- `pip install -r requirements.txt`
4. Explore directories with attempts to solve the problem/test task
5. In general, all scripts are run as `python <filename>.py --category="<category>" --location="<location>"`

## WIP

The main problem with accessing Yelp API search endpoint (the one that holds most of the "easy to get data") is the following:
Response in a huge JSON object with (oven 10K lines) and the only way I managed to did request is to spawn subprocess with cURL library.
