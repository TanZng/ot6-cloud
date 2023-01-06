import scrapy
import time
from project.items import ProjectItem   

# run with: scrapy crawl product
# DEPRECATED: run with to get an output.json file: scrapy runspider -o output.json final_project_scraper.py

# get all possible attributes of the products that can be useful for analysis
# collect products from all categories from all locations of auchan

class ProductSpider(scrapy.Spider):
    name = 'product'
    start_urls = ['https://www.auchan.fr']
    # start_urls = ['https://www.auchan.fr/nos-magasins?types=SUPER']

    def parse(self, response):
        # for each category go through all products
        for category in response.css('.navigation-layer__link'):
            yield response.follow(category, self.parse_category)
    
    def parse_category(self, response):
        for sub_category in response.css('.universe-block__link.green-txt.bold'):
            yield response.follow(sub_category, self.parse_sub_category)

    def parse_sub_category(self, response):
        category_path = response.css('.site-breadcrumb__title--ellipsis a::text').get()
        print(category_path)
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
            project_item['category_path'] = category_path
            project_item['sponsored'] = sponsored
            project_item['availability'] = product.css('.delivery-promise ::text').get()
            project_item['brand'] = product.css('.product-thumbnail__description strong::text').get()
            # add additional properties
            project_item['discount'] = product.css('.product-discount--sticker ::text').get()
            project_item['label'] = product.css('.product-flap__label ::text').get()
            project_item['rating_value'] = product.css('.gauge--star ::attr(value)').get()
            project_item['rating_count'] = product.css('.rating-value__value--count ::text').get()
            project_item['sold_by'] = product.css('.product-thumbnail__seller-label .bold::text').get()
            yield project_item
        
        for next_page in response.css('.pagination-adjacent__link'):
            yield response.follow(next_page, self.parse_category)
