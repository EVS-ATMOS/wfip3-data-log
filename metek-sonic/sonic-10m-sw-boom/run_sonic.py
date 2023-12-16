import serial
import csv
import time
from datetime import datetime
from datetime import timedelta

# Read the incoming serial data....
ser = serial.Serial(port='COM4',baudrate=57600,bytesize=8,stopbits=1)
ser.flushInput()
while True:
    try:
        ser_bytes = ser.readline()
        text = str(ser_bytes,'utf-8').strip()
                        
        timenow = datetime.now()
        filename = 'METEK_'+ str(timenow.strftime('%Y_%m_%d_%H'))+".csv"
        print(filename)
        
        with open(filename,"a") as f:
            
            writer = csv.writer(f,delimiter=",")
            try:
                writer.writerow([time.strftime('%Y-%m-%d'),datetime.now().strftime('%H:%M:%S.%f'),text.split(";")[1],text.split(";")[2],text.split(";")[3],text.split(";")[4]])
            
            except:
                continue
            
    except:
        print("keyboard interrupt")
        break
