#kinda main

import umyo_parser
import ulabel_parser
import ulabel_display
from datetime import datetime
import time
import os
import csv

# list
from serial.tools import list_ports
port = list(list_ports.comports())
print("available ports:")
for p in port:
    print(p.device)
    device = p.device
print("===")

#read
import serial
ser = serial.Serial(port=device, baudrate=921600, parity=serial.PARITY_NONE, stopbits=1, bytesize=8, timeout=0)


parse_buf = bytearray(0)

def parse_preprocessor(data):
    parse_buf.extend(data)
    cnt = len(parse_buf)
    if(cnt < 72):
        return 0
    parsed_pos = 0
    for i in range(cnt-70):
        if(parse_buf[i] == 79 and parse_buf[i+1] == 213):
            rssi = parse_buf[i+2]
            packet_id = parse_buf[i+3]
            packet_len = parse_buf[i+4]
            if(packet_len > 20 and i + 3 + packet_len < cnt):
                if(parse_buf[i+3+6] > 2):
                    umyo_parser.umyo_parse(parse_buf, i+3)
                else:
                    ulabel_parser.ulabel_parse(parse_buf, i+3)
                parsed_pos = i+2+packet_len
                i += 1+packet_len
#            else:
#                del parse_buf[0:i+2+packet_len]
#                break
    if(parsed_pos > 0): del parse_buf[0:parsed_pos]
    return cnt

def get_file_number_and_timestamp(directory):
    # Ensure the subfolder exists, create if it doesn't
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Count the number of files in the subfolder
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    file_number = len(files) + 1
    
    # Generate timestamp in a compact format
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    return file_number, timestamp

def get_ulabel_data(ulabel_data):
    global start_time
    # Return a sample list of uLabel data
    attribute_names = ['uid', 'batt', 'hall_values', 'Qsg','zeroQ','ax','ay','az','dev_yaw','dev_pitch','dev_roll']
    data = {}
    for name in attribute_names:
        # Use getattr to get the value, with a default value if the attribute does not exist
        value = getattr(ulabel_data, name, 'Attribute not found')
        data[name] = value
    #print('uLabel',data)
    ordered = ['1',data['hall_values'][0],data['hall_values'][1],data['hall_values'][2],data['hall_values'][3],data['hall_values'][4],
            data['ax'],data['ay'],data['az'],data['dev_yaw'],data['dev_pitch'],data['dev_roll'],time.time()-start_time]
    #print(ordered)
    #print('------------------')
    return ordered


def get_umyo_data(umyo_data):
    global start_time
    # Return a sample list of uMyo data for each device
    attribute_names = ['uid', 'batt', 'data_array','device_spectr', 'Qsg','zeroQ','ax','ay','az','dev_yaw','dev_pitch','dev_roll','mag_angle']
    uMyos = []
    for zz,umyo in enumerate(umyo_data):
        data = {}
        for name in attribute_names:
            # Use getattr to get the value, with a default value if the attribute does not exist
            value = getattr(umyo, name, 'Attribute not found')
            data[name] = value
        d = data['data_array']
        ds = data['device_spectr']
        ordered = [f'{zz}',d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7],ds[0],ds[1],ds[2],ds[3],
                data['ax'],data['ay'],data['az'],data['dev_yaw'],data['dev_pitch'],data['dev_roll'],time.time()-start_time]
        uMyos.append(ordered)
    return uMyos

def append_to_csv(file_name,ulabel_data, umyo_data):
    with open(file_name, 'a', newline='') as file:
        writer = csv.writer(file)
        # Construct dynamic headers based on the number of uMyo devices
        headers = ['uLabel','h1','h2','h3','h4','h5','ax','ay','az','uL dev_yaw','uL dev_pitch','uL dev_roll','uL Timestamp']
        for i in range(1, 5):
            headers.extend([f'uMyo{i}',f'uM{i} d1',f'uM{i} d2',f'uM{i} d3',f'uM{i} d4',f'uM{i} d5',f'uM{i} d6',f'uM{i} d7',f'uM{i} d8',f'uM{i} ds1',f'uM{i} ds2',f'uM{i} ds3',f'uM{i} ds4',
                            f'uM{i} ax',f'uM{i} ay',f'uM{i} az',f'uM{i} dev_yaw',f'uM{i} dev_pitch',f'uM{i} dev_roll',f'uM{i} Timestamp'])
        writer.writerow(headers) if file.tell() == 0 else None  # Write headers if file is empty
        row_data = ulabel_data
        #print('umo_data_csv',umyo_data)
        for i in umyo_data:
            row_data.extend(i)
        writer.writerow(row_data)

