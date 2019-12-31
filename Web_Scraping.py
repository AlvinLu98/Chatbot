import scrapy

class singleTrainSpider(scrapy.Spider):
    name = 'single_train_spider'
    allowed_domains = ['trainline.com']

    def __init__(self, url):
        self.start_urls = [url]

    def parse(self, response):
        print(response.url)

def main():
    s = singleTrainSpider('https://www.thetrainline.com/book/results?origin=8c369975256e3aa119e38f1c02da8192&destination=a994b357084b0548e2b14a0c76ca0ac0&outwardDate=2019-12-30T21%3A00%3A00&outwardDateType=departAfter&journeySearchType=single&passengers%5B%5D=1989-12-30&selectedOutward=GTjgd7erdmM%3D%3AyreUu12GqJ4%3D&temporalDirection=next&transitDefinitionDirection=outward&searchId=aef44dc6-3e4e-41ba-9536-9e369487b3d9')
    print(s.start_urls)

if __name__ == '__main__':
    main()