import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as md
import time

def epoch_to_date(epoch_date):
    my_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(epoch_date)))
    return(my_time)
def spacing():
    print('*\n*\n*')

print('Welcome to get_graphs from Flow data program!\n')
time.sleep(1)

#Variables
x_val = []
y_val = []
flow_id_ls = []
pollut_ls = ['no2', 'voc', 'pm25', 'pm10', 'pm1']
usr_input = None
event_name = input("Please input the event or experiment name attached to the csv files you want to plot: \n")
while True:
    usr_input = input("Please input Flow ID (5 digits), input 'no' when done: ")
    if(usr_input == 'no'):
        break
    try:
        int(usr_input)
    except:
        print("Flow ID must be ONLY numbers")
        continue
    if (len(usr_input) != 5):
        print("Flow ID must be ONLY 5 digits")
        continue

    flow_id_ls.append(usr_input)
spacing()
print("The following IDs' data will be plotted and saved: ", flow_id_ls, '\n')

for id in flow_id_ls:
    print("-Processing Data from Flow ", id)
    try:
        df = pd.read_csv('/home/tony/plumme_labs_python/flowdata_csvmain/' + event_name + '_flowdata_' + id + '.csv')
    except:
        print('====== Error: CSV file was not found for Flow ', id, ' ======')
        continue
    for epoch in df['epoch_val']:
            x_val.append(epoch_to_date(epoch))
    datenum = md.date2num(x_val)
    for pollut in pollut_ls:
        for pollutval in df[pollut + '_val']:
            y_val.append(float(pollutval))
        plt.figure(figsize=(20,10)) #width, height
        plt.title('Flow ' + id + ': ' + pollut.upper() + ' vs Time')
        plt.xlabel("fecha y hora (CST)")
        if(pollut == 'no2' or pollut == 'voc'):
            plt.ylabel("ppb")
        else:
            plt.ylabel('ug/m3')
        plt.xticks(rotation=25)
        plt.grid()
        ax = plt.gca()
        xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
        ax.xaxis.set_major_formatter(xfmt)
        plt.plot(datenum, y_val)
        plt.savefig('/home/tony/plumme_labs_python/figures/'+ event_name + '_' + pollut +'_flow' + id + '.png', bbox_inches = 'tight')
        time.sleep(1)
        plt.close()
        y_val.clear()
    x_val.clear()
print("\nThe figures where saved succesfully!!!")
print("Quitting...")
exit()
