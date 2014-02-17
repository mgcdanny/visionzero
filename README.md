Aggregating Public Collision and Traffic Summons Data from NYPD Website:


Described in more detail here:
http://mgcdanny.blogspot.com/2014/02/public-data-public-health-and-python.html


The two main files are:

getCollision.py

getSummons.py

Which download, organize, and format all the archived excel files posted at these two respectice websites:

http://www.nyc.gov/html/nypd/html/traffic_reports/traffic_summons_reports.shtml

http://www.nyc.gov/html/nypd/html/traffic_reports/motor_vehicle_collision_data.shtml


These scripts will create folders, download many excel files into those folders, iterate through those excel files, cleaning each one and appending the data into one giant csv file per script.  The result is one csv file for collision data and one csv file for summons data which are put into the main folder:

allSummons.csv
allAccidents.csv

