import scrapy
import pandas as pd

# run with: scrapy runspider final_project_scraper.py

# get all possible attributes of the products that can be useful for analysis
# collect products from all categories from all locations of auchan

class ProductSpider(scrapy.Spider):
    name = 'productspider'
    start_urls = ['https://www.auchan.fr']
    df = pd.DataFrame({"name": []
    })
    category_path = None

    def parse(self, response):
        # for each category go through all products
        for category in response.css('.navigation-layer__link'):
            self.category_path = category.css('a::attr(href)').extract_first()
            yield response.follow(category, self.parse_category)
            #{'category': category.css('::text').get()}


    
    def parse_category(self, response):
        for product in response.css('.product-thumbnail--column'):
            yield {
                'name': product.css('.product-thumbnail__description').css('p::text').get(),
                'price': product.css('.product-price').css('::text').get(), # sometimes None
                'base price': product.css('.product-price--old').css('::text').get(), # sometimes None, for example if sth is not sold anymore
                'unit': product.css('.product-thumbnail__attributes').css('span::text').get(), # 2 coloris, what to do with results without piece?
                'image': product.css('.product-thumbnail__picture img::attr(src)').extract_first(), # somehow the results do not always have an image
                'link': product.css('.product-thumbnail__details-wrapper').css('a::attr(href)').extract_first(),
                #'category path': self.category_path,
                'sponsored': product.css('.discount_markups').get(),
                #'availability':delivery-promise,
                'brand': product.css('.product-thumbnail__description').css('strong::text').get(),
                'discount': product.css('.product-discount--sticker').css('::text').get(),
                'label': product.css('.product-flap__label').css('::text').get(),
                'rating value': product.xpath('//meta[@itemprop="ratingValue"]/@content').extract_first(), # only chooses the first value of the products
                #'rating value': product.css('.gauge--star').attrib['value'],
                'rating count': product.css('.rating-value__value--count').css('::text').get(),
                #'sold by': 'product-thumbnail__marketplace-label-link'
            }
