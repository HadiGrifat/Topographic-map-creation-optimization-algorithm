from pymavlink import mavutil
import keyboard
import csv
from datetime import datetime

# Connecting to Pixhawk
pix_connect = mavutil.mavlink_connection('COM6', baud=9600) # GPS module can reach 25 Hz update rate, currently 2 Hz, change in MissionPlanner

sample_id = 0 # variable to count samples

# Wait for first heartbeat
pix_connect.wait_heartbeat()
print("Connected to Pixhawk")

filename = f'gps_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
csvfile = open(filename, 'w', newline='')
writer = csv.writer(csvfile)
writer.writerow(['sample id', 'timestamp', 'latitude', 'longitude', 'altitude'])

while True:
    if keyboard.is_pressed('q'):
        print("Exiting loop.")
        break

    msg = pix_connect.recv_match(type='GPS_RAW_INT', blocking=True)
    #msg2 = pix_connect.recv_match(type='ALTITUDE', blocking=True) # barometer settings
    #if msg and msg2: # barometer settings
    if msg:
        lat = msg.lat / 1e7
        lon = msg.lon / 1e7
        alt = msg.alt / 1000.0  # in meters, alt is usually given in mm
        #alt_bar = msg2.relative_alt # barometer settings
        sample_id += 1
        print(f"ID: {sample_id}, Lat: {lat}, Lon: {lon}, Alt: {alt}")
        timestamp = datetime.now().isoformat()
        #writer.writerow([sample_id, timestamp, lat, lon, alt])

csvfile.close()