def write_to_csv(file_name):
    global recording_data
    for zzz in recording_data:
        with open(file_name, 'a', newline='') as file:
            writer = csv.writer(file)
            # Construct dynamic headers based on the number of uMyo devices
            headers = ['uLabel','h1','h2','h3','h4','h5','ax','ay','az','uL dev_yaw','uL dev_pitch','uL dev_roll','uL Timestamp']
            for i in range(1, 5):
                headers.extend([f'uMyo{i}',f'uM{i} d1',f'uM{i} d2',f'uM{i} d3',f'uM{i} d4',f'uM{i} d5',f'uM{i} d6',f'uM{i} d7',f'uM{i} d8',f'uM{i} ds1',f'uM{i} ds2',f'uM{i} ds3',f'uM{i} ds4',
                                f'uM{i} ax',f'uM{i} ay',f'uM{i} az',f'uM{i} dev_yaw',f'uM{i} dev_pitch',f'uM{i} dev_roll',f'uM{i} Timestamp'])
            writer.writerow(headers) if file.tell() == 0 else None  # Write headers if file is empty
            writer.writerow(zzz)


def append_to_object(file_name,ulabel_data,umyo_data):
    global recording_data
    global loop_time
    line = ulabel_data
    for i in umyo_data:
        line.extend(i)
    recording_data.append(line)

    


print("conn: " + ser.portstr)
last_data_upd = 0
ulabel_display.plot_init()
parse_unproc_cnt = 0
uML_Data = []
data = []

recording_data = []
loop_time = time.time()

#USER DEFINED VARIABLES
SUBFOLDER = 'training_data'
file_number, timestamp = get_file_number_and_timestamp(SUBFOLDER)
FILE_NAME = f"{SUBFOLDER}/uMyo_uLabel_Recording_{file_number}_{timestamp}.csv"

# User instructions
print("Training will start now. Please follow the on-screen instructions.")

# Set the duration of the loop in seconds
duration = 20  # For example, 5 minutes


start_time = time.time()  # Record the start time
last_print_time = start_time  # Keep track of the last time we printed the message


while(time.time() - start_time < duration):
    current_time = time.time()
    elapsed_time = current_time - start_time
    if(current_time - last_print_time >= 5):
        percentage_complete = (elapsed_time / duration) * 100
        print(f"Elapsed time: {elapsed_time:.2f}s / {duration}s ({percentage_complete:.2f}%)")
        last_print_time = current_time
    # Loop for gathering serial data from uMyo and uLabel
    cnt = ser.in_waiting
    if(cnt > 0):
        cnt_corr = parse_unproc_cnt/200
        data = ser.read(cnt)
        parse_unproc_cnt = parse_preprocessor(data)
        umyo_list = umyo_parser.umyo_get_list()
        if(len(umyo_list) > 0):
                print("uMyo: ", umyo_parser.umyo_get_list()[0].data_array[4])      
        ulabel_list = ulabel_parser.ulabel_get_list()
        if(len(ulabel_list) > 0):
            print("vals: ")
            print(ulabel_list[0].hall_values)
            # gather data and write to csv file
            ulabel_data = get_ulabel_data(ulabel_list[0])
            umyo_data = get_umyo_data(umyo_parser.umyo_get_list())
            append_to_object(FILE_NAME,ulabel_data,umyo_data)
        dat_id = ulabel_display.plot_prepare(ulabel_parser.ulabel_get_list())
        d_diff = 0
        if(not (dat_id is None)):
            d_diff = dat_id - last_data_upd
        if(d_diff > 2 + cnt_corr):
           #display_stuff.plot_cycle_lines()
            #ulabel_display.plot_cycle_tester()
            last_data_upd = dat_id

write_to_csv(FILE_NAME)
print("Training completed.")

