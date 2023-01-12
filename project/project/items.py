# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ProjectItem(Item):
    ProductId = Field()
    name = Field()
    price = Field()
    base_price= Field() 
    unit = Field()
    image= Field()
    link= Field()
    category_path = Field()
    sponsored= Field()
    availability = Field()
    brand= Field()
    discount= Field()
    label= Field()
    rating_value= Field()
    rating_count= Field()
    sold_by = Field()
    location = Field()
