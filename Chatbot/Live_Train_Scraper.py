#Gets information about live, in progress trains

import sys
import re
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException


def getLiveTrainInfo(org, dest, date, time):
    day = date[-2:]
    year = date[:4]
    month = date[5:7]
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
    
    #Present all trains that match the search and get the user to make a choice 
    print ("\nThe following trains match your search. Please choose a train using the specified ID number: ")
    for i in range(0, len(trains)):
            time = trains[i].find_elements_by_css_selector(".gbtt.time.timetabled")
            train = trains[i].text.rsplit("\n",3)[0]
            train = train.replace('\n', ' ').replace('\r', '')
            print(str(i+1) + ") " + train)
    
    #train choice
    trainChoice = trains[int( input())-1]
    print("\nPlease wait while I find the train...\n")
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
    
    predictedArrivalTime = destinationElement.find_element_by_css_selector(".realtime.time.prediction.borderleft").text
    currentDelay         = allStationsEnroute[len(visitedStations)-1].find_element_by_css_selector(".delay").text
    
    #edit the delay string to be more presentable
    if(not currentDelay == "On time"):
    
            currentDelaySplit = currentDelay.split(" ")
            delayTime = currentDelaySplit[0][:-1]
    else:
            delayTime = 0
    
    print("\nThis train is currently between " + previousStation + "and " + nextStation)
    print("This train's delay is currently " + str(delayTime) + " minute(s) ")
    print("This train is expected to arrive at its destination, " + destinationStation + "at " + predictedArrivalTime)
           
    browser.close()
   

if __name__ == "__main__":
    print("Welcome to live train checker, you may check the progress of any train currently running")
    start = input ("Please enter a start station: ")
    end   = input ("Please enter an end station: ")
    date  = input("Please enter a date:")
    time  = input ("please enter a train time (hhmm): ")
    
    print("\nPlease wait while I look for that journey (this may take some time)...\n")
    getLiveTrainInfo(start, end, date, time)