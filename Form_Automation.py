"""
Created on Sun Oct 27 13:30:10 2019

@author: Alvin Lu
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Form_filler():
    def __init__(self):
        options = webdriver.ChromeOptions()

        # options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--log-level=3")
        options.add_argument("--disable-extensions")
        options.add_argument("test-type")

        self.browser = webdriver.Chrome("chromedriver.exe", options=options)
    
    ##################################################################################################
    #                                      Helper functions
    ##################################################################################################
    def initiate_website(self, url):
        self.browser.get(url)

    ##################################################################################################
    #                                     Completing tickets
    ##################################################################################################
    def single_ticket(self, url, orig, dest, t_type, date, hour, minute, amount):
        self.initiate_website(url)

        self.fill_general(orig, dest, t_type, date, hour, minute, amount)

        submit = self.browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[1]/div/div/div/div[1]/section/form/div[5]/button')
        submit.click()
        ret_url = self.browser.current_url

        self.browser.quit()
        return ret_url
    
    def return_ticket(self, url, orig, dest, t_type, dep_date, dep_hour, dep_min, ret_date, ret_hour, 
    ret_min, amount):
        self.initiate_website(url)

        self.fill_general(orig, dest, t_type, dep_date, dep_hour, dep_min, amount)
        self.fill_return(ret_date, ret_hour, ret_min)

        submit = self.browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[1]/div/div/div/div[1]/section/form/div[5]/button')
        submit.click()
        ret_url = self.browser.current_url

        self.browser.quit()
        return ret_url

    def fill_general(self, orig, dest, t_type, date, hour, minute, amount):
        #fill in origin 
        origin = self.browser.find_element_by_id('from.text')
        origin.send_keys(orig)
        origin.send_keys(Keys.ENTER)

        #fill in destiation
        destination = self.browser.find_element_by_id('to.text')
        destination.send_keys(dest)
        destination.send_keys(Keys.ENTER)

        #select ticket type
        if t_type == "single":
            t_type = self.browser.find_element_by_id('single')
            t_type.click()
        elif t_type == "open":
            t_type = self.browser.find_element_by_id('openReturn')
            t_type.click()
        elif t_type == "return":
            t_type = self.browser.find_element_by_id('return')
            t_type.click()
        else:
            t_type = self.browser.find_element_by_id('single')
            t_type.click()

        depart_date = self.browser.find_element_by_id('page.journeySearchForm.outbound.title')
        depart_date.send_keys(Keys.HOME,Keys.SHIFT,Keys.END)
        depart_date.send_keys(date)
        depart_date.send_keys(Keys.ENTER)

        dep_time = self.browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[1]/div/div/div/div[1]/section/form/div[3]/fieldset[1]/div[4]/div[1]/select')
        dep_time.click()
        dep_time.send_keys(hour)
        dep_time.click()
        
        dep_quart = self.browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[1]/div/div/div/div[1]/section/form/div[3]/fieldset[1]/div[4]/div[2]/select')
        dep_quart.click()
        minute = int(minute)
        if(minute < 15):
            dep_quart.send_keys(0)
        elif (minute < 30):
            dep_quart.send_keys(15)
        elif (minute < 45):
            dep_quart.send_keys(30)
        else:
            dep_quart.send_keys(45)
        dep_quart.click()

        amt = self.browser.find_element_by_xpath('//*[@id="passenger-summary-btn"]')
        amt.click()
        amt = self.browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[1]/div/div/div/div[1]/section/form/div[4]/div/div/div/div[1]/div/div/select')
        amt.click()
        amt.send_keys(amount)
        amt.click()

        self.browser.find_element_by_xpath('//*[@id="passenger-summary-btn"]').click()
    
    def fill_return(self, ret_date, ret_hour, ret_min):
        return_date = self.browser.find_element_by_xpath('//*[@id="page.journeySearchForm.inbound.title"]')
        return_date.send_keys(Keys.HOME,Keys.SHIFT,Keys.END)
        return_date.send_keys(ret_date)
        return_date.send_keys(Keys.ENTER)

        return_time = self.browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[1]/div/div/div/div[1]/section/form/div[3]/fieldset[2]/div[4]/div[1]/select')
        return_time.click()
        return_time.send_keys(ret_hour)
        return_time.click()

        dep_quart = self.browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[1]/div/div/div/div[1]/section/form/div[3]/fieldset[2]/div[4]/div[2]/select')
        dep_quart.click()
        minute = int(ret_min)
        if(minute < 15):
            dep_quart.send_keys(0)
        elif (minute < 30):
            dep_quart.send_keys(15)
        elif (minute < 45):
            dep_quart.send_keys(30)
        else:
            dep_quart.send_keys(45)
        dep_quart.click()


##################################################################################################
#                                           Testing
##################################################################################################

def main():
    test = Form_filler()
    # test.single_ticket('https://www.thetrainline.com/', 'Norwich', "Gatwick Airport", "open", 
    # "12-Feb-20", "07", "45", 2)

    test.return_ticket('https://www.thetrainline.com/', 'Norwich', "Gatwick Airport", "return", 
    "12-Feb-20", "07", "45", "14-Feb-20", "08", "09", 2)
    
if __name__ == '__main__':
    main()
