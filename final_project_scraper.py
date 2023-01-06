import scrapy
import time

# run with: scrapy runspider final_project_scraper.py
# run with to get an output.json file: scrapy runspider -o output.json final_project_scraper.py

# get all possible attributes of the products that can be useful for analysis
# collect products from all categories from all locations of auchan

class ProductSpider(scrapy.Spider):
    name = 'productspider'
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
        timestamp = time.time()

        for product in response.css('.product-thumbnail--column'):
            sponsored = False
            if product.css('.product-thumbnail__flaps'):
                sponsored = True
            yield {
                'ProductId': str(product.css('.product-thumbnail ::attr(data-id)').get()) + '_'+ str(timestamp), # consists of data-id from website and timestamp, to get a unique key
                'name': product.css('.product-thumbnail__description').css('p::text').get().replace('\n', '').strip(),
                'price': product.css('.product-price::text').get(),
                'base price': product.css('.product-price--old::text').get(),
                'unit': product.css('.product-thumbnail__attributes span::text').extract_first(),
                'image': product.css('.product-thumbnail__picture img::attr(src)').extract_first(),
                'link': product.css('.product-thumbnail__details-wrapper').css('a::attr(href)').extract_first(),
                'category path': category_path,
                'sponsored': sponsored,
                'availability': product.css('.delivery-promise ::text').get(),
                'brand': product.css('.product-thumbnail__description strong::text').get(),
                # add additional properties
                'discount': product.css('.product-discount--sticker ::text').get(),
                'label': product.css('.product-flap__label ::text').get(),
                'rating value': product.css('.gauge--star ::attr(value)').get(),
                'rating count': product.css('.rating-value__value--count ::text').get(),
                'sold by': product.css('.product-thumbnail__seller-label .bold::text').get(),
            }
        
        for next_page in response.css('.pagination-adjacent__link'):
            yield response.follow(next_page, self.parse_category)
