#kinda main

import umyo_parser
import ulabel_parser
import ulabel_display
from datetime import datetime

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

print("conn: " + ser.portstr)
last_data_upd = 0
ulabel_display.plot_init()
parse_unproc_cnt = 0
uML_Data = []
data = []
while(1):
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
            uML_Data.append(['ulabel#0',ulabel_list[0].hall_values,datetime.now()])
            for i,x in enumerate(umyo_parser.umyo_get_list()):
                uML_Data.append([f'umyo#:{i}',x.data_array[:8],datetime.now()])
            data.append(uML_Data)
            uML_Data = []
            print('data')
#	        print(ulabel_list[0].ax)
#	        print(ulabel_list[0].batt)
#	        print(ulabel_list[0].data_id)
        dat_id = ulabel_display.plot_prepare(ulabel_parser.ulabel_get_list())
        d_diff = 0
        if(not (dat_id is None)):
            d_diff = dat_id - last_data_upd
        if(d_diff > 2 + cnt_corr):
           #display_stuff.plot_cycle_lines()
            #ulabel_display.plot_cycle_tester()
            last_data_upd = dat_id

with open('emg_and_label_data.txt', 'w') as file:
    file.write(str(uML_Data))

file.close()
