# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 20:59:34 2019

@author: Alvin Lu
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

###############################################################################
#             Form submission for single and open return ticket
###############################################################################

#Submits single or open return form online and gets the url
#@fro:          origin
#@to:           destination
#@ticket_type:  "single" or "open"
#@out_date:     Date of departure in format yyyy:mm:dd
#@out_byBefore: "Arrive before" OR "Depart after"
#@out_time:     Hour of the submitted time
#@out_quarter:  Quarter of the submitted time
#@amt:          Amount of adults booking the ticket
#OUTPUT:        url submitted by the form
def submitTrainLineForm_Single(fro, to, ticket_type, out_date, out_byBefore, out_time, out_quarter, amt):
    url = "https://www.thetrainline.com/"
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-extensions")
    options.add_argument("test-type")
    
    browser = webdriver.Chrome("chromedriver.exe", options=options)

    browser.get(url)
    org = browser.find_element_by_id('from.text')
    org.send_keys(fro)
    org.send_keys(Keys.ENTER)
    
    dest = browser.find_element_by_id('to.text')
    dest.send_keys(to)
    dest.send_keys(Keys.ENTER)
    
    if ticket_type == "single":
        ticket_type = browser.find_element_by_id('single')
        ticket_type.click()
    elif ticket_type == "open":
        ticket_type = browser.find_element_by_id('openReturn')
        ticket_type.click()
    else:
        ticket_type = browser.find_element_by_id('single')
        ticket_type.click()
        
    depart_date = browser.find_element_by_id('page.journeySearchForm.outbound.title')
    depart_date.send_keys(Keys.HOME,Keys.SHIFT,Keys.END)
    depart_date.send_keys(out_date)
    depart_date.send_keys(Keys.ENTER)
    
    if out_byBefore == "arrive before":
        browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[1]/div/div/div[1]/section/form/div[3]/fieldset[1]/div[3]/div/select/option[2]').click()
    elif out_byBefore == "depart after":
        browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[1]/div/div/div[1]/section/form/div[3]/fieldset[1]/div[3]/div/select/option[1]').click()
    
    dep_time = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[1]/div/div/div[1]/section/form/div[3]/fieldset[1]/div[4]/div[1]/select')
    dep_time.click()
    dep_time.send_keys(out_time)
    dep_time.click()
    
    dep_quart = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[1]/div/div/div[1]/section/form/div[3]/fieldset[1]/div[4]/div[2]/select')
    dep_quart.click()
    dep_quart.send_keys(out_quarter)
    dep_quart.click()
    
    passengers = browser.find_element_by_xpath('//*[@id="passenger-summary-btn"]')
    passengers.click()
    passengers = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[1]/div/div/div[1]/section/form/div[4]/div/div/div/div[1]/div/div/select')
    passengers.click()
    passengers.send_keys(amt)
    passengers.click()
    browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[1]/div/div/div[1]/section/form/div[4]/div/div/button').click()
    
    submit = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[1]/div/div/div[1]/section/form/div[5]/button')
    submit.click()
    url = browser.current_url
    browser.quit()
    return url
    
###############################################################################
#                     Form submission for return ticket
###############################################################################
#Submits return form online and gets the url
#@fro:          origin
#@to:           destination
#@ticket_type:  "single" or "open"
#@out_date:     Date of departure in format yyyy:mm:dd
#@out_byBefore: "Arrive before" OR "Depart after"
#@out_time:     Hour of the submitted time for return
#@out_quarter:  Quarter of the submitted time for return
#@ret_date:     Date of return in format yyyy:mm:dd
#@ret_byBefore: "Arrive before" OR "Depart after"
#@ret_time:     Hour of the submitted time for return
#@ret_quarter:  quarter of the submitted time for return
#@amt:          Amount of adults booking the ticket
#OUTPUT:        url submitted by the form
def submitTrainLineForm_Return(fro, to, ticket_type, out_date, out_byBefore, out_time, out_quarter, ret_date, ret_byBefore, ret_time, ret_quarter, amt):
    url = "https://www.thetrainline.com/"

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-extensions")
    options.add_argument("test-type")
    
    browser = webdriver.Chrome("chromedriver.exe", options=options)

    browser.get(url)
    org = browser.find_element_by_id('from.text')
    org.send_keys(fro)
    org.send_keys(Keys.ENTER)
    
    dest = browser.find_element_by_id('to.text')
    dest.send_keys(to)
    dest.send_keys(Keys.ENTER)

    ticket_type = browser.find_element_by_id('return')
    ticket_type.click()
    
    depart_date = browser.find_element_by_id('page.journeySearchForm.outbound.title')
    depart_date.send_keys(Keys.HOME,Keys.SHIFT,Keys.END)
    depart_date.send_keys(out_date)
    depart_date.send_keys(Keys.ENTER)
    
    if out_byBefore == "arrive before":
        browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[1]/div/div/div[1]/section/form/div[3]/fieldset[1]/div[3]/div/select/option[2]').click()
    elif out_byBefore == "depart after":
        browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[1]/div/div/div[1]/section/form/div[3]/fieldset[1]/div[3]/div/select/option[1]').click()
    
    dep_time = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[1]/div/div/div[1]/section/form/div[3]/fieldset[1]/div[4]/div[1]/select')
    dep_time.click()
    dep_time.send_keys(out_time)
    dep_time.click()
    
    dep_quart = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[1]/div/div/div[1]/section/form/div[3]/fieldset[1]/div[4]/div[2]/select')
    dep_quart.click()
    dep_quart.send_keys(out_quarter)
    dep_quart.click()
    
    return_date = browser.find_element_by_id('page.journeySearchForm.inbound.title')
    return_date.send_keys(Keys.HOME,Keys.SHIFT,Keys.END)
    return_date.send_keys(ret_date)
    return_date.send_keys(Keys.ENTER)
    
    if ret_byBefore == "arrive before":
        browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[1]/div/div/div[1]/section/form/div[3]/fieldset[2]/div[3]/div/select/option[2]').click()
    elif ret_byBefore == "depart after":
        browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[1]/div/div/div[1]/section/form/div[3]/fieldset[2]/div[3]/div/select/option[1]').click()
    
    
    return_time = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[1]/div/div/div[1]/section/form/div[3]/fieldset[2]/div[4]/div[1]/select')
    return_time.click()
    return_time.send_keys(ret_time)
    return_time.click()
    
    return_quart = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[1]/div/div/div[1]/section/form/div[3]/fieldset[2]/div[4]/div[2]/select')
    return_quart.click()
    return_quart.send_keys(ret_quarter)
    return_quart.click()
    
    passengers = browser.find_element_by_xpath('//*[@id="passenger-summary-btn"]')
    passengers.click()
    passengers = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[1]/div/div/div[1]/section/form/div[4]/div/div/div/div[1]/div/div/select')
    passengers.click()
    passengers.send_keys(amt)
    passengers.click()
    browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[1]/div/div/div[1]/section/form/div[4]/div/div/button').click()
    
    submit = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[1]/div/div/div[1]/section/form/div[5]/button')
    submit.click()
    
    url = browser.current_url
    browser.quit()
    return url

###############################################################################
#                                  Main method
###############################################################################  
if __name__ == "__main__":
    #print(submitTrainLineForm_Single("Norwich", "Gatwick Airport", "single", "12-Feb-19", "arrive before", "19", "45", 3))
    print(submitTrainLineForm_Return("Norwich", "Gatwick Airport", "return", "12-Feb-19","arrive before", "19", "45", "13-Feb-19", "depart after", "06", "15", 3))