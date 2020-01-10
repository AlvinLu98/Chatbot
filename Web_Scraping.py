from selenium import webdriver
from bs4 import BeautifulSoup

class process_tickets():
    def __init__(self):
        options = webdriver.ChromeOptions()

        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--log-level=3")
        options.add_argument("--disable-extensions")
        options.add_argument("test-type")

        self.browser = webdriver.Chrome("chromedriver.exe", options=options)

    def get_page(self, url):
        self.browser.get(url)
        self.url = url
        if 'openReturn' in url:
            self.type = 'Open return'
        elif 'single' in url:
            self.type = 'Single'
        else:
            self.type = 'Return'

    def get_cheapest(self):
        cheapest = ''
        if(self.type == "Open return"):
            cheapest =self.get_cheapest_open_return()
        elif(self.type == "Single"):
            cheapest = self.get_cheapest_single()
        else:
            cheapest = self.get_cheapest_return()
        self.browser.close()
        return cheapest

    def get_cheapest_single(self):
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        cheapest = soup.find(class_="_wvg8la")
        cheapest = cheapest.find('span').find('span').getText()
        return cheapest

    def get_cheapest_open_return(self):
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        cheapest = soup.find(class_="_9xsoyzs").find('span').getText()
        return cheapest

    def get_cheapest_return(self):
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        cheapest = soup.find(class_="_cjzfgo")
        if not cheapest:
            cheapest = self.get_cheapest_single()
        else:
            cheapest = cheapest.find('span').getText()
        return cheapest

    def get_all_cheapest(self, cheapest):
        cheapest_list = []
        for c in cheapest:
            cheapest_list.append(c.find('span').getText())
        cheapest_list = set(cheapest_list)
        return cheapest_list

##################################################################################################
#                                       Testing and Training
##################################################################################################
def main():
    test = process_tickets()

    t_single = "https://www.thetrainline.com/book/results?origin=8c369975256e3aa119e38f1c02da8192&destination=a994b357084b0548e2b14a0c76ca0ac0&outwardDate=2020-02-12T07%3A45%3A00&outwardDateType=departAfter&journeySearchType=single&passengers%5B%5D=1989-12-31&passengers%5B%5D=1989-12-31&selectedOutward=1oU7LCqHx5A%3D%3Aq5PkedMWD4Y%3D&lang=en"
    t_return = "https://www.thetrainline.com/book/results?origin=8c369975256e3aa119e38f1c02da8192&destination=a994b357084b0548e2b14a0c76ca0ac0&outwardDate=2020-02-12T07%3A45%3A00&outwardDateType=departAfter&journeySearchType=return&passengers%5B%5D=1989-12-31&passengers%5B%5D=1989-12-31&inwardDate=2020-02-14T17%3A00%3A00&inwardDateType=departAfter&selectedOutward=1oU7LCqHx5A%3D%3Aq5PkedMWD4Y%3D&selectedInward=4Hx0pxTE0hc%3D%3A8DszCE9x6lA%3D"
    t_return_2 = "https://www.thetrainline.com/book/results?origin=8c369975256e3aa119e38f1c02da8192&destination=ab2ebee3c41ae38ea2947d0166e79df4&outwardDate=2020-02-12T07%3A45%3A00&outwardDateType=departAfter&journeySearchType=return&passengers%5B%5D=1989-12-31&passengers%5B%5D=1989-12-31&inwardDate=2020-02-14T17%3A00%3A00&inwardDateType=departAfter&selectedOutward=k2zdUJHdm2E%3D%3AtZrcoUs5cU4%3D&selectedInward=eI%2BPROgm8hA%3D%3AMmNAWxEGWt8%3D&lang=en"
    t_open_ret = "https://www.thetrainline.com/book/results?origin=8c369975256e3aa119e38f1c02da8192&destination=ab2ebee3c41ae38ea2947d0166e79df4&outwardDate=2020-02-12T07:45:00&outwardDateType=departAfter&journeySearchType=openReturn&passengers[]=1989-12-31&passengers[]=1989-12-31"
    test.get_page(t_return)
    print(test.get_cheapest())

if __name__ == '__main__':
    main()