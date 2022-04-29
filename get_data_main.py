#Gets JSON files form the Plumme Labs API, if the items are larger that 2000
#the program makes the neccesary additional requests to ge the full data.
#After that it creates a new JSON file with all the data and with additional GMT
#and CST time representation for each item.
#All null values in the original JSON file are replaced with a O value in the new JSON.
#Finally, the JSON file is converted into a CSV file.
############### Author: Juan Antonio Robledo ###############
############### Github: https://github.com/TonyRob127 ###############
############### Last modification: April 29th 2022 ###############
import urllib.request, urllib.parse, urllib.error
import json
import ssl
import time
import pandas as pd

#Functions
def epoch_to_date(epoch_date, time_zone):
    if (time_zone == 'GMT'):
        my_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(epoch_date)))
    elif (time_zone == 'CST'):
        my_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(epoch_date)))
    else:
        print("Incorrect Time Zone, check source code")
        exit()
    return(my_time)
def check_null(pollut_name, value_type):
    if (str(flow_item['pollutants'][pollut_name][value_type]) == 'None'):
        return '0'
        
    else:
        return flow_item['pollutants'][pollut_name][value_type]
def create_data_dict():
    data_dict = dict()
    data_dict['epoch_val'] = flow_item['date']
    data_dict['timeGMT_val'] = epoch_to_date(flow_item['date'], 'GMT')
    data_dict['timeCST_val'] = epoch_to_date(flow_item['date'], 'CST')
    data_dict['no2_val'] =  check_null('no2','value')
    data_dict['no2_pi'] = check_null('no2','pi')
    data_dict['voc_val'] = check_null('voc','value')
    data_dict['voc_pi'] = check_null('voc','pi')
    data_dict['pm25_val'] = check_null('pm25','value')
    data_dict['pm25_pi'] = check_null('pm25','pi')
    data_dict['pm10_val'] =  check_null('pm10','value')
    data_dict['pm10_pi'] = check_null('pm10','pi')
    data_dict['pm1_val'] = check_null('pm1','value')
    data_dict['pm1_pi'] = check_null('pm1','pi')
    return data_dict
def date_to_epoch(h_date):
    time_format = '%Y-%m-%d %H:%M:%S'
    epoch_date = int(time.mktime(time.strptime(h_date,time_format)))
    return epoch_date
def spacing():
    print('*\n*\n*')

#API Parameters
flow_id = None
api_key = '' #Write your Plumme Labs API Token
start_date = None
end_date = None
api_offset = None
service_url = 'https://api.plumelabs.com/2.0/organizations/41/sensors/measures?'

#Other Parameters
flow_id_ls = list()
dict_lst = list()
api_params = dict()
call_n = None
usr_input = None
csv_file_path = '/home/tony/plumme_labs_python/flowdata_csvmain/flowdata_' #CHANGE PATH

#Ignore SSL certification errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#Welcome!
print("Welcome to the Get Data From Plumme Labs program!")
time.sleep(1)
print("NOTE: This program uses local time for the input of dates")
print("Check this website for more info: https://www.epochconverter.com/")
time.sleep(3)
spacing()

#Set time range for query
while True: 
    start_date = input('Input start date in the format yyyy-mm-dd hh:mm:ss\n')
    end_date = input('Input end date in format yyyy-mm-dd hh:mm:ss\n')

    #print('FROM: ', start_date)
    #print('TO: ', end_date)
    try: 
        start_date = date_to_epoch(start_date)
        end_date = date_to_epoch(end_date)
        spacing()
        break
    except:
        print("===== Error: time data does not match format '%Y-%m-%d %H:%M:%S' =====")
        continue

#Set the FlowID you want to consult
while True:
    usr_input = input("Please input Flow ID (5 digits), input 'no' when done: ")
    if(usr_input == 'no'):
        break
    try:
        int(usr_input)
    except:
        print("===== Error: Flow ID must be ONLY numbers =====")
        continue
    if (len(usr_input) != 5):
        print("===== Error: Flow ID must be ONLY 5 digits =====")
        continue
    flow_id_ls.append(usr_input)
    
spacing()

#Main loop for retrieving data
for flow_id in flow_id_ls:
#Set variable query parameters
    api_params['token'] = api_key
    api_params['start_date'] = start_date
    api_params['end_date'] = end_date
    api_params['sensor_id'] = flow_id
    api_params['offset'] = str(0)
    call_n = 0

#QUERY CALLS LOOP BEGINS
    while True:
        url = service_url + urllib.parse.urlencode(api_params)
        print('Retrieving: ', url)
        uh = urllib.request.urlopen(url, context=ctx)
        data = uh.read().decode()
        print('Retrieved', len(data), 'characters')
        spacing()

        try:
            js = json.loads(data)
            if (call_n == 0):
                print('Total of retrieved measures: ', js['total'])
        except:
            js = None
            print('===== Error: Failure to retrieve =====')
            continue
        #Creation of new JSON to append in a single CSV
        for flow_item in js['measures']:
            measures_dict =  dict()
            measures_dict = create_data_dict()
            dict_lst.append(measures_dict)
        
        if (js['more']):
            api_params['offset'] = str(js['offset'])
            print('===== Measurements > 2000, creating new query with offset: ', js['offset'],' =====')
            spacing()
        elif not (js['more']):
            json_hd = json.dumps(dict_lst)
            data_frame = pd.read_json(json_hd)
            data_frame.to_csv(csv_file_path + flow_id + '.csv', index=None) #CHANGE PATH
            print('Succesfull creation of CSV file for ID: ', flow_id)
            dict_lst.clear()
            api_params.clear()
            break

        call_n = call_n + 1
            
spacing()
print('===== Data retrieving completed!! =====\n Quitting program...')
time.sleep(2)
exit()


    