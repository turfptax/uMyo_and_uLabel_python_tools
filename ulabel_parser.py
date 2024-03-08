#parser

import ulabel_class
#import quat_math
#from quat_math import sV
#from quat_math import *
import math

#parse_buf = bytearray(0)

ulabel_list = []
unseen_cnt = []

def id2idx(uid):
    cnt = len(ulabel_list)
    u = 0
    while(u < cnt):
        if(unseen_cnt[u] > 1000 and ulabel_list[u].unit_id != uid):
            del ulabel_list[u]
            del unseen_cnt[u]
            cnt -= 1
        else: u += 1
    for u in range(cnt):
        unseen_cnt[u] += 1
        if(ulabel_list[u].unit_id == uid): 
            unseen_cnt[u] = 0
            return u
        
    ulabel_list.append(ulabel_class.uLabel(uid))
    unseen_cnt.append(0)
    return cnt

def ulabel_parse(parse_buf, pos):
    pp = pos
    rssi = parse_buf[pp-1]; #pp is guaranteed to be >0 by design
    packet_id = parse_buf[pp]; pp+=1
    packet_len = parse_buf[pp]; pp+=1
    unit_id = parse_buf[pp]; pp+=1; unit_id <<= 8
    unit_id += parse_buf[pp]; pp+=1; unit_id <<= 8
    unit_id += parse_buf[pp]; pp+=1; unit_id <<= 8
    unit_id += parse_buf[pp]; pp+=1
    idx = id2idx(unit_id)
#    packet_type = parse_buf[pp]; pp+=1
#    if(packet_type > 80 and packet_type < 120):
#        umyo_list[idx].data_count = packet_type - 80;
#        umyo_list[idx].packet_type = 80;
#    else:
#        return

    ulabel_list[idx].data_count = 5; #fixed for uLabel device
    ulabel_list[idx].rssi = rssi
    param_id = parse_buf[pp]; pp+=1
    pb1 = parse_buf[pp]; pp+=1
    pb2 = parse_buf[pp]; pp+=1
    pb3 = parse_buf[pp]; pp+=1
    if(param_id == 0):
        ulabel_list[idx].batt = 2000 + pb1*10;
        ulabel_list[idx].version = pb2
    print(ulabel_list[idx].version)
    data_id = parse_buf[pp]; pp+=1
    d_id = data_id - ulabel_list[idx].prev_data_id
    ulabel_list[idx].prev_data_id = data_id
    if(d_id < 0): d_id += 256
    ulabel_list[idx].data_id += d_id
    for x in range(ulabel_list[idx].data_count):
        hb = parse_buf[pp]; pp+=1
        lb = parse_buf[pp]; pp+=1
        val = hb*256 + lb
#        if(hb > 127):
#            val = -65536 + val
        ulabel_list[idx].hall_values[x] = val

    hb = parse_buf[pp]; pp+=1; lb = parse_buf[pp]; pp+=1; val = hb*256 + lb    
    if(val > 32767): val = -(65536-val)
    qww = val
    hb = parse_buf[pp]; pp+=1; lb = parse_buf[pp]; pp+=1; val = hb*256 + lb    
    if(val > 32767): val = -(65536-val)
    qwx = val
    hb = parse_buf[pp]; pp+=1; lb = parse_buf[pp]; pp+=1; val = hb*256 + lb    
    if(val > 32767): val = -(65536-val)
    qwy = val
    hb = parse_buf[pp]; pp+=1; lb = parse_buf[pp]; pp+=1; val = hb*256 + lb    
    if(val > 32767): val = -(65536-val)
    qwz = val

    hb = parse_buf[pp]; pp+=1; lb = parse_buf[pp]; pp+=1; val = hb*256 + lb    
    if(val > 32767): val = -(65536-val)
    ax = val
    hb = parse_buf[pp]; pp+=1; lb = parse_buf[pp]; pp+=1; val = hb*256 + lb    
    if(val > 32767): val = -(65536-val)
    ay = val
    hb = parse_buf[pp]; pp+=1; lb = parse_buf[pp]; pp+=1; val = hb*256 + lb    
    if(val > 32767): val = -(65536-val)
    az = val
    
    hb = parse_buf[pp]; pp+=1; lb = parse_buf[pp]; pp+=1; val = hb*256 + lb    
    if(val > 32767): val = -(65536-val)
    yaw = val
    hb = parse_buf[pp]; pp+=1; lb = parse_buf[pp]; pp+=1; val = hb*256 + lb    
    if(val > 32767): val = -(65536-val)
    pitch = val
    hb = parse_buf[pp]; pp+=1; lb = parse_buf[pp]; pp+=1; val = hb*256 + lb    
    if(val > 32767): val = -(65536-val)
    roll = val

    ulabel_list[idx].Qsg[0] = qww
    ulabel_list[idx].Qsg[1] = qwx
    ulabel_list[idx].Qsg[2] = qwy
    ulabel_list[idx].Qsg[3] = qwz
    ulabel_list[idx].dev_yaw = yaw
    ulabel_list[idx].dev_pitch = pitch
    ulabel_list[idx].dev_roll = roll
    ulabel_list[idx].ax = ax
    ulabel_list[idx].ay = ay
    ulabel_list[idx].az = az

#    print(data_id)
'''
def ulabel_parse_preprocessor(data):
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
                ulabel_parse(i+3)
                parsed_pos = i+2+packet_len
                i += 1+packet_len
#                del parse_buf[0:i+2+packet_len]
#                break
    if(parsed_pos > 0): del parse_buf[0:parsed_pos]
    return cnt
'''
def ulabel_get_list():
    return ulabel_list
