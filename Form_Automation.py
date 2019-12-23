"""
Created on Sun Oct 27 13:30:10 2019

@author: Alvin Lu
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

##################################################################################################
#                                      Helper functions
##################################################################################################

def initiate_website(url):
    options = webdriver.ChromeOptions()

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-extensions")
    options.add_argument("test-type")

    browser = webdriver.Chrome("chromedriver.exe", options=options)

    browser.get(url)
    return browser

##################################################################################################
#                                     Completing tickets
##################################################################################################
def get_ticket_single(url, orig, dest, t_type, date, hour, minute, amount):
    browser = initiate_website(url)

    #fill in origin 
    origin = browser.find_element_by_id('from.text')
    origin.send_keys(orig)
    origin.send_keys(Keys.ENTER)

    #fill in destiation
    destination = browser.find_element_by_id('to.text')
    destination.send_keys(dest)
    destination.send_keys(Keys.ENTER)

    #select ticket type
    if t_type == "single":
        t_type = browser.find_element_by_id('single')
        t_type.click()
    elif t_type == "open":
        t_type = browser.find_element_by_id('openReturn')
        t_type.click()
    else:
        t_type = browser.find_element_by_id('single')
        t_type.click()

    depart_date = browser.find_element_by_id('page.journeySearchForm.outbound.title')
    depart_date.send_keys(Keys.HOME,Keys.SHIFT,Keys.END)
    depart_date.send_keys(date)
    depart_date.send_keys(Keys.ENTER)

    dep_time = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[1]/div/div/div/div[1]/section/form/div[3]/fieldset[1]/div[4]/div[1]/select')
    dep_time.click()
    dep_time.send_keys(hour)
    dep_time.click()
    
    dep_quart = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[1]/div/div/div/div[1]/section/form/div[3]/fieldset[1]/div[4]/div[2]/select')
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

    amt = browser.find_element_by_xpath('//*[@id="passenger-summary-btn"]')
    amt.click()
    amt = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[1]/div/div/div/div[1]/section/form/div[4]/div/div/div/div[1]/div/div/select')
    amt.click()
    amt.send_keys(amount)
    amt.click()

    browser.find_element_by_xpath('//*[@id="passenger-summary-btn"]').click()
    
    submit = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[1]/div/div/div/div[1]/section/form/div[5]/button')
    submit.click()
    ret_url = browser.current_url

    browser.quit()
    return ret_url

##################################################################################################
#                                           Testing
##################################################################################################

def main():
    print(get_ticket_single('https://www.thetrainline.com/', 'Norwich', "Gatwick Airport", "open", 
    "12-Feb-20", "07", "45", 2))
    
if __name__ == '__main__':
    main()
