import scrapy
import time
from project.items import ProjectItem   

# run with: scrapy crawl product
# DEPRECATED: run with to get an output.json file: scrapy runspider -o output.json final_project_scraper.py

# get all possible attributes of the products that can be useful for analysis
# collect products from all categories from all locations of auchan

dict_of_locations_with_session_ids = {
    "Paris": "9a528be2-1584-4454-9c86-78fccb6bc51c",
    "Marseille": "cbaffc50-a5cb-428a-af62-ce0051d2081f",
    "Lyon": "e5f66048-fd40-4940-8c50-feca91e2a486",
    "Toulouse": "fad605f1-a083-4da8-a87a-771e3ce07b16",
    "Nice": "8e9b263b-007a-43fe-bd25-e6d2223de106",
    "Nantes": "050c3123-21aa-4d7c-8e08-4595b97536a7",
    "Montpellier": "63841ec3-40f5-411c-beea-ef50f60bfb16",
    "Strasbourg": "abcf0cd5-7976-48e1-8724-e74be47cb830",
    "Bordeaux": "d58bbea9-3659-4415-af44-d4e9b5684db1",
    "Lille": "954c715b-133e-47c6-a62a-0f2431dcc131"
}

class ProductSpider(scrapy.Spider):

    def __init__(self, **kwargs):
        self.name = 'product'
        self.start_urls = ['https://www.auchan.fr/nos-rayons']
        super().__init__(**kwargs)

    def parse(self, response):
        print(self.location)
        for sub_category in response.css('.universe-block__link.green-txt.bold'):
            # follow to all products from sub_category, additionally add cookie to set a preselected store
            yield response.follow(sub_category, self.parse_sub_category, cookies={"lark-journey": dict_of_locations_with_session_ids[self.location]})

    def parse_sub_category(self, response):
        categories = []
        category_part = response.css('.site-breadcrumb__nav')
        for category_part in category_part.css('.site-breadcrumb__item'):
            categories.append(category_part.css('a::text').get())
        print(categories)
        print()
        timestamp = time.time() % 1

        for product in response.css('.product-thumbnail--column'):
            sponsored = False
            if product.css('.product-thumbnail__flaps'):
                sponsored = True
            project_item = ProjectItem()
            project_item['ProductId'] = str(product.css('.product-thumbnail ::attr(data-id)').get()) + '_'+ str(timestamp) # consists of data-id from website and timestamp, to get a unique key
            project_item['name'] = product.css('.product-thumbnail__description').css('p::text').get().replace('\n', '').strip()
            project_item['price'] = product.css('.product-price::text').get()
            project_item['base_price'] = product.css('.product-price--old::text').get()
            project_item['unit'] = product.css('.product-thumbnail__attributes span::text').extract_first()
            project_item['image'] = product.css('.product-thumbnail__picture img::attr(src)').extract_first()
            project_item['link'] = product.css('.product-thumbnail__details-wrapper').css('a::attr(href)').extract_first()
            project_item['category_path'] = '/'.join(category for category in categories)
            project_item['sponsored'] = sponsored
            project_item['availability'] = product.css('.delivery-promise ::text').get()
            project_item['brand'] = product.css('.product-thumbnail__description strong::text').get()
            # add additional properties
            project_item['discount'] = product.css('.product-discount--sticker ::text').get()
            project_item['label'] = product.css('.product-flap__label ::text').get()
            project_item['rating_value'] = product.css('.gauge--star ::attr(value)').get()
            project_item['rating_count'] = product.css('.rating-value__value--count ::text').get()
            project_item['sold_by'] = product.css('.product-thumbnail__seller-label .bold::text').get()
            project_item['location'] = response.css('.context-header__pos::text').get()
            yield project_item
        
        for next_page in response.css('.pagination-adjacent__link'):
            yield response.follow(next_page, self.parse_sub_category)