# flowsensordata_retrieve
Python program for the automation of the data retrieve of a FLOW 2 personal air monitor from the Plumme Labs API. Generates a CSV file with full sensed data in a specific time span. It allows to get data from multiple FLOW 2 sensors.
To start using the program we have to add some configurations to the source code first:
            
            Search for the csv_file_path variable in the source code and replace the original path string with your own without modifying the last part of the string     (/flowdata_). Here you must write the directory you want your CSV files to be storaged.
            Search for the api_key variable in the source code and set your Plumme Labs API key since it is necessary to access the data in their cloud service.

Once this configuration is done, the program is ready to use from the terminal using the command "python3 get_data_main.py"
