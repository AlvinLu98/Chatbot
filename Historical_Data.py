import requests
import json
import csv
import Database_controller

def add_training_data(query):
    rids  = retrieve_past_rids(query)
    data = retrieve_hisotrical_arrival_data(rids, query[6])
    print("Adding data to database.....")
    for entry in data:
        Database_controller.add_historical_data(entry)
        

#https://wiki.openraildata.com/index.php/HSP
def retrieve_past_rids(query):
    url = "https://hsp-prod.rockshore.net/api/v1/serviceMetrics"
    headers = { "Content-Type": "application/json" }
    auths = ("lulianghao@gmail.com", "AI_CW_Group2")

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

    rid_list = []

    request = requests.post(url, headers=headers, auth=auths, json=data)
    if(request):
        print("Gathering data for %4s on %8s....." %(query[4][:4], query[6]))
        readData = json.loads(request.text)
        for service in readData['Services']:
            service_rids = service['serviceAttributesMetrics']['rids']
            for rid in service_rids:
                rid_list.append(rid)
    return rid_list

def retrieve_hisotrical_arrival_data(rids, day):
    historical_data = []
    url = "https://hsp-prod.rockshore.net/api/v1/serviceDetails"
    headers = { "Content-Type": "application/json" }
    auths = ("lulianghao@gmail.com", "AI_CW_Group2")

    print("Processing data.......")
    for rid in rids:
        data = {
              "rid": rid
            }
        request = requests.post(url, headers=headers, auth=auths, json=data, verify=True)
        if(request):
            readData = json.loads(request.text)
            service_date = readData['serviceAttributesDetails']['date_of_service']
            toc = readData['serviceAttributesDetails']['toc_code']
            stops = readData['serviceAttributesDetails']['locations']
            num_stops = len(stops)

            if num_stops > 1:
                for s in range(num_stops - 1):
                    for e in range(1, num_stops - s):
                        current_data = stops[s]
                        next_data = stops[s + e]

                        #Location data
                        origin = current_data['location']
                        destination = next_data['location']

                        #Departure data
                        exp_dep = " "
                        if not current_data['gbtt_ptd']:
                            exp_dep = current_data['gbtt_pta']
                        else:   
                            exp_dep = current_data['gbtt_ptd']
                        
                        act_dep = ""
                        if(not current_data['actual_td']):
                            act_dep = exp_dep
                        else:
                            act_dep = current_data['actual_td']

                        #Arrival data
                        exp_arr = ""
                        if not next_data['gbtt_pta']:
                            exp_arr = next_data['gbtt_ptd']
                        else:
                            exp_arr = next_data['gbtt_pta']

                        act_arr = ""
                        if(not next_data['actual_ta']):
                            act_arr = exp_arr
                        else:
                            act_arr = next_data['actual_ta']

                        #Delay data
                        dep_delay = time_diff(exp_dep, act_dep)
                        arr_delay = time_diff(exp_arr, act_arr)

                        historical_entry = []
                        historical_entry.append(origin)
                        historical_entry.append(exp_dep)
                        historical_entry.append(dep_delay)
                        historical_entry.append(destination)
                        historical_entry.append(exp_arr)
                        historical_entry.append(arr_delay)
                        historical_entry.append(service_date.split('-')[1])
                        historical_entry.append(day)
                        historical_entry.append(toc)
                        historical_data.append(historical_entry)
    return historical_data

def to_minutes(time):
    hr = time[:2]
    mins = time[-2:]
    return int(hr) * 60 + int(mins)

def time_diff(time_1, time_2):
    time_1_min = to_minutes(time_1)
    time_2_min = to_minutes(time_2)
    diff_min = time_2_min - time_1_min

    time_1_hr = int(time_1[:2])
    time_2_hr = int(time_2[:2])
    if time_1_hr != 0 and time_2_hr == 0:
        diff_min += 1440 #add 1 day in mins to the difference
    elif time_2_hr != 0 and time_1_hr == 0:
        diff_min -= 1440
    return diff_min

def main():
    # print(str(time_diff("2359", "0010")))
    
    # rids = retrieve_past_rids(["NRW", "LST", "0000", "2359", "2017-01-01", "2017-12-31", "SATURDAY"])
    # retrieve_hisotrical_arrival_data(rids, "SATURDAY")

    query1 = ["NRW", "LST", "0000", "2359", "2018-01-01", "2018-12-31", "WEEKDAY"]
    query2 = ["NRW", "LST", "0000", "2359", "2018-01-01", "2018-12-31", "SATURDAY"]
    query3 = ["NRW", "LST", "0000", "2359", "2018-01-01", "2018-12-31", "SUNDAY"]

    query4 = ["NRW", "LST", "0000", "2359", "2017-01-01", "2017-12-31", "WEEKDAY"]
    query5 = ["NRW", "LST", "0000", "2359", "2017-01-01", "2017-12-31", "SATURDAY"]
    query6 = ["NRW", "LST", "0000", "2359", "2017-01-01", "2017-12-31", "SUNDAY"]

    query7 = ["NRW", "LST", "0000", "2359", "2016-01-01", "2016-12-31", "WEEKDAY"]
    query8 = ["NRW", "LST", "0000", "2359", "2016-01-01", "2016-12-31", "SATURDAY"]
    query9 = ["NRW", "LST", "0000", "2359", "2016-01-01", "2016-12-31", "SUNDAY"]

    add_training_data(query1)
    add_training_data(query2)
    add_training_data(query3)
    add_training_data(query4)
    add_training_data(query5)
    add_training_data(query6)
    add_training_data(query7)
    add_training_data(query8)
    add_training_data(query9)
    
if __name__ == '__main__':
    main()