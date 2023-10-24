from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from yelpdata.items import YelpBusinessItem


class YelpSpider(CrawlSpider):
    name = "yelp"
    allowed_domains = ["yelp.com"]
    # start_urls = ["https://www.yelp.com"]
    # https://www.yelp.com/search?find_desc={self.category}&find_loc={self.location}

    # def start_requests(self):
    #     yield Request(f"https://www.yelp.com/search?find_desc={self.category}&find_loc={self.location}")
    def __init__(self, category=None, location=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [f"https://www.yelp.com/search?find_desc={category}&find_loc={location}"]

    # In this case, we follow all the links within pagination breadcrumbs
    # And call the "parse_business" method on every crawled page, 10 results/page x 24 p.
    rules = (
        Rule(LinkExtractor(restrict_css="div[role='navigation']"), follow=True),
        Rule(LinkExtractor(restrict_css="h3 a"), callback="parse_business"),
    )

    def parse_business(self, response):
        self.logger.info("Hi, this is an item page! %s", response.url)

        # Extract business details from response
        business_name = ...
        business_rating = ...
        num_reviews = ...
        business_yelp_url = ...
        business_website = ...

        # Create YelpBusinessItem instance
        business_item = YelpBusinessItem(
            business_name=business_name,
            business_rating=business_rating,
            num_reviews=num_reviews,
            business_yelp_url=business_yelp_url,
            business_website=business_website,
        )

        # Yield the item
        yield business_item
