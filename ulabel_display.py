#drawing via pygame

import sys, pygame
from math import *
pygame.init()

max_devices = 1
size = width, height = 1200, 500
screen = pygame.display.set_mode(size)

plot_len = 2000
plot_H0 = []
plot_H1 = []
plot_H2 = []
plot_H3 = []
plot_H4 = []
plot_ax = []
plot_ay = []
plot_az = []
dev_rssi = [0]*max_devices
dev_batt = [0]*max_devices
y_scale0 = [0.01]*max_devices
y_scale1 = [0.01]*max_devices
y_scale2 = [0.01]*max_devices
y_scale3 = [0.01]*max_devices
y_scale4 = [0.1]*max_devices
y_zero0 = [32000]*max_devices
y_zero1 = [32000]*max_devices
y_zero2 = [32000]*max_devices
y_zero3 = [32000]*max_devices
y_zero4 = [32000]*max_devices
last_data_id = [0]*max_devices
not_updated_cnt = [10000]*max_devices
active_devices = 0

def plot_init():
    global max_devices
    for i in range(max_devices):
        plot_H0.append([0]*plot_len)
        plot_H1.append([0]*plot_len)
        plot_H2.append([0]*plot_len)
        plot_H3.append([0]*plot_len)
        plot_H4.append([0]*plot_len)
        plot_ax.append([0]*plot_len)
        plot_ay.append([0]*plot_len)
        plot_az.append([0]*plot_len)

def num_to_color(n):
    if(n == 0): return 0, 200, 0
    if(n == 1): return 0, 100, 200
    if(n == 2): return 150, 150, 0
    if(n == 3): return 200, 0, 250
    if(n == 4): return 100, 250, 100
    if(n == 5): return 100, 250, 250
    if(n == 6): return 250, 250, 100
    return 100, 100, 100

def plot_cycle_tester():
    global plot_spg, max_devices, last_data_id, active_devices
    for event in pygame.event.get():
        if(event.type == pygame.QUIT): sys.exit()
    screen.fill([0,0,0])
    cur_devices = 0
    screen.lock()
    for d in range(max_devices):
        if(not_updated_cnt[d] > 1000): continue
        cur_devices += 1
        xy0 = []
        xy1 = []
        xy2 = []
        xy3 = []
        xy4 = []
        DX = 10
        DY = height/(1+active_devices) * (d+1)
        x_scale = (width - DX*2) / plot_len
        
        DX = 10
        YS = height/2 #/(active_devices+1)
        DY = height/2 # - YS*6*active_devices/2 + YS*6*(cur_devices-1) # (1+active_devices) * (d+1)
        x_scale = 0.8*(width - DX*2) / plot_len
        
        for x in range(plot_len):
            xy0.append([DX+x*x_scale, DY+(plot_H0[d][x]-y_zero0[d])*y_scale0[d]])
            xy1.append([DX+x*x_scale, DY+(plot_H1[d][x]-y_zero1[d])*y_scale1[d]])
            xy2.append([DX+x*x_scale, DY+(plot_H2[d][x]-y_zero2[d])*y_scale2[d]])
            xy3.append([DX+x*x_scale, DY+(plot_H3[d][x]-y_zero3[d])*y_scale3[d]])
            xy4.append([DX+x*x_scale, DY+(plot_H4[d][x]-y_zero4[d])*y_scale4[d]])
        cl = num_to_color(d)
        
        pygame.draw.lines(screen, num_to_color(0), False, xy0)
        pygame.draw.lines(screen, num_to_color(1), False, xy1)
        pygame.draw.lines(screen, num_to_color(2), False, xy2)
        pygame.draw.lines(screen, num_to_color(3), False, xy3)
        pygame.draw.lines(screen, num_to_color(4), False, xy4)

        xy = []
        for x in range(plot_len):
            ax = plot_ax[d][x] / 8129 * YS + YS*4
            xy.append([DX+x*x_scale, DY*1.2+ax])

        cl = 255,0,0 #num_to_color(d)        
        pygame.draw.lines(screen, cl, False, xy)

        xy = []
        for x in range(plot_len):
            ay = plot_ay[d][x] / 8129 * YS + YS*4
            xy.append([DX+x*x_scale, DY*1.2+ay])

        cl = (255,255,0) #num_to_color(d)        
        pygame.draw.lines(screen, cl, False, xy)

        xy = []
        for x in range(plot_len):
            az = plot_az[d][x] / 8129 * YS + YS*4
            xy.append([DX+x*x_scale, DY*1.2+az])

        cl = (0,0,255) #num_to_color(d)        
        pygame.draw.lines(screen, cl, False, xy)

        DX = 10   
        DY = 40     

