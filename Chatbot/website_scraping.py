# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 01:30:16 2019

@author: Alvin Lu
"""

import re
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

###############################################################################
#                         Web scraper for single ticket
###############################################################################
#Returns train ticket data from html
#@respData: list of html data of the web pages
#OUTPUT:    list to train ticket data with the cheapest fare
def get_Single_Data_TL(respData):
    """ Retrieves essential data from the website Train Line given the url """
    date = None
    departure = None
    arrival = None
    duration = None
    changes = None
    soup = None
    date = None
    currentDay = None
    dayChange = None
    available_Trains = list()
    
    for n in respData:
        train_detail = ''
        soup = BeautifulSoup(n, 'html.parser')
        trains = soup.find(class_="_h9wfdq")
        
        if date is None or currentDay != soup.find(class_="_ybofl5").text:
            date = soup.find(class_="_ybofl5")
            currentDay = date.text
            #print()
            #print(currentDay)
        
        for li in trains.find_all("li"):
            dayChange = datetime.strptime(li.find(class_="_wbydt7").text, '%H:%M')
            dayChange = dayChange.time()
                
            departure = datetime.strptime(li.find(class_="_wbydt7").text,"%H:%M")
            departure = departure.time()
            arrival = datetime.strptime(li.find(class_="_9zpz00").text,"%H:%M")
            arrival = arrival.time()
            duration = li.find(class_="_1ic8min")
            prices = li.find(class_="_hq5slr")
            changes = li.find(class_="_130pdk39")
            if duration is None:
                duration = li.find(class_="_137hbqu3")
            if prices is not None:
                price = prices.findChildren("span")
                train_detail = str(departure) + "   " +str(arrival) + "   "+ str(duration.findChildren("span")[0].text)+ "   "+ changes.text+ "   "+price[0].text
                available_Trains.append(train_detail)
                #print(train_detail)
    return available_Trains

#gets the html page depends on the choice of arrive before or depart after
#@url:   url of the initial results page
#OUTPUT: list of html data of the results page
def get_Sigle_TL(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-extensions")
    options.add_argument("test-type")
    options.add_argument("--window-size=1920,1080")
    
    browser = webdriver.Chrome("chromedriver.exe", options=options)
    browser.get(url)
    respData = list()
    try:
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/main/div[2]/div[1]/div/div/div[3]/div[1]/div[1]/div/div/button[2]')))
        respData.append(browser.page_source)
    except NoSuchElementException:
        print("Loading failed")
    if("arriveBefore" in url):
        get_Single_Before_TL(browser, respData)
    else:
        get_Single_After_TL(browser, respData)
    browser.quit()
    return get_Single_Data_TL(respData)

#gets the results before the initial results page
#@browser:   url of the initial results page
#@respData: list containing the initial results page
def get_Single_Before_TL(browser, respData):
    for x in range (0,3):
        try:
            before = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[2]/div[1]/div/div/div[3]/div[1]/div[1]/div/div/button[1]')
            before.click()
            WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/main/div[2]/div[1]/div/div/div[3]/div[1]/div[1]/div/div/button[1]')))
            respData.insert(0, browser.page_source)
        except TimeoutException:
            print("Loading took too much time!")
        except NoSuchElementException:
            print("Loading failed")
   
#gets the results after the initial results page
#@browser:   url of the initial results page
#@respData: list containing the initial results page
def get_Single_After_TL(browser, respData):
    for x in range(0, 3):
        try:
            later = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[2]/div[1]/div/div/div[3]/div[1]/div[1]/div/div/button[2]')
            later.click()
            WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/main/div[2]/div[1]/div/div/div[3]/div[1]/div[1]/div/div/button[2]')))
            respData.append(browser.page_source)
        except TimeoutException:
            print("Loading took too much time!")
        except NoSuchElementException:
            print("Loading failed")

###############################################################################
#                     Web scraper for open return ticket
###############################################################################
#Returns train ticket data from html
#@respData: list of html data of the web pages
#OUTPUT:    list to train ticket data with the cheapest fare
def get_OpenRet_Data_TL(respData):
    """ Retrieves essential data from the website Train Line given the url """
    #date = None
    departure = None
    arrival = None
    duration = None
    changes = None
    soup = None
    prices = None
    priceList = set()
    trainList = list()
    price_List = ''
    
    for n in respData:
        soup = BeautifulSoup(n, 'html.parser')
        trains = soup.find(class_="_1t3yyjh")
        #date = soup.find(class_="_l55b2y")
        
        for li in trains.find_all("li"):
            times = li.findAll(class_="_1mlnrh6")
            departure = times[0].text[-8:]
            arrival = times[1].text[-8:]
            duration = li.find(class_="_co3gg6")
            changes = li.find(class_="_7wa8kp")
            info = departure + '   '+ arrival+ '   '+duration.text+'    '+changes.text
            #print(info)
            trainList.append(info)
            
        prices = soup.findAll("h3", {"class":"_1cqcfips"})
        for p in prices:
            priceList.add(p.text)
        for p in priceList:
            ind = p.index("£")
            p = p[:ind] + " " + p[ind:]
            price_List+=p + "<br>"
        price_List+="<br><br>"
        #print(price_List)
        trainList.append(price_List)
        #print()
        price_List = ''
        priceList = set()
    return trainList

#gets the html page depends on the choice of arrive before or depart after
#@url:   url of the initial results page
#OUTPUT: list of html data of the results page
def get_OpenRet_TL(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-extensions")
    options.add_argument("test-type")
    options.add_argument("--window-size=1920,1080")
    
    browser = webdriver.Chrome("chromedriver.exe", options=options)
    browser.get(url)
    respData = list()
    try:
        WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, '_1xm8va3a')))
        respData.append(browser.page_source)
    except TimeoutException:
            print("Loading took too much time!")
    except NoSuchElementException:
            print("Loading failed")
    if("arriveBefore" in url):
        get_OpenRet_Before_TL(browser, respData)
    else:
        get_OpenRet_After_TL(browser, respData)
    #browser.quit()
    return get_OpenRet_Data_TL(respData)

#gets the results before the initial results page
#@browser:   url of the initial results page
#@respData: list containing the initial results page 
def get_OpenRet_Before_TL(browser, respData):
    for x in range(0,3):
        try:
            before = browser.find_element_by_class_name('_1r03v1l')
            before.click()
            WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, '_1r03v1l')))
            respData.insert(0, browser.page_source)
        except TimeoutException:
            print("Loading took too much time!")
   
#gets the results after the initial results page
#@browser:   url of the initial results page
#@respData: list containing the initial results page   
def get_OpenRet_After_TL(browser, respData):
    for x in range(0, 3):
        try:
            later = browser.find_element_by_class_name('_1xm8va3a')
            later.click()
            WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, '_1xm8va3a')))
            respData.append(browser.page_source)
        except TimeoutException:
            print("Loading took too much time!")
        except NoSuchElementException:
            print("Loading failed")

###############################################################################
#                         Web scraper for return ticket
###############################################################################
#Returns train ticket data from html
#@respDataO: list of html data of web pages for outward
#@respDataI: list of html data of web pages for return
#OUTPUT:     list to train ticket data with the cheapest fare
def get_Ret_Data_TL(respDataO, respDataI):
    """ Retrieves essential data from the website Train Line given the url """
    date = None
    departure = None
    arrival = None
    duration = None
    changes = None
    soup = None
    date = None
    currentDay = None
    dayChange = None
    available_Trains = list()
    available_Returns = list()
    
    #print("---------------- OUT -----------------")
    for n in respDataO:
        train_detail = ''
        soup = BeautifulSoup(n, 'html.parser')
        trains = soup.findAll(class_="_h9wfdq")
        
        if date is None or currentDay != soup.find(class_="_ybofl5").text:
            date = soup.find(class_="_ybofl5")
            currentDay = date.text
            #print()
            #print(currentDay)
        
        for li in trains[0].find_all("li"):
            dayChange = datetime.strptime(li.find(class_="_wbydt7").text, '%H:%M')
            dayChange = dayChange.time()
                
            departure = datetime.strptime(li.find(class_="_wbydt7").text,"%H:%M")
            departure = departure.time()
            arrival = datetime.strptime(li.find(class_="_9zpz00").text,"%H:%M")
            arrival = arrival.time()
            duration = li.find(class_="_1ic8min")
            prices = li.find(class_="_hq5slr")
            changes = li.find(class_="_130pdk39")
            if duration is None:
                duration = li.find(class_="_137hbqu3")
            if prices is not None:
                price = prices.findChildren("span")
                train_detail = str(departure) + "   " +str(arrival) + "   "+ str(duration.findChildren("span")[0].text)+ "   "+ changes.text+ "   "+price[0].text
                #print(train_detail)
                available_Trains.append(train_detail)
     
    print("---------------- IN -----------------")
    for n in respDataI:
        train_detail = ''
        soup = BeautifulSoup(n, 'html.parser')
        trains = soup.findAll(class_="_h9wfdq")
        
        if date is None or currentDay != soup.find(class_="_ybofl5").text:
            date = soup.find(class_="_ybofl5")
            currentDay = date.text
            #print()
            #print(currentDay)
        
        for li in trains[1].find_all("li"):
            dayChange = datetime.strptime(li.find(class_="_wbydt7").text, '%H:%M')
            dayChange = dayChange.time()
                
            departure = datetime.strptime(li.find(class_="_wbydt7").text,"%H:%M")
            departure = departure.time()
            arrival = datetime.strptime(li.find(class_="_9zpz00").text,"%H:%M")
            arrival = arrival.time()
            duration = li.find(class_="_1ic8min")
            prices = li.find(class_="_hq5slr")
            changes = li.find(class_="_130pdk39")
            if duration is None:
                duration = li.find(class_="_137hbqu3")
            if prices is not None:
                price = prices.findChildren("span")
                train_detail = str(departure) + "   " +str(arrival) + "   "+ str(duration.findChildren("span")[0].text)+ "   "+ changes.text+ "   "+price[0].text
                #print(train_detail)
                available_Returns.append(train_detail)
                
    return available_Trains, available_Returns

#gets the html page depends on the choice of arrive before or depart after
#@url:   url of the initial results page
#OUTPUT: two list of html data of the results page for departure and return
def get_Ret_TL(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-extensions")
    options.add_argument("test-type")
    options.add_argument("--window-size=1920,1080")
    
    browser = webdriver.Chrome("chromedriver.exe", options=options)
    browser.get(url)
    respDataO = list()
    respDataI = list()
    try:
        WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/main/div[2]/div[1]/div/div/div[3]/div[1]/div[1]/div/div/button[1]')))
        respDataO.append(browser.page_source)
        respDataI.append(browser.page_source)
    except TimeoutException:
            print("Loading took too much time!")
    except NoSuchElementException:
        print("Loading failed")
    if("outwardDateType=arriveBefore" in url):
        get_Ret_Before_outward_TL(browser, respDataO)
    else:
        get_Ret_After_outward_TL(browser, respDataO)
    
    if("inwardDateType=arriveBefore" in url):
        get_Ret_Before_inward_TL(browser, respDataI)
    else:
        get_Ret_After_inward_TL(browser, respDataI)
    browser.quit()
    out_Train, in_Train = get_Ret_Data_TL(respDataO, respDataI)
    return out_Train, in_Train

#gets the results before the initial results page for departure
#@browser:   url of the initial results page
#@respData: list containing the initial results page 
def get_Ret_Before_outward_TL(browser, respData):
    for x in range (0,3):
        try:
            WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/main/div[2]/div[1]/div/div/div[3]/div[1]/div[1]/div/div/button[1]')))
            before = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[2]/div[1]/div/div/div[3]/div[1]/div[1]/div/div/button[1]')
            before.click()
            WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/main/div[2]/div[1]/div/div/div[3]/div[1]/div[1]/div/div/button[1]')))
            respData.insert(0, browser.page_source)
        except TimeoutException:
            print("Loading took too much time!")
        except NoSuchElementException:
            print("Loading failed")
   
#gets the results after the initial results page for return
#@browser:   url of the initial results page
#@respData: list containing the initial results page    
def get_Ret_After_outward_TL(browser, respData):
   for x in range(0, 3):
        try:
            WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/main/div[2]/div[1]/div/div/div[3]/div[1]/div[1]/div/div/button[2]')))
            later = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[2]/div[1]/div/div/div[3]/div[1]/div[1]/div/div/button[2]')
            later.click()
            WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/main/div[2]/div[1]/div/div/div[3]/div[1]/div[1]/div/div/button[2]')))
            respData.append(browser.page_source)
        except TimeoutException:
            print("Loading took too much time!")
        except NoSuchElementException:
            print("Loading failed")

#gets the results before the initial results page for return
#@browser:   url of the initial results page
#@respData: list containing the initial results page             
def get_Ret_Before_inward_TL(browser, respData):
    for x in range (0,3):
        try:
            WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/main/div[2]/div[1]/div/div/div[3]/div[1]/div[3]/div/div/button[1]')))
            before = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[2]/div[1]/div/div/div[3]/div[1]/div[3]/div/div/button[1]')
            before.click()
            WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/main/div[2]/div[1]/div/div/div[3]/div[1]/div[3]/div/div/button[1]')))
            respData.insert(0, browser.page_source)
        except TimeoutException:
            print("Loading took too much time!")
        except NoSuchElementException:
            print("Loading failed")
   
#gets the results after the initial results page for return
#@browser:   url of the initial results page
#@respData: list containing the initial results page  
def get_Ret_After_inward_TL(browser, respData):
    for x in range(0, 3):
        try:
            WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/main/div[2]/div[1]/div/div/div[3]/div[1]/div[3]/div/div/button[2]')))
            later = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/main/div[2]/div[1]/div/div/div[3]/div[1]/div[3]/div/div/button[2]')
            later.click()
            WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/main/div[2]/div[1]/div/div/div[3]/div[1]/div[3]/div/div/button[2]')))
            respData.append(browser.page_source)
        except TimeoutException:
            print("Loading took too much time!")
        except NoSuchElementException:
            print("Loading failed")
            
###############################################################################
#                          Get info of live trains
###############################################################################
#Returns the current information of a live train
#@org:   origin of the train
#@dest:  destination of the train
#@date:  date of departure
#@time:  time of expected departure
#OUTPUT: previous station the train was in, next station the train is going to
#        current delay and the predicted arrival time
def getLiveTrainInfo(org, dest, date, time):
    day = date[-2:]
    year = date[:4]
    month = date[5:7]
    time = time[:2]+time[-2:]
    #open webpage at required train tracker
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-extensions")
    options.add_argument("test-type")
    browser = webdriver.Chrome("chromedriver.exe", options=options)
    baseUrl = "http://www.realtimetrains.co.uk/search/basic/"
    fullUrl = baseUrl + org + "/to/" + dest + "/" + year + "/" + month + "/" + day + "/" + time
    browser.maximize_window()
    browser.get(fullUrl)
    #Get a list of train times that match the search
    trains = browser.find_elements_by_css_selector(".service_group")
    trainChoice = trains[0]
    #Present all trains that match the search and get the user to make a choice 
    for i in range(0, len(trains)):
            train_time = trains[i].find_elements_by_css_selector(".gbtt.time.timetabled")
            train_time = train_time[0].text
            if(train_time == time):
                trainChoice = trains[i]
    #train choice
    trainChoice.click()
    
    #Get a list of all the stations on a route
    allStationsEnroute = browser.find_elements_by_css_selector(".call_public.call")
    stations = []
    for i in range (0, len(allStationsEnroute)):
            stationIndex = re.search("\d", allStationsEnroute[i].text )
            station = allStationsEnroute[i].text[:stationIndex.start()]
            station = station.split('(', 1)[0]
            stations.append(station)
    
    #Gets a list of visited stations, as well as the trains last visited station and its next station
    originElement          = allStationsEnroute[0]
    destinationElement     = allStationsEnroute[-1]
    
    visitedStations         = browser.find_elements_by_css_selector(".reported.call_public.call")
    previousStation         = stations[len(visitedStations)-1]
    nextStation             = stations[len(visitedStations)]
    destinationStation      = str(stations[-1])
    
    predictedArrivalTime = 0
    currentDelay = "On time"
    
    try:
        predictedArrivalTime = destinationElement.find_element_by_css_selector(".realtime.time.prediction.borderleft").text
        currentDelay         = allStationsEnroute[len(visitedStations)-1].find_element_by_css_selector(".delay").text
    except NoSuchElementException:
        print("Not operating")
    
    #edit the delay string to be more presentable
    if currentDelay != "On time":
        currentDelaySplit = currentDelay.split(" ")
        delayTime = currentDelaySplit[0][:-1]
    else:
        delayTime = 0
    
    #print("\nThis train is currently between " + previousStation + "and " + nextStation)
    #print("This train's delay is currently " + str(delayTime) + " minute(s) ")
    #print("This train is expected to arrive at its destination, " + destinationStation + "at " + predictedArrivalTime)
    return previousStation, nextStation, str(delayTime), predictedArrivalTime
           
    browser.close()

###############################################################################
#                                  Main method
###############################################################################
if __name__ == "__main__":
    url1 = 'https://www.thetrainline.com/book/results?origin=9ec4a5a1adc550e1eda507588bbabbcc14276b43&destination=0c0dfbfa772017b31b747c33d0e0faf3661722f0&outwardDate=2019-02-12T20%3A15%3A00&outwardDateType=arriveBefore&journeySearchType=single&passengers%5B%5D=1989-01-11&selectedOutward=j1d3I1J%2F45o%3D%3A74wFkffyyL0%3D'
    url2 = 'https://www.thetrainline.com/book/results?origin=9ec4a5a1adc550e1eda507588bbabbcc14276b43&destination=0c0dfbfa772017b31b747c33d0e0faf3661722f0&outwardDate=2019-02-12T20%3A15%3A00&outwardDateType=arriveBefore&journeySearchType=openReturn&passengers%5B%5D=1989-01-11&selectedOutward=YtBkBFv52Pw%3D%3APTcdCc2bVOo%3D&temporalDirection=previous&transitDefinitionDirection=outward&searchId=774d690a-7690-4aea-ba34-c07ee79800cd'
    url3 = 'https://www.thetrainline.com/book/results?origin=9ec4a5a1adc550e1eda507588bbabbcc14276b43&destination=0c0dfbfa772017b31b747c33d0e0faf3661722f0&outwardDate=2019-02-12T20%3A15%3A00&outwardDateType=arriveBefore&journeySearchType=return&passengers%5B%5D=1989-01-11&inwardDate=2019-03-13T20%3A15%3A00&inwardDateType=departAfter&selectedOutward=j1d3I1J%2F45o%3D%3A74wFkffyyL0%3D&selectedInward=ISrgXJI%2BuJw%3D%3AfOvI%2FvyujYE%3D&temporalDirection=previous&transitDefinitionDirection=outward&searchId=cc832fff-5741-4e71-8833-c1b6b03661a4'
    #a=get_Sigle_TL(url1)
    
    #a=get_OpenRet_TL(url2)
    
    #a,b=get_Ret_TL(url3)
    '''
    print()
    for i in a:
        print(i)
    '''
    '''
    for i in b:
        print(i)
    '''
    
    
    print("Welcome to live train checker, you may check the progress of any train currently running")
    start = input ("Please enter a start station: ")
    end   = input ("Please enter an end station: ")
    date  = input("Please enter a date (yyyy/mm/dd):")
    time  = input ("please enter a train time (hh:mm): ")
    
    print("\nPlease wait while I look for that journey (this may take some time)...\n")
    getLiveTrainInfo(start, end, date, time)
    
    