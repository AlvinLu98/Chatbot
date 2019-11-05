import requests
import json
import csv

#helper functions. Don't use them.
def _time_to_minutes(time):
    hours = time[:2]
    minutes = time[2:]
    return 60*int(hours) + int(minutes)

def _subtract_times(starttime, endtime):
    
    start_hours = int(starttime[:2])
    end_hours = int(endtime[:2])
    starttime = _time_to_minutes(starttime)
    endtime = _time_to_minutes(endtime)
    time_diff = endtime - starttime
    if (end_hours == 0 and start_hours != 0):
        time_diff += 1440
    return time_diff    

# OUTPUT: A sample of training data for the predictive model.
#         Will return historic data relevant to training in accordance with
#         the entries in the parameter @query
#         Each entry in @historical_data is data sample for stop A to stop B

# ORDER OF DATA:
    # 1: Current location of train
    # 2: Final destination of train
    # 3: TOC (train company) code of train
    # 4: Time of day at which train is running (later categorised in to "morning", "afternoon", "evening", "night" for training)
    # 5: Day of the week (weekday, saturday or sunday)
    # 6: Departure delay
     
#
# @query  contains:
# 1: Where the train is departing from
# 2: The train's final destination (these are both encoded in CRS format)
# 3: Start of time interval in which to gather data (e.g. trains running from 7 til 8)
# 4: End of time interval
# 5: From date (same as above)
# 6: To date 
# 7: Days (we can ask for data on weekdays, saturday or sunday) 

# See example at EOF
def pullHistoricalData(query):
    rids = []
    api_url = "https://hsp-prod.rockshore.net/api/v1/serviceMetrics"
    headers = { "Content-Type": "application/json" }
    auths = ("nik_77@live.co.uk", "Bl343$.00135")
    
    data = {
      "from_loc": query[0],
      "to_loc": query[1],
      "from_time": query[2],
      "to_time": query[3],
      "from_date": query[4],
      "to_date": query[5],
      "days": query[6],
      "tolerance": ['45']
    }
    
    request = requests.post(api_url, headers=headers, auth=auths, json=data)
    if(request):
        readData = json.loads(request.text)
        for service in readData['Services']:
            service_rids = service['serviceAttributesMetrics']['rids']
            for rid in service_rids:
                rids.append(rid)
                
        historical_data = []
        api_url = "https://hsp-prod.rockshore.net/api/v1/serviceDetails"
        day = query[6] 
       
        for rid in rids:
        
            data = {
              "rid": rid
            }
            
            request = requests.post(api_url, headers=headers, auth=auths, json=data, verify=True)
            if(request):
                readData = json.loads(request.text)
                #toc = readData['serviceAttributesDetails']['toc_code']
                monthOfService= readData['serviceAttributesDetails']['date_of_service'].split('-')[1]
                stopsList = readData['serviceAttributesDetails']['locations']
                numberOfStops = len(stopsList)
                if (numberOfStops > 1):
                    for i in range(numberOfStops-1):
                        for j in range(1, numberOfStops-i):
                            currentStop = stopsList[i]
                            nextStop = stopsList[i+j]
                            
                            #datadatdata
                            location = currentStop['location']
                            destination = nextStop['location']
                            #datadatadata
                            
                            expectedDeparture = ""
                            if (not currentStop['gbtt_ptd']):
                                expectedDeparture = currentStop['gbtt_pta']
                            else:
                                expectedDeparture = currentStop['gbtt_ptd']
                            expectedArrival = ""
                            if (not nextStop['gbtt_pta']):
                                expectedArrival = nextStop['gbtt_ptd']
                            else:
                                expectedArrival = nextStop['gbtt_pta']
                            actualDeparture = ""
                            if (not currentStop['actual_td']):
                                actualDeparture = expectedDeparture
                            else:
                                actualDeparture = currentStop['actual_td']
                            actualArrival = ""
                            if (not nextStop['actual_ta']):
                                actualArrival = expectedArrival
                            else:
                                actualArrival = nextStop['actual_ta']
                            
                            #datadatadata
                            #distanceFromDestination = _subtract_times(expectedDeparture, expectedArrival)
                            departureDelay = _subtract_times(expectedDeparture, actualDeparture)
                            arrivalDelay = _subtract_times(expectedArrival, actualArrival)
                            timeOfDay = expectedDeparture #roughly
                            #datadatadata
                            
                            historicalDataEntry = []
                            historicalDataEntry.append(location)
                            historicalDataEntry.append(destination)
                            #historicalDataEntry.append(toc) Not using for now
                            historicalDataEntry.append(timeOfDay)
                            historicalDataEntry.append(day)
                            #historicalDataEntry.append(distanceFromDestination) unused for now
                            historicalDataEntry.append(monthOfService)
                            historicalDataEntry.append(departureDelay)
                            historicalDataEntry.append(arrivalDelay)
                            historical_data.append(historicalDataEntry)
                
        return historical_data      

#this was the code used to generate "TrainingData.csv"
if __name__ == "__main__":
    a = pullHistoricalData(["NRW", "LST", "0000", "2359", "2017-01-01", "2017-12-31", "SATURDAY"])
    b = pullHistoricalData(["NRW", "LST", "0000", "2359", "2017-01-01", "2017-12-31", "SUNDAY"])       
    c = pullHistoricalData(["NRW", "LST", "0000", "2359", "2017-01-01", "2017-12-31", "WEEKDAY"])
    
    with open("TrainingData.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(a+b+c)
   

