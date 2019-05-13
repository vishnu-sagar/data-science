from scrapy.http import Request
import scrapy
from flip import settings

product=settings.product
print("FETCHING DETAILS")

class GoodsSpider(scrapy.Spider):
    name = 'flip_spider'
    
    def start_requests(self):
        
        yield Request(url='https://www.flipkart.com/search?q='+product, callback=self.parse_flipkart)

    def parse_flipkart(self, response):
        path='https://www.flipkart.com'
        Noresult= response.xpath('//div[contains(text(),"Sorry")]/text()').extract_first()
        #print(Noresult+"yes")
        if Noresult!=None:
            print(Noresult+"Please try correcting your spelling")
            yield {'Website':'Website','Stock':'Stock status','Product':'Product Name','Rating':'Rating','Original Price':'Original_price','Current Price':'Current_price','LINK':'link'}
            yield {'Website':'Flipkart','Stock':Noresult,'Product':'None','Rating':'None','Original Price':'None','Current Price':'None','LINK':'None'}
        else:
         items=response.xpath('//div[@data-id]')
         #print(items)
         for item in items:
            text=item.xpath('.//div/text()').extract()
            #print(text)
            if '₹' in text:
                current_price=text[text.index('₹')-1]
                original_price=text[text.index('₹')+1]
            else:
                current_price=text[2]
                original_price=current_price
            link=path+item.xpath('.//*/@href')[0].extract()
            Rating=item.xpath('.//span[contains(@id,"productRating")]/div/text()').extract()
            status=item.xpath('.//div[contains(@style,"grayscale")]').extract_first()
            #print(status)
            if status!=None:
             stock="product out of stock"
            else:
             stock="IN STOCK"
            #print(Rating)
            if Rating==[]:
                Rating='NO Rating available'
            else:
                Rating=Rating[0]
            if Rating in text:
                text.remove(Rating)
            if text[0]=='ON OFFER':
             title=item.xpath('.//*/@alt').extract_first()
            else:
                title=title=item.xpath('.//div/a/@title').extract_first()
            break  
            #print(stock)
         yield {'Website':'Website','Stock':'Stock status','Product':'Product Name','Rating':'Rating','Original Price':'Original_price','Current Price':'Current_price','LINK':'link'}
         yield {'Website':'Flipkart','Stock':stock,'Product':title,'Rating':Rating,'Current Price':current_price,'Original Price':original_price,'LINK':link}
        yield Request(url='https://www.amazon.in/s?k='+product, callback=self.parse_amazon)

    def parse_amazon(self, response):
         results=response.xpath('//h1[@id="noResultsTitle"]/text()').extract_first()
         #Noresult=results[0]+product+results[1]
         #print(Noresult)
         if results!=None:
            Noresult=results[0]+product+results[1]
            print(Noresult+"Please try correcting your spelling")
            yield {'Website':'Amazon.in','Stock':Noresult,'Product':'None','Rating':'None','Original Price':'None','Current Price':'None','LINK':'None'}
         else:
          link=response.xpath('//div/a[@class="a-link-normal a-text-normal"]/@href').extract_first()
          #print(response.xpath('//h2/text()'))
          title=response.xpath('//h2/text()').extract_first()
          rating=response.xpath('//i[contains(@class,"a-icon-star")]/span/text()').extract_first()
          original_price=response.xpath('//*[contains(@class,"strike")]/text()').extract_first()
          current_price= response.xpath('//*[contains(@class,"price")]/text()').extract_first()
          stock="IN STOCK"
          yield {'Website':'Amazon.in','Stock':stock,'Product':title,'Rating':rating,'Current Price':current_price,'Original Price':original_price,'LINK':link}
         yield Request(url='https://www.snapdeal.com/search?keyword='+product, callback=self.parse_snap)
    
    def parse_snap(self,response):
        Noresult=response.xpath('//span[@class="alert-heading"]/text()').extract_first()
        if Noresult!=None:
            print(Noresult+"Please try correcting your spelling")
            yield {'Website':'Snapdeal','Stock':Noresult,'Product':'None','Rating':'None','Original Price':'None','Current Price':'None','LINK':'None'}
        else:
         link=response.xpath('//a[@pogid]/@href').extract_first()
         title=response.xpath('//div[@class="product-desc-rating "]/a/p/text()').extract_first()
         current_price=response.xpath('//span[contains(@class,"product-price")]/text()').extract_first()
         original_price=response.xpath('//span[contains(@class,"product-desc-price")]/text()').extract_first()
         rating='NO rating available'
         stock="IN STOCK"
         yield {'Website':'Snapdeal','Stock':stock,'Product':title,'Rating':rating,'Current Price':current_price,'Original Price':original_price,'LINK':link}
        yield Request(url='https://www.shopclues.com/search?q='+product, callback=self.parse_shop)
        
    def parse_shop(self,response):
        s=product.split(' ')
        j='%20'.join(s)
        Noresult= response.xpath('//span[@class="no_fnd"]/text()').extract_first()
        if Noresult!=None:
            print(Noresult+"Please try correcting your spelling")
            yield {'Website':'Shopclues','Stock':Noresult,'Product':'None','Rating':'None','Original Price':'None','Current Price':'None','LINK':'None'}
        else:
         link=response.xpath('//div[@class="column col3 search_blocks"]/a/@href').extract_first()
         title=response.xpath('//h2/text()').extract_first()
         current_price=response.xpath('//div[@class="ori_price"]/span/text()').extract_first()
         ref=response.xpath('//div[@class="refurbished_i"]/text()').extract_first()
         if ref=='Refurbished':
            original_price=current_price
         else:
            original_price=response.xpath('//div[@class="old_prices"]/span/text()').extract_first()
         rating='NO rating available'
         stock="IN STOCK"
         yield {'Website':'Shopclues.com','Stock':stock,'Product':title,'Rating':rating,'Current Price':current_price,'Original Price':original_price,'LINK':link} 
        yield Request(url='https://paytmmall.com/shop/search?q='+j+'&from=organic&child_site_id=6', callback=self.parse_paytm)
        
    def parse_paytm(self,response):
        path='https://paytmmall.com'
        Noresult= response.xpath('//span[contains(text(),"Sorry")]/text()').extract_first()
        #print(Noresult)
        if Noresult!=None:
            print(Noresult+"Please try correcting your spelling")
            yield {'Website':'Paytmmall','Stock':'None','Product':'None','Rating':'None','Original Price':'None','Current Price':'None','LINK':'None'}
        else:
         items=response.xpath('//div[@class="_2i1r"]')[0]
         #print(items.extract())
         current_price=items.xpath('.//div[@class="_1kMS"]/span/text()').extract_first()
         #print(current_price)
         #print(items.xpath('.//div[@class="dQm2"]/span/text()').extract_first())
         if items.xpath('.//div[@class="dQm2"]/span/text()').extract_first()==None:
          original_price=current_price
         elif items.xpath('.//div[@class="dQm2"]/span/text()').extract_first()=='-' :
          original_price=items.xpath('.//div[@class="dQm2"]/text()').extract_first()
         else:
          original_price=items.xpath('.//div[@class="dQm2"]/span/text()').extract_first()
         link=path+items.xpath('.//div[@class="_3WhJ"]/a/@href').extract_first()
         title=items.xpath('.//div[@class="_2apC"]/text()').extract_first()
         rating='NO rating available'
         stock='IN STOCK'
         
         yield {'Website':'Paytm MALL','Stock':stock,'Product':title,'Rating':rating,'Current Price':current_price,'Original Price':original_price,'LINK':link} 
        print("******************************************************************************SUCCESSFULLY IMPORTED TO CSV************************************************************************************")
        