#RSSI drawing        
        xy = []
        xy.append([DX + width*0.05, DY - 30])
        xy.append([DX + width*0.35, DY - 30])
        xy.append([DX + width*0.35, DY - 5])
        xy.append([DX + width*0.05, DY - 5])
        xy.append([DX + width*0.05, DY - 30])
        cl = 255,255,255
        pygame.draw.lines(screen, cl, False, xy)
        
        sig_level = 0
        if(dev_rssi[d] > 1):
            sig_level = (90 - dev_rssi[d])*1.6 #reasonable 0-100 scale
        if(sig_level < 0): sig_level = 0
        if(sig_level > 100): sig_level = 100
        cl = 200,0,0
        if(sig_level > 30): cl = 200,100,0
        if(sig_level > 55): cl = 0,100,150
        if(sig_level > 80): cl = 0,200,0
        
        x_sz = sig_level*0.01 * width*0.3 - 2
        screen.fill(cl,(DX + width*0.05+1,DY - 29,x_sz,23))

#Battery drawing        
        batt_perc = (dev_batt[d] - 3100)/10
        if(batt_perc < 0): batt_perc = 0
        batt_dx = DX + width*0.9
        batt_w = width * 0.03
        batt_dy = DY
        batt_h = height/5
        xy = []
        xy.append([batt_dx, batt_dy])
        xy.append([batt_dx, batt_dy + batt_h])
        xy.append([batt_dx + batt_w, batt_dy + batt_h])
        xy.append([batt_dx + batt_w, batt_dy])
        xy.append([batt_dx, batt_dy])
        cl = 50,150,150
        if(batt_perc < 20): cl = 150,0,0
        pygame.draw.lines(screen, cl, False, xy)
        cl = 0,200,0
        if(batt_perc < 70): cl = 0,100,150
        if(batt_perc < 40): cl = 150,150,0
        if(batt_perc < 15): cl = 255,0,0
        batt_fh = batt_h * batt_perc / 100 - 1
        if(batt_fh < 2): batt_fh = 2
        screen.fill(cl,(batt_dx+1,batt_dy + batt_h - batt_fh - 1, batt_w - 2, batt_fh))
        
        
        
            
#    screen.blit(ball, ballrect)
    screen.unlock()
    pygame.display.flip()        
    active_devices = cur_devices
    return active_devices

def plot_prepare(devices):
    global plot_emg, plot_spg, max_devices, last_data_id, y_zero, active_devices
    for i in range(max_devices): not_updated_cnt[i] += 1
    cnt = len(devices)
    if(cnt < 1): return
    for d in range(cnt):
        if(devices[d].data_id != last_data_id[d]):
            not_updated_cnt[d] = 0
            plot_H0[d].append(devices[d].hall_values[0])
            plot_H1[d].append(devices[d].hall_values[1])
            plot_H2[d].append(devices[d].hall_values[2])
            plot_H3[d].append(devices[d].hall_values[3])
            plot_H4[d].append(devices[d].hall_values[4])
                        
            plot_ax[d].append(devices[d].ax)
            plot_ay[d].append(devices[d].ay)
            plot_az[d].append(devices[d].az)
            
            y_zero0[d] *= 0.999;
            y_zero0[d] += 0.001 * devices[d].hall_values[0];
            y_zero1[d] *= 0.999;
            y_zero1[d] += 0.001 * devices[d].hall_values[1];
            y_zero2[d] *= 0.999;
            y_zero2[d] += 0.001 * devices[d].hall_values[2];
            y_zero3[d] *= 0.999;
            y_zero3[d] += 0.001 * devices[d].hall_values[3];
            y_zero4[d] *= 0.999;
            y_zero4[d] += 0.001 * devices[d].hall_values[4];
            
        last_data_id[d] = devices[d].data_id
        if(hasattr(devices[d], 'rssi')):
            dev_rssi[d] = devices[d].rssi
        if(hasattr(devices[d], 'batt')):
            dev_batt[d] = devices[d].batt
        if(len(plot_H0[d]) < 2): return
        plot_H0[d] = plot_H0[d][-plot_len:]
        plot_H1[d] = plot_H1[d][-plot_len:]
        plot_H2[d] = plot_H2[d][-plot_len:]
        plot_H3[d] = plot_H3[d][-plot_len:]
        plot_H4[d] = plot_H4[d][-plot_len:]
        plot_ax[d] = plot_ax[d][-plot_len:]
        plot_ay[d] = plot_ay[d][-plot_len:]
        plot_az[d] = plot_az[d][-plot_len:]
#    print(plot_emg[0])
    return devices[0].data_id

