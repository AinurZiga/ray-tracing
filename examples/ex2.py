""" Load file with calculated in ex3.py parameters.
Plots heat map of chosen parameters.
Parameters comprise capacity (open and closed loop),
channel rank (with conditions), Demmel condition number. 
idx:
    2: channel rank with power 5%+ compared to strongest mode
    3: capacity open loop
    4: channel rank or number of mode used by the "water-filling"
    5: capacity closed loop ("water-filling" is used)
    6: siso channel H[0][0] capapcity
    7: Demmel condition number """

import sys
import os
import operator
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from PySide2 import QtGui, QtCore, QtWidgets
import numpy as np

import rt
import functions
import viewer as viewer



def load_rates(cls, filename, idx):
    with open(filename, 'rb') as f:
        rates0 = np.load(f)
    #idx = 2  # 2...7 channels, rate, channels, rate, siso, demmel
    if idx < 2 or idx > 7:
        raise Exception("Wrong idx, must be from 2 to 7")
    rates = np.array(rates0[:, [0,1,idx]], dtype=np.float64)
    if idx == 7:
        limit = 2000
        idx_dem = np.where(rates[:, 2] > limit)  # for demmel (i = 7)
        rates[idx_dem, 2] = limit
        cls.max_par = 0
        cls.min_par = limit
    else:
        cls.max_par = max(rates, key = operator.itemgetter(2))
        cls.max_par = cls.max_par[2]
        cls.min_par = min(rates, key = operator.itemgetter(2))
        cls.min_par = cls.min_par[2]
    cls.step_value = (cls.max_par - cls.min_par) / 8
    if cls.step_value == 0:
        cls.step_value = 1
    cls.legend.set_par(cls.min_par, cls.max_par, cls.step_value)
    cls.rate_values = rates
    cls.paint_map_rate()
    p_BS = [54.0, 35.0, 2.5]
    cls.draw_p(p_BS)
    return

def draw_walls(cls):
    cls.draw_walls()
    return

def main_fun(cls):
        cls.draw_walls()
        load_rates(cls, './data/res1.npy', idx=5)

if __name__ == '__main__':
    print('file planner:', __name__)
    app = QtWidgets.QApplication(sys.argv)
    window = viewer.Window()
    window.show()
    filename_in = './maps/RTS1.map'
    window.center.graphicView.task1(filename_in)
    main_fun(window.center.graphicView)
    sys.exit(app.exec_())