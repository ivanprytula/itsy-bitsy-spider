# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YelpBusinessItem(scrapy.Item):
    # Business details
    business_name = scrapy.Field()
    business_rating = scrapy.Field()
    num_reviews = scrapy.Field()
    business_yelp_url = scrapy.Field()
    business_website = scrapy.Field()

    # List of first 5 reviews
    reviews = scrapy.Field()


class YelpReviewItem(scrapy.Item):
    # Review details
    reviewer_name = scrapy.Field()
    reviewer_location = scrapy.Field()
    review_date = scrapy.Field()

    # class YelpdataItem(scrapy.Item):
    # define the fields for your item here like:
    # business_name = scrapy.Field()
    # business_rating = scrapy.Field()
    # number_of_reviews = scrapy.Field()
    # business_yelp_url = scrapy.Field()
    # business_website = scrapy.Field()
    # reviews = scrapy.Field()
