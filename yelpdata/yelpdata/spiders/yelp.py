# flake8: noqa

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from yelpdata.items import YelpBusinessItem, YelpReviewItem
import scrapy
from pathlib import Path
from scrapy.shell import inspect_response

FLOAT_POINT_NUMBER_REGEX = r"[-+]?([0-9]*\.[0-9]+|[0-9]+)"


class YelpSpider(CrawlSpider):
    name = "yelp"
    allowed_domains = ["yelp.com"]
    # custom_settings = {'DEPTH_LIMIT': 1}
    # https://www.yelp.com/search?find_desc={self.category}&find_loc={self.location}

    def __init__(self, category=None, location=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [f"https://www.yelp.com/search?find_desc={category}&find_loc={location}"]

    # In this case, we follow all the links within pagination breadcrumbs
    # And call the "parse_business" method on every crawled page, 10 results/page x 24 p.
    rules = (
        Rule(LinkExtractor(restrict_css="div[role='navigation']"), follow=True),
        Rule(LinkExtractor(restrict_css="h3 span a"), callback="parse_business"),
    )

    def parse_business(self, response):
        self.logger.info("Hi, this is an business page! %s", response.url)

        business_name = response.xpath("normalize-space(//h1/text())").get()
        business_rating = response.xpath('(//main//div[starts-with(@class, "five-stars")])[1]/@aria-label').re_first(
            FLOAT_POINT_NUMBER_REGEX
        )
        num_reviews = response.xpath("//a[@href='#reviews']/text()").re_first(r"\d+")
        business_yelp_url = response.url
        business_website = response.xpath(
            "//p[contains(text(),'Business website')]/following-sibling::p/a/text()"
        ).get()

        # NB: https://docs.scrapy.org/en/latest/topics/selectors.html?highlight=extract_first#beware-of-the-difference-between-node-1-and-node-1
        reviews_raw = response.xpath('(//section[contains(@aria-label, "Recommended Reviews")]//ul)[2]/li')
        reviews_list = []

        for review in reviews_raw[:5]:
            inspect_response(response, self)
            reviewer_name = review.xpath('.//div[contains(@class, "user-passport-info")]//a/text()').get()
            reviewer_location = review.xpath(
                './/div[contains(@class, "user-passport-info")]//div//span/text()'
            ).get()
            review_date = review.xpath('.//div[starts-with(@class, "arrange-unit")][last()]/span/text()').get()

            review_item = YelpReviewItem(
                reviewer_name=reviewer_name, reviewer_location=reviewer_location, review_date=review_date
            )
            reviews_list.append(review_item)

        yield YelpBusinessItem(
            business_name=business_name,
            business_rating=business_rating,
            num_reviews=num_reviews,
            business_yelp_url=business_yelp_url,
            business_website=business_website,
            reviews=reviews_list,
        )
