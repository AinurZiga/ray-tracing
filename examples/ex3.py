""" Calculates mimo channel metrics for the whole map.
Only direct and single bounce reflected rays are considered
due to high computational complexity of double bounce reflections.
idx:
    2: channel rank with power 5%+ compared to strongest mode
    3: capacity open loop
    4: channel rank or number of mode used by the "water-filling"
    5: capacity closed loop ("water-filling" is used)
    6: siso channel H[0][0] capapcity
    7: Demmel condition number  """

import sys
import os
import operator
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from PySide2 import QtGui, QtCore, QtWidgets
import numpy as np

import rt
import functions
import viewer


def load_rates(cls, filename, idx):
    with open(filename, 'rb') as f:
        rates0 = np.load(f)
    #idx = 2  # 2...7 channels, rate, channels, rate, siso, demmel
    if idx < 2 or idx > 7:
        raise Exception("Wrong idx, must be from 2 to 7")
    rates = np.array(rates0[:, [0,1,idx]], dtype=np.float64)
    #print(rates[:10])
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

def mimo_rates(cls, ray_tracing, filename_out='./data/default.npy'):
    cls.draw_p(cls.p_BS)
    rates = []

    rates += rt.parmap(ray_tracing.mimo_rates_help, cls.analyse_points)
    rates = np.array(rates, dtype=np.float64)
    with open(filename_out, 'wb') as f:
        np.save(f, rates)
    idx = 5   #  5 -> closed loop capacity
    cls.rate_values = np.array(rates[:, [0,1, idx]], dtype=np.float64)
    cls.max_par = max(cls.rate_values, key = operator.itemgetter(2))
    cls.max_par = cls.max_par[2]
    cls.min_par = min(cls.rate_values, key = operator.itemgetter(2))
    cls.min_par = cls.min_par[2]
    cls.step_value = (cls.max_par - cls.min_par) / 8
    if cls.step_value == 0:
        cls.step_value = 1
    cls.legend.set_par(cls.min_par, cls.max_par, cls.step_value)
    cls.paint_map_rate()

def draw_walls(cls):
    cls.draw_walls()
    return

def init_rt(cls):
    cls.p_BS = [54.0, 35.0, 2.5]
    cls.draw_p(cls.p_BS)
    cls.fc = 5.6*10**9

    (n_walls, faces, segments, DRs, face_ps, 
            face_vs) = functions.walls_to_arrays(cls.walls_list)

    ray_tracing = rt.Ray_tracing(cls.p_BS, cls.walls_list, cls.materials,
            n_walls, faces, segments, 
            DRs, face_ps, face_vs, cls.fc,
            'image', 'rigorous')

    ray_tracing.is_single_bounce = True
    ray_tracing.is_double_bounce = False
    return ray_tracing


def main_fun(cls):
    cls.draw_walls()
    ray_tracing = init_rt(cls)
    mimo_rates(cls, ray_tracing, './data/res2.npy')

if __name__ == '__main__':
    print('file planner:', __name__)
    app = QtWidgets.QApplication(sys.argv)
    window = viewer.Window()
    window.show()
    filename_in = './maps/RTS1.map'
    window.center.graphicView.task1(filename_in)
    main_fun(window.center.graphicView)
    sys.exit(app.exec_())