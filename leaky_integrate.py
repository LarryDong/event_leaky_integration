import argparse
import math
import os
import cv2
import numpy as np
from pathlib import Path


def read_frame_ts(filename):
    ts = []
    ts_tmp = 0
    with open(filename,'r') as f:
        for row in f.readlines():
            row=row.split('\n')[0].split(' ')[1]
            ts.append(float(row)/1000+ts_tmp)
    return ts


# log(I(x), t) = e^{-a*dt*s(x_k, t_{k-1})} + p      main equation
def direct_integrate(img, ts_frame, ts, xs, ys, ps):
    lg = cv2.log(img)
    a = 5
    for x,y,t,p in zip(xs,ys,ts,ps):
        p = 2*p - 1
        dt = t - ts_frame[x, y]
        ts_frame[x,y] = t
        lg[x, y] = math.exp(-a*dt*1e-3)*lg[x, y] + p
    img = cv2.exp(lg)
    return img, ts_frame


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='direct integrate')
    parser.add_argument('--width', default=346, type=int, help='image width')
    parser.add_argument('--height', default=260, type=int, help='image height')
    parser.add_argument('--duration', default=50, type=int, help='default time duration in ms. If `ts_file` not exist')
    parser.add_argument('--ts_file', default='data/data_ts.txt', type=str, help='path of the timestampe file')
    parser.add_argument('--event_file', default='data/data.txt', type=str, help='path of the data')
    args = parser.parse_args()
    
    assert(Path(args.event_file).exists())

    # first extract timestamp or using default.
    frame_ts = -1
    ts_from_file = False
    if(Path(args.ts_file).exists()):
        ts_from_file = True
        frame_ts = read_frame_ts(args.ts_file)
    else:
        print('TS file noe exist. Using default value: {:d} ms'.format(args.duration))


    # initial integration conditions
    inte_frame = np.ones((args.height, args.width), np.float) * 0.5 # init default value as 0.5
    ts_frame = np.zeros((args.height, args.width), np.float)        # init timestamp 

    with open(args.event_file, 'r') as f:
        current_ts = frame_ts[0] if ts_from_file else 0
        row = f.readline()
        ts, ys, xs, ps = [], [], [], []
        index = 0
        while(True):
            row = f.readline()
            if(not row):
                print('eof')
                os.abort()
            row = row.split(' ')            # split using ',' or ' '
            ts.append(float(row[0])/1000)
            ys.append(int(row[1]))
            xs.append(int(row[2]))
            ps.append(int(row[3][0]))       # using [0] to avoid '\n'
            if ts[-1] > current_ts:
                inte_frame, ts_frame = direct_integrate(inte_frame, ts_frame, ts, xs, ys, ps)
                index = index+1
                current_ts = frame_ts[index] if ts_from_file else index*args.duration
                ts, ys, xs, ps = [], [], [], []
                cv2.imshow('leaky-integrate', inte_frame)
                # save images
                cv2.imwrite('image/' + str(current_ts) + '.bmp', np.uint8(inte_frame*255))
                key = cv2.waitKey(10)
                if key == ord('q'):
                    print('abort!!!')
                    os.abort()

