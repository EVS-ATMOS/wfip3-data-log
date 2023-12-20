import serial
import csv
import time
from datetime import datetime
import re

# Read the incoming serial data....
ser = serial.Serial(port='COM4',baudrate=57600,bytesize=8,stopbits=1)
ser.flushInput()

# Define a regular expression to subset the serial input
pattern = re.compile(r'\\x02(.*?)\\x03')

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
                matches = pattern.findall(text)
                if matches:
                    print('number of samples received', len(matches))
                    print(matches[line].split('\\\\')[0].split(';')) for line in matches)
                    [write.writerow(matches[line].split('\\\\')[0].split(';')) for line in matches]
                    ##for line in matches:
                    ##    writer.writerow(matches[line].split('\\\\')[0].split(';'))
                else:
                    print('No Matches Found; Instrument Output:')
                    print(text)
            except:
                continue
            
    except:
        print("keyboard interrupt")
        break
