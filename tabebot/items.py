# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field


class ReviewItem(Item):
    user_id = Field()
    business_id = Field()
    review_id = Field()
    stars_dinner = Field()
    stars_lunch = Field()
    visit = Field()
    text = Field()
    title = Field()
    situations = Field()
    price_dinner = Field()
    price_lunch = Field()


class BusinessItem(Item):
    business_id = Field()
    name = Field()
    categories = Field()
    stars = Field()
    stars_dinner = Field()
    stars_lunch = Field()
    review_count = Field()
    prefecture = Field()
    area = Field()
    subarea = Field()
    price_dinner = Field()
    price_lunch = Field()
    menu_items = Field()


class UserItem(Item):
    user_id = Field()
    name = Field()
    review_count = Field()
    profile = Field()
    verified = Field()


class MenuItem(Item):
    name = Field()
    explanation = Field()
    price = Field()
