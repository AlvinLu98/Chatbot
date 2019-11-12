"""
knowledge_acquisition.py

Knowledge Acquisition component
"""

import os
import subprocess
import chatbot

LINK_PATH = "link.txt"

# Get booking information from the booking website
def request_booking(start, destination, date, hour):
    #print(start + "\n" + destination + "\n" + date + "\n" + hour + "\n")

    # Scrape the website
    subprocess.call('scraper/phantomjs.exe scraper/scraper.js ' + start + ' ' + destination + ' ' + date + ' ' + hour)

    # Get the scraper's link from file
    if os.path.exists(LINK_PATH):
        file = open(LINK_PATH, "r")

        link = file.read()
        if link == "http://ojp.nationalrail.co.uk/service/planjourney/search" or link == "http://www.nationalrail.co.uk/times_fares/116055.aspx":
            chatbot.message("Unfortunately I was not able to find any tickets matching your criteria.")
            chatbot.message("Please ensure the ticket time has not expired and that a trainline exists between the two stations.")
        else:
            chatbot.message("Please visit this link to book your tickets: " + link)

        file.close()
    else:
        chatbot.message("Sorry, I am having problems contacting the website. Please try again.")

def request_last_booking():
    if os.path.exists(LINK_PATH):
        file = open(LINK_PATH, "r")
        chatbot.message("Your last booking was: " + file.read())
        file.close()
