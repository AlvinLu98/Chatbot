import requests
import json
import csv
import Database_controller

def get_training_data(query, s_year, e_year):
    rids  = retrieve_past_rids(query)
    data = retrieve_hisotrical_arrival_data(rids, query[6])
    for entry in data:
        print(entry)

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

    for rid in rids:
        data = {
              "rid": rid
            }
        request = requests.post(url, headers=headers, auth=auths, json=data, verify=True)
        if(request):
            readData = json.loads(request.text)
            service_date = readData['serviceAttributesDetails']['date_of_service']
            stops = readData['serviceAttributesDetails']['locations']
            num_stops = len(stops)

            if num_stops > 1:
                for s in range(num_stops - 1):
                    for e in range(num_stops - s):
                        current_data = stops[s]
                        next_data = stops[s + e]

                        #Location data
                        origin = current_data['location']
                        destination = next_data['location']

                        #Departure data
                        exp_dep = current_data['gbtt_ptd']
                        act_dep = ""
                        if(not current_data['actual_td']):
                            act_dep = exp_dep
                        else:
                            act_dep = current_data['actual_td']

                        #Arrival data
                        exp_arr = next_data['gbtt_pta']
                        act_arr = ""
                        if(not next_data['actual_ta']):
                            act_arr = exp_arr
                        else:
                            act_arr = next_data['actual_ta']

                        #Delay data
                        dep_delay = 0
                        if exp_dep:
                            dep_delay = time_diff(exp_dep, act_dep)
                        
                        arr_delay = 0
                        if exp_arr:
                            arr_delay = time_diff(exp_arr, act_arr)
                        historical_entry = []
                        historical_entry.append(origin)
                        historical_entry.append(dep_delay)
                        historical_entry.append(destination)
                        historical_entry.append(arr_delay)
                        historical_entry.append(service_date.split('-')[1])
                        historical_entry.append(day)
                        print(historical_entry)

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
    if(time_1_hr > time_2_hr):
        diff_min += 1440 #add 1 day in mins to the difference
    
    return diff_min

def main():
    # print(str(time_diff("20:00", "00:35")))
    
    rids = retrieve_past_rids(["NRW", "LST", "0000", "2359", "2017-01-01", "2017-12-31", "SATURDAY"])
    retrieve_hisotrical_arrival_data(rids, "SATURDAY")
    
if __name__ == '__main__':
    main()