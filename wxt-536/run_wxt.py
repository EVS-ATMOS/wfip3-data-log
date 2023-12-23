import serial
import time
import argparse
import csv

from datetime import datetime

# To display current ports:
# python -m serial.tools.list_ports

def search_ports(args):
    """
    Serial to USB devices can mount randomly to ports during reboot of a system.

    This function searches all available ports and determines the specific port
    for the WXT-536
    """
    # define all available ports
    

def pollsave(args):
    # check if you need to poll the data
    if args.poll is True:
        # Initalize communication with the instrument
        ser.write(bytearray(args.query + '\r\n', 'utf-8'))
    # Read the incoming serial data
    data = ser.readline()
    # check to make sure data are being returned
    if data:
        # define a timestamp for the data and append to data string
        time = datetime.now().strftime("%Y%m%dT%H:%M:%S.%f")
        datatime = time + ','+ data.decode('utf-8')
    else:
        datetime = None

    return datatime

def main(args):
    # start serial connection:
    with serial.Serial(args.device, args.baud_rate, timeout = 1) as ser:
        # create a file to write data to
        nfile = 'WXT536_' + args.site + '_' + datetime.now().strftime("%Y%m%d.%H%M%S")
        # check desired output from user. supports netcdf or csv
        if args.output == 'nc' or args.output == 'netcdf':
            filename = nfile + '.nc'
        else:
            filename = nfile + '.csv'
        # While Serial connection is valid
        while True:
            try:
                # query the instrument
                ndata = pollsave(args)
                # check to see if anything is returned
                ### Add debug line here? -> check how to store values
                if ndata:
                    if args.output == 'nc' or args.output == 'netcdf':
                        print("netcdf stuff")
                    else:
                        # Append to the file. 
                        with open(filename, "a") as myfile:
                            try:
                                writer = csv.writer(myfile, delimiter=",")
                                writer.writerow(ndata)
                            except:
                                print('Unable to write to file')                     
                time.sleep(args.freq)
            except:
                print("Keyboard Interrupt")
 
if __name__ == '__main__':
     parser = argparse.ArgumentParser(
            description="Script for interfacing with Viasala WXT 2D anemometer data")
 
     parser.add_argument("--debug",
                         action="store_true",
                         dest='debug',
                         help="enable debug logs"
                         )
     parser.add_argument("--device",
                         type=str,
                         dest='device',
                         default="/dev/ttyUSB0",
                         help="serial device to use"
                         )
     parser.add_argument("--baudrate",
                         type=int,
                         dest='baud_rate',
                         default=19200,
                         help="baudrate to use"
                         )
     parser.add_argument("--poll",
                         type=bool,
                         default=False,
                         help="Boolean Flag for if data are polled"
                         )
     parser.add_argument("--query",
                         type=str,
                         default="0R",
                         help="ASCII query command to send to the instrument"
                        )
     parser.add_argument("--output",
                         type=str,
                         dest='output',
                         default="csv",
                         help="output file format (csv or nc)"
                         )
     parser.add_argument("--site",
                         type=str,
                         dest="site",
                         default="atmos",
                         help="Site Identifier for Filename"
                         )
     parser.add_argument("--frequency",
                         type=int,
                         default=1,
                         dest="freq",
                         help="Temporal frequency of the data aquesition"
                         )
     args = parser.parse_args()

     main(args)