# is_point_inside_figure

import sys, os
#sys.path.append("..")
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import rt
import functions
import numpy as np
import viewer as viewer
from PySide2 import QtGui, QtCore, QtWidgets

_, walls, materials = functions.open_file('./maps/RTS1.map')

n_walls, faces, segments, DRs, face_ps, face_vs = functions.walls_to_arrays(walls)

def foo(p1, p2, n_walls, faces, segments, 
            DRs=np.array([[]]), face_ps=np.array([[]]), face_vs=np.array([[]])):
    count1, count2 = 0, 0
    for i in range(n_walls):  # walls
        for j in range(faces[i+1]-faces[i]):  # faces
            ind = faces[i] + j
            DR = DRs[ind]
            D0 = (DR[0] * face_ps[segments[ind]][0] + DR[1] * face_ps[segments[ind]][1]
                    + DR[2] * face_ps[segments[ind]][2])
            tmp1 = D0 - DR[0] * p1[0] - DR[1] * p1[1] - DRs[ind][2] * p1[2]
            tmp2 = DR[0] * (p2[0] - p1[0]) + DR[1] *(p2[1] - p1[1]) + DR[2] * (p2[2] - p1[2])
            if tmp2 == 0:
                continue
            t0 = tmp1 / tmp2
            crossing_p = [0.0] * 3
            for k in range(3):
                crossing_p[k] = (p2[k] - p1[k]) * t0 + p1[k]
            if functions.skal(crossing_p, p1, p2) > 0:
                continue
            a = functions._is_point_inside_figure_mid(crossing_p, DR, 
                                face_ps[segments[ind]:segments[ind + 1], :], 
                                face_vs[segments[ind]:segments[ind + 1], :])
            b = functions._is_point_inside_figure_complex(crossing_p, DR,
                    face_ps[segments[ind]:segments[ind + 1], :])
            if segments[ind + 1] - segments[ind] == 4:
                c = functions._is_point_inside_figure_rect(crossing_p, DR, 
                                face_ps[segments[ind]:segments[ind + 1], :], 
                                face_vs[segments[ind]:segments[ind + 1], :])
                if not a == b == c:
                    count1 += 1
                    print(i, j, a, b, c)

            #print(i, j, a, b, -(segments[ind] - segments[ind + 1]))
            if a != b:
                print(i, j, a, b, segments[ind] - segments[ind + 1])
                count2 += 1
    print(count1, count2)
    return count1, count2



def foo1(p1, p2, n_walls, faces, segments, 
            DRs=np.array([[]]), face_ps=np.array([[]]), face_vs=np.array([[]])):
    count = 0
    i = 32
    #for j in range(faces[i+1]-faces[i]):  # faces
    j = 7
    ind = faces[i] + j
    DR = DRs[ind]
    D0 = (DR[0] * face_ps[segments[ind]][0] + DR[1] * face_ps[segments[ind]][1]
            + DR[2] * face_ps[segments[ind]][2])
    tmp1 = D0 - DR[0] * p1[0] - DR[1] * p1[1] - DRs[ind][2] * p1[2]
    tmp2 = DR[0] * (p2[0] - p1[0]) + DR[1] *(p2[1] - p1[1]) + DR[2] * (p2[2] - p1[2])
    if tmp2 == 0:
        return
    t0 = tmp1 / tmp2
    crossing_p = [0.0] * 3
    for k in range(3):
        crossing_p[k] = (p2[k] - p1[k]) * t0 + p1[k]
    if functions.skal(crossing_p, p1, p2) > 0:
        return
    print("crossing_p:", crossing_p)
    a = functions._is_point_inside_figure_mid(crossing_p, np.array(DR), 
                        face_ps[segments[ind]:segments[ind + 1], :], 
                        face_vs[segments[ind]:segments[ind + 1], :])
    b = functions._is_point_inside_figure_complex(crossing_p, np.array(DR), 
            face_ps[segments[ind]:segments[ind + 1], :])
    if segments[ind + 1] - segments[ind] == 4:
        c = functions._is_point_inside_figure_rect(crossing_p, np.array(DR), 
                        face_ps[segments[ind]:segments[ind + 1], :], 
                        face_vs[segments[ind]:segments[ind + 1], :])
        print(i, j, a, b, c)
    #print(i, j, a, b)
    return

def foo2(p1, p2, n_walls, faces, segments, 
            DRs=np.array([[]]), face_ps=np.array([[]]), face_vs=np.array([[]])):
    crossings = 0
    cr_points = []
    for i in range(n_walls):  # walls
        for j in range(faces[i+1]-faces[i]):  # faces
            ind = faces[i] + j
            DR = DRs[ind]
            D0 = (DR[0] * face_ps[segments[ind]][0] + DR[1] * face_ps[segments[ind]][1]
                    + DR[2] * face_ps[segments[ind]][2])
            tmp1 = D0 - DR[0] * p1[0] - DR[1] * p1[1] - DRs[ind][2] * p1[2]
            tmp2 = DR[0] * (p2[0] - p1[0]) + DR[1] *(p2[1] - p1[1]) + DR[2] * (p2[2] - p1[2])
            if tmp2 == 0:
                continue
            t0 = tmp1 / tmp2
            crossing_p = [0.0] * 3
            for k in range(3):
                crossing_p[k] = (p2[k] - p1[k]) * t0 + p1[k]
            if functions.skal(crossing_p, p1, p2) > 0:
                continue
            if functions.is_point_inside_figure(crossing_p, DR, 
                                face_ps[segments[ind]:segments[ind + 1], :], 
                                face_vs[segments[ind]:segments[ind + 1], :]):
                crossings += 1
                cr_points.append(crossing_p)
    print(crossings)
    return crossings, cr_points

import numba as nb

@nb.njit
def foo3(p1, p2, n_walls, faces, segments, 
            DRs=np.array([[]]), face_ps=np.array([[]]), face_vs=np.array([[]])):
    crossing_p = [0.0] * 3
    DR = [np.sqrt(1/3)] * 3
    ind = 0
    a = functions.is_point_inside_figure(crossing_p, DR, 
                                face_ps[segments[ind]:segments[ind + 1], :], 
                                face_vs[segments[ind]:segments[ind + 1], :])
    return a

p1 = [54.0, 35.0, 2.0]   # far
p2 = [59.0, 74.0, 1.0]


assert foo(p1, p2, n_walls, faces, segments, DRs, face_ps, face_vs) == (0, 0)
assert foo2(p1, p2, n_walls, faces, segments, DRs, face_ps, face_vs)[0] == 16

#foo3(p1, p2, n_walls, faces, segments, DRs, np.array(face_ps), np.array(face_vs)) 
# doesn't work

