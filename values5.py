#coding = utf-8

# NUMBA here

import struct
import ctypes
import numpy as np
import numba as nb
#from numba import njit

import warnings
warnings.filterwarnings("ignore")

#fun_wall = ctypes.CDLL('./crossing_wall.so')
#from numpy import ndarray
#import numpy as np


class M3DPOINT(ctypes.Structure):
     _fields_ = [("X", ctypes.c_double),
                 ("Y", ctypes.c_double),
                 ("H", ctypes.c_double)]

def bin_to_float(file):
    b = []
    for i2 in range(3):
        text = file.read(8)
        b.append(struct.unpack('<d', text)[0])
    return b


def bin_to_int(file, b = 8):
    N_str = ''
    for i in range(b):
        t = bin(ord(file.read(1)))
        t = t[2:]
        t = '0'*(8 - len(t)) + t
        N_str = str(t) + N_str
    return int(N_str, 2)

def float_to_bin(file, value):
    [d] = struct.unpack(">Q", struct.pack("<d", value))
    return '{:064b}'.format(d)

#def int_to_bin(value):
#    if value > 0:
#        tmp = f"{value:064b}"
#    else:
#        tmp = '1' + f"{-value:063b}"
#    return str(tmp)

def bin_to_string1(file):
    material = ''
    text = file.read(1)
    count = 0
    while text != b'x\00':
        if count > 20:
            print('error:', material)
            return
        count += 1
        material += text.decode("utf-8")
        text = file.read(1)
    return material

def bin_to_string(file):
    text = file.read(6)
    return text.decode("utf-8")

def open_file(filename):
    f = open(filename, 'rb')
    try:
        f.read(8)
        Zones = bin_to_int(f)
        points = []
        walls_list = []
        for i in range(Zones):
            f.read(24)
            Npoints = bin_to_int(file = f)
            for _ in range(Npoints):
                points.append(bin_to_float(f))
        Nfigures = bin_to_int(file = f)
        for i1 in range(Nfigures):
            #f.read(80)
            f.read(4*8)
            material = bin_to_string(f)
            #print(i1, material)
            f.read(298)
            faces = bin_to_int(f)
            #print('faces:', faces, k)
            if faces < 1 and faces > 20:
                return 0, 0
            edge_list = []
            for i2 in range(faces):
                segments = []
                try:
                    DR = bin_to_float(f)
                except:
                    return points, walls_list
                plane_points = bin_to_int(f)
                #print('DR:', DR)
                try:
                    for _ in range(2*plane_points):
                        segments.append(bin_to_float(f))
                except:
                    return points, walls_list
                edge_list.append([DR, segments])
            walls_list.append(edge_list)
            #print(edge_list)
    finally:
        f.close()
        print(len(walls_list))
    return points, walls_list
#points, walls_list = open_file("RTS1.map")
#for k in range(100, 300):
#    try:
#        points, walls_list = open_file("RTS1.map", k)
#    except:
#       pass
#points, walls_list = open_file("City4X10_8_2_3D.map")
#print(len(walls_list))

def walls_to_arrays(walls):
    faces = [0]
    segments = [0]
    DRs = []
    face_ps = []
    face_vs = []
    for i in range(len(walls)):
        for j in range(len(walls[i])):
            face = walls[i][j]
            DRs.append(face[0])
            for k in range(len(face[1])//2):
                face_ps.append(face[1][2*k])
                face_vs.append(face[1][2*k+1])
            segments.append(segments[-1] + len(face[1])//2)
        faces.append(faces[-1] + j)
    return len(walls), faces, segments, DRs, np.array(face_ps), np.array(face_vs)


@nb.njit(cache=True)
def check(A, b):
    a = np.empty(A.shape[1], dtype=np.bool_)
    rows = A.shape[0]
    for r in range(rows):
        a = A[r] == b
        if a.all():
            return True 
    return False

@nb.njit(cache=True)
def crossing_wall(p1, p2, n_walls, faces, segments, 
            DRs=np.array([[]]), face_ps=np.array([[]]), face_vs=np.array([[]])):
    cr_walls = 0
    #pool_cr_points = np.array([])
    #pool_cr_points = None
    for i in range(n_walls):  # walls
        first_interaction = False
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
            if skal(crossing_p, p1, p2) > 0:
                continue
            if is_point_inside_figure(crossing_p, DR, 
                                face_ps[segments[ind]:segments[ind + 1], :], 
                                face_vs[segments[ind]:segments[ind + 1], :]):
                #if is_pr:
                #    print('crossing point:', crossing_p)
                #crossing_p = np.array(crossing_p)
                if not cr_walls:
                    #pool = np.array(crossing_p, dtype=np.float64)
                    pool = np.zeros((2, 3))
                    pool[0,:] = np.array(crossing_p)
                    pool[1,:] = np.array(crossing_p)
                    #pool = np.vstack((np.array(crossing_p), np.array(crossing_p)))
                    cr_walls += 1
                    break
                    #if not first_interaction:
                    #    first_interaction = True
                    #else:
                    #    cr_walls += 1
                    #    break
                elif not check(pool, np.array(crossing_p)):
                    #old_pool = np.array(pool, dtype=np.float64)
                    old_pool = pool[:, :]
                    pool = np.empty((old_pool.shape[0] + 1, old_pool.shape[1]))
                    pool[:-1, :] = old_pool
                    pool[-1,:] = np.array(crossing_p)
                    #print(crossing_p)
                    #pool = np.vstack((pool, np.array(crossing_p)))
                    cr_walls += 1
                    break
                    #if not first_interaction:
                    #    first_interaction = True
                    #else:
                    #    cr_walls += 1
                    #    break
                
                #if pool_cr_points and crossing_p not in pool_cr_points:
                #    if not pool_cr_points:
                #        pool_cr_points = np.array(crossing_p)
                #    else:
                #        pool_cr_points = np.vstack((pool_cr_points, np.array(crossing_p)))
                #    cr_walls += 1
    return cr_walls

@nb.njit(cache=True)
def d_crossing_wall(p1, p2, n_walls, faces, segments, 
            DRs=np.array([[]]), face_ps=np.array([[]]), face_vs=np.array([[]])):
    cr_walls = 0
    #faces_d = []
    #faces_theta = []
    pool = np.zeros((2, 3))
    faces_d = nb.typed.List.empty_list(nb.float64)
    faces_theta = nb.typed.List.empty_list(nb.float64)
    for i in range(n_walls):  # walls
        cr_p1 = [0.0] * 3
        cr_p2 = [0.0] * 3
        for j in range(faces[i+1]-faces[i]):  # faces
            #cr_p1 = [0.0] * 3
            #cr_p2 = [0.0] * 3
            #cr_p2 = np.zeros(3)
            #face_crossings = np.zeros((2, 3))
            #face_crossings = []
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
            if skal(crossing_p, p1, p2) > 0:
                continue
            if is_point_inside_figure(crossing_p, DR, 
                                face_ps[segments[ind]:segments[ind + 1], :], 
                                face_vs[segments[ind]:segments[ind + 1], :]):
                #if not cr_walls:
                #    pool = np.zeros((2, 3))
                #    pool[0,:] = np.array(crossing_p)
                #    pool[1,:] = np.array(crossing_p)
                    #pool = np.vstack((np.array(crossing_p), np.array(crossing_p)))
                    #cr_p1 = np.array(crossing_p)
                #    cr_p1 = list(crossing_p)
                #    print("Yes cr_p1:", cr_p1)
                #    cr_walls += 1
                if not check(pool, np.array(crossing_p)):
                    old_pool = pool[:, :]
                    pool = np.empty((old_pool.shape[0] + 1, old_pool.shape[1]))
                    pool[:-1, :] = old_pool
                    pool[-1,:] = np.array(crossing_p)
                    if cr_p1 != [0.0]*3:
                        #cr_p2 = np.array(crossing_p)
                        cr_p2 = list(crossing_p)
                        #print("Yes cr_p2:", cr_p2)
                        tmp = vec_len(cr_p1, cr_p2)
                        if tmp > 1.0:
                            tmp = 1.0
                        faces_d.append(tmp)
                        cr_p1 = [p1[i] - crossing_p[i] for i in range(3)]
                        theta = np.arccos(skal_mul(cr_p1, DR) / vec_len(p1, crossing_p))
                        if theta > np.pi/2:
                            theta = np.pi - theta
                        faces_theta.append(theta)
                        cr_p1 = [0.0]*3
                        break
                        #cr_p1 = [0.0]*3
                    else:
                        cr_p1 = list(crossing_p)
                        #print("Yes cr_p1:", cr_p1)
                        cr_walls += 1
                    #face_crossings.append()
                    #cr_walls += 1
        if cr_p1 != [0.0]*3:
            faces_d.append(0.15)
            faces_theta.append(45/57.3)
    res = np.zeros((2, len(faces_d)), dtype=nb.float64) #TODO
    for i in range(len(faces_d)):
        res[0, i] = faces_d[i]
        res[1, i] = faces_theta[i]
    #res[0, :] = np.array(faces_d)
    #res[1, :] = np.array(faces_theta)
    #res[0, :] = faces_d
    #res[1, :] = faces_theta
    return res

#@nb.njit
def is_crossing_wall(p1, p2, walls):
    cr_walls = 0
    #print('len walls: ', len(walls))
    for i in range(len(walls)):
        for j in range(len(walls[i])):
            face = walls[i][j]
            DR = face[0]
            #print(i)
            #print('DR:', DR)
            #print('face:', face[1], len(face[1]))
            D0 = (DR[0] * face[1][0][0] + DR[1] * face[1][0][1]
                    + DR[2] * face[1][0][2])
            tmp1 = D0 - DR[0] * p1[0] - DR[1] * p1[1] - DR[2] * p1[2]
            tmp2 = DR[0] * (p2[0] - p1[0]) + DR[1] *(p2[1] - p1[1]) + DR[2] * (p2[2] - p1[2])
            if tmp2 == 0:
                continue
            t0 = tmp1 / tmp2
            crossing_p = [0.0] * 3
            for k in range(3):
                crossing_p[k] = (p2[k] - p1[k]) * t0 + p1[k]
            if skal(crossing_p, p1, p2) > 0:
                continue
            face_p, face_v = [], []
            for i in range(len(face[1])//2):
                face_p.append(face[1][2*i])
                face_v.append(face[1][2*i+1])
            if is_point_inside_figure(crossing_p, np.array(face[0]), np.array(face_p), np.array(face_v)):
                #print('crossing point:', crossing_p)
                return True
    return False
    

@nb.njit(cache=True)
def is_point_inside_figure(p, DR, face_p=np.array([[]]), face_v=np.array([[]])):
    #DR = face[0]
    #vc = np.zeros(face_p.shape[0]//2)
    vc = []
    for v in range(face_p.shape[0]):
        #AB = face_p[1+2*v]    # vector
        AB = face_v[v]
        #AM = [p[k] - face[1][2*v][k] for k in range(3)]
        #AM = np.zeros(3)
        AM = [0.0]*3
        #AM = np.array(p - face_p[2*v])
        for k in range(3):
            tmp = face_p[v]
            AM[k] = p[k] - tmp[k]
        vc.append(vect_mul(AB, AM, DR))
    if case_more(vc):
        return True
    if case_less(vc):
        return True
    return False
    

@nb.njit(cache=True)
def skal(crossing_p, p1, p2):
    #return (p1 - crossing_p) * (p2 - crossing_p)
    sum = 0.0
    for k in range(3):
        sum += (p1[k] - crossing_p[k]) * (p2[k] - crossing_p[k])
    return sum

@nb.njit(cache=True)
def vect_mul(AB, AM, DR):
    vc1 = [0.0] * 3
    vc1[0] = (AB[1] * AM[2] - AM[1] * AB[2]) * DR[0]
    vc1[1] = (AB[0] * AM[2] - AM[0] * AB[2]) * DR[1]
    vc1[2] = (AB[0] * AM[1] - AM[0] * AB[1]) * DR[2]
    return vc1[0] + vc1[1] + vc1[2]

@nb.njit(cache=True)
def case_more(vect):
    #return (vect >= 0).all()
    for x in vect:
        if x <= 0.0:
            return False
    return True

@nb.njit(cache=True)
def case_less(vect):
    #return (vect <= 0).all()
    for x in vect:
        if x >= 0.0:
            return False
    return True

@nb.njit(cache=True)
def skal_mul(vec1, vec2):
    sum = 0.0
    for i in range(3):
        sum += vec1[i]*vec2[i]
    return sum

@nb.njit(cache=True)
def vec_len(p1, p2):
    s = 0.0
    for i in range(3):
        s += (p1[i] - p2[i])**2
    return np.sqrt(s)

#@nb.njit
def case1(p1, p2, walls, n_walls, faces, segments, DRs: np.array([[]]),
            face_ps: np.array([[]]), face_vs: np.array([[]])):
    """ Calculating reflected rays """
    cr_points = []
    cf_faces = []
    d_faces = []
    count = 0

    los_crossings = crossing_wall(p1, p2, n_walls, faces, segments, np.array(DRs),
            np.array(face_ps), np.array(face_vs))
    for i in range(len(walls)):
        for j in range(len(walls[i])):
            # Проверим, находяться ли точки p1 и p2 по одну сторону от плоскости
            # подставим их в уравнение плоскости
            face = walls[i][j]
            #print(face); return
            DR = face[0]
            D = -(DR[0]*face[1][0][0] + DR[1]*face[1][0][1] + DR[2]*face[1][0][2])
            a1 = DR[0]*p1[0] + DR[1]*p1[1] + DR[2]*p1[2] + D  # len of normal add-ly
            a2 = DR[0]*p2[0] + DR[1]*p2[1] + DR[2]*p2[2] + D
            if not ((a1 < 0 and a2 < 0) or (a1 > 0 and a2 > 0)):
                #print(a1, a2, face)
                continue # exit
            else:
                A = [p1[k] - a1*DR[k] for k in range(3)]
                B = [p2[k] - a2*DR[k] for k in range(3)]
                k = a2 / a1
                #C = [max(A[i], B[i]) - min(A[i], B[i])/k + ]
                #C = [(A[i] - B[i])/(k+1) + B[i] for i in range(3)]
                C = [(A[i] - B[i])*k/(k+1) + B[i] for i in range(3)]
                # проверить, лежит ли точка С внутри грани
                #print('Check ray', C, A, B, k)
                face_p, face_v = [], []
                for k in range(len(face[1])//2):
                    face_p.append(face[1][2*k])
                    face_v.append(face[1][2*k+1])
                if not is_point_inside_figure(C, np.array(face[0]), np.array(face_p), np.array(face_v)):
                    continue
                #if i == 20 and j == 7:
                #    print("YES")
                impinging = [C[i] - p1[i] for i in range(3)]  # падающий луч
                if skal_mul(impinging, DR) >= 0:
                    continue
                #is_los1, is_los2 = True, True
                #is_los1 = crossing_wall(p1, C, walls) <= 1
                #is_los2 = crossing_wall(p2, C, walls) <= 1
                C1 = [C[i] - (C[i] - p1[i])*0.001 for i in range(3)]
                C2 = [C[i] - (C[i] - p2[i])*0.001 for i in range(3)]
                los1 = crossing_wall(p1, C1, n_walls, faces, segments, np.array(DRs), 
                        np.array(face_ps), np.array(face_vs))
                los2 = crossing_wall(p2, C2, n_walls, faces, segments, np.array(DRs), 
                        np.array(face_ps), np.array(face_vs))
                #if is_los1 and is_los2:
                if (los1 + los2 <= los_crossings+1) and (C not in cr_points):
                    #is_point_inside_figure(C, face, True)
                    #print("cross:", C, los1, los2)
                    #print("is_cross:", i, j)
                    cf_faces.append(face)
                    cr_points.append(C)
                    #print(walls[i][2][1][1])
                    #d = vec_len(walls[i][0][1][1], [0.0, 0.0, 0.0])
                    d = 0.2   # TODO
                    #print("d:", walls[i][0][1])
                    d_faces.append(d)
                    count += 1
    C = floor_reflect(p1, p2, n_walls, faces, segments, los_crossings, np.array(DRs),
                np.array(face_ps), np.array(face_vs))
    if C and (C not in cr_points):
        cr_points.append(C)
        d_faces.append(0.3)
    C = ceil_reflect(p1, p2, n_walls, faces, segments, los_crossings, np.array(DRs),
                np.array(face_ps), np.array(face_vs))
    if C and (C not in cr_points):
        cr_points.append(C)
        d_faces.append(0.3)
    #print("cr_points:", len(cr_points), cr_points)
    return cr_points, cf_faces, d_faces

def floor_reflect(p1, p2, n_walls, faces, segments, los_crossings,
                DRs: np.array([[]]), face_ps: np.array([[]]), face_vs: np.array([[]])):
    k = p2[2] / p1[2]
    C = [0.0]*3
    C[0] = p1[0] + (p2[0] - p1[0])/(k + 1)
    C[1] = p1[1] + (p2[1] - p1[1])/(k + 1)
    C1 = [C[i] - (C[i] - p1[i])*0.001 for i in range(3)]
    C2 = [C[i] - (C[i] - p2[i])*0.001 for i in range(3)]
    los1 = crossing_wall(p1, C1, n_walls, faces, segments, np.array(DRs), 
            np.array(face_ps), np.array(face_vs))
    los2 = crossing_wall(p2, C2, n_walls, faces, segments, np.array(DRs), 
            np.array(face_ps), np.array(face_vs))
    if los1 + los2 <= los_crossings+1:
        return C
    return None

def ceil_reflect(p1, p2, n_walls, faces, segments, los_crossings,
                DRs: np.array([[]]), face_ps: np.array([[]]), face_vs: np.array([[]])):
    k = p2[2] / p1[2]
    C = [0.0]*3
    C[2] = 3.0
    C[0] = p1[0] + (p2[0] - p1[0])/(k + 1)
    C[1] = p1[1] + (p2[1] - p1[1])/(k + 1)
    C1 = [C[i] - (C[i] - p1[i])*0.001 for i in range(3)]
    C2 = [C[i] - (C[i] - p2[i])*0.001 for i in range(3)]
    los1 = crossing_wall(p1, C1, n_walls, faces, segments, np.array(DRs), 
            np.array(face_ps), np.array(face_vs))
    los2 = crossing_wall(p2, C2, n_walls, faces, segments, np.array(DRs), 
            np.array(face_ps), np.array(face_vs))
    if los1 + los2 <= los_crossings+1:
        return C
    return None


#@njit  # for rigorous
def calc_amplitudes(p1, p2, cr_points, cr_faces, d_faces, walls, n_walls, 
                        faces, segments, DRs, face_ps, face_vs, fc):
    #fc = 5.6*10**9
    c = 3*10**8
    lamda = c / fc
    k = 2*3.14 / lamda
    eta_brick = 3.75 - 1j * (17.98 * 0.038 / 5.6)
    eta_wood = 1.99 - 1j * (17.98 * 0.0047 * 5.6**1.0718 / 5.6)
    #Ampl = 2*lamda / (4*np.pi)  # + antenna gain
    Ampl = 2  # + antenna gain
    #eta = eta_brick



    D_direct = vec_len(p1, p2)
    ray0 = Ampl * np.exp(-2j*np.pi*fc*D_direct/c) / D_direct
    faces_d_theta = d_crossing_wall(p1, p2, n_walls, faces, segments, np.array(DRs), 
                        np.array(face_ps), np.array(face_vs))
    for i in range(faces_d_theta.shape[1]):
        face_d = faces_d_theta[0, i]
        face_theta = faces_d_theta[1, i]
        #eta = 3.75 - 1j * (17.98 * 0.038 / 5.6)   # brick
        eta = eta_brick
        q = 6.28*face_d/lamda * np.sqrt(eta - np.sin(face_theta)**2)
        tmp1 = np.cos(face_theta) - np.sqrt(face_theta - np.sin(face_theta)**2)
        tmp2 = np.cos(face_theta) + np.sqrt(face_theta - np.sin(face_theta)**2)
        R_prime = tmp1 / tmp2
        tmp2 = 1 - R_prime**2 * np.exp(-2j*q)
        tmp3 = (1 - R_prime**2)*(np.exp(-1j*q))
        T = tmp3 / tmp2
        ray0 = ray0 * T
    rays = ray0

    for i, point in enumerate(cr_points):
        d = d_faces[i]
        tmp1 = sum([(p1[i] - point[i])*(p2[i] - point[i]) for i in range(3)])
        tmp2 = vec_len(p1, point) * vec_len(p2, point)
        theta = np.arccos(tmp1 / tmp2) /2
        if i < len(cr_points)-2:
            # vertical, TE, brick
            eta = eta_brick
            q = 6.28*d/lamda * np.sqrt(eta - np.sin(theta)**2)
            tmp1 = np.cos(theta) - np.sqrt(theta - np.sin(theta)**2)
            tmp2 = np.cos(theta) + np.sqrt(theta - np.sin(theta)**2)
            R_prime = tmp1 / tmp2
        else:
            eta = eta_wood
            q = 6.28*d/lamda * np.sqrt(eta - np.sin(theta)**2)
            tmp1 = eta*np.cos(theta) - np.sqrt(theta - np.sin(theta)**2)
            tmp2 = eta*np.cos(theta) + np.sqrt(theta - np.sin(theta)**2)
            R_prime = tmp1 / tmp2
        tmp1 = R_prime*(1-np.exp(-2j*q))
        tmp2 = 1 - R_prime**2 * np.exp(-2j*q)
        R = tmp1 / tmp2
        D = vec_len(p1, point) + vec_len(p2, point)
        tau = D / c
        ray = Ampl * R * np.exp(-2j*np.pi*fc*tau) / D
        C1 = [point[j] - (point[j] - p1[j])*0.001 for j in range(3)]
        C2 = [point[j] - (point[j] - p2[j])*0.001 for j in range(3)]
        faces_d_theta1 = d_crossing_wall(p1, C1, n_walls, faces, segments, np.array(DRs), 
                        np.array(face_ps), np.array(face_vs))
        faces_d_theta2 = d_crossing_wall(p2, C2, n_walls, faces, segments, np.array(DRs), 
                        np.array(face_ps), np.array(face_vs))
        faces_d_theta = np.hstack((faces_d_theta1, faces_d_theta2))
        for i in range(faces_d_theta.shape[1]):  # crossings through wall
            #eta = 3.75 - 1j * (17.98 * 0.038 / 5.6)   # brick
            eta = eta_brick
            face_d = faces_d_theta[0, i]
            face_theta = faces_d_theta[1, i]
            q = 6.28*face_d/lamda * np.sqrt(eta - np.sin(face_theta)**2)
            tmp1 = np.cos(face_theta) - np.sqrt(face_theta - np.sin(face_theta)**2)
            tmp2 = np.cos(face_theta) + np.sqrt(face_theta - np.sin(face_theta)**2)
            R_prime = tmp1 / tmp2
            tmp2 = 1 - R_prime**2 * np.exp(-2j*q)
            tmp3 = (1 - R_prime**2)*(np.exp(-1j*q))
            T = tmp3 / tmp2
            ray = ray * T        
        rays += ray
    return rays

#@njit
def ray_tracing(point1, point2, walls, n_walls, faces, segments, DRs, face_ps, face_vs):
    cr_points, cr_faces, d_faces = case1(point1, point2, walls,
            n_walls, faces, segments, DRs, face_ps, face_vs)
    return cr_points, cr_faces, d_faces

def azimuth_old(p1, p2):
    p1 = list(p1)
    p2 = list(p2)
    p1[2] = 0.0
    p2[2] = 0.0
    p_help = list(p1)
    p_help[0] += 1.0
    d1 = vec_len(p1, p2)
    d2 = 1.0
    d3 = vec_len(p_help, p2)
    a = np.arccos((d2**2 + d1**2 - d3**2) / (2*d2*d1))
    k = (p_help[0] - p1[0]) / (p_help[1] - p1[1])
    #p1 = p_help - p1
    #p2 = p2 - p1
    if (p_help[0] - p1[0])*(p2[1] - p1[1]) - (p_help[1] - p1[1])*(p2[0] - p1[0]) < 0:
        a = -a
    return 180*a/np.pi


def azimuth(p1, p2):
    #d2 = p2[1] - p1[1]
    #d = vec_len(p1, p2)
    #return np.arcsin(d2/d)*57.3
    p1 = list(p1)
    p2 = list(p2)
    p1[2] = 0.0
    p2[2] = 0.0
    p_help = list(p1)
    p_help[0] += 1.0
    tmp1 = skal(p1, p_help, p2)
    tmp2 = vec_len(p1, p_help) * vec_len(p2, p1)
    if tmp2 == 0:
        return 0
    #print(tmp1/tmp2)
    res = np.arccos(tmp1 / tmp2)*57.3
    if p2[1] < p1[1]:
        res = -res
    return res

def zenith(p1, p2):
    h = p2[2] - p1[2]
    d = vec_len(p1, p2)
    if d == 0:
        return 90
    return 90 - np.arcsin(h/d)*57.3
    #p_help = list(p1)
    #p_help[2] += 1.0
    #tmp1 = skal(p1, p_help, p2)
    #tmp2 = vec_len(p1, p_help) * vec_len(p2, p1)
    #return np.arccos(tmp1 / tmp2)*57.3

def step_3(p1, p2, cr_points, cr_faces, d_faces, walls, n_walls, 
                        faces, segments, DRs, face_ps, face_vs, fc):
    """Принимает точки отражения, добавить прямой луч.
    Сгенерировать 2-мерный массив 4 угла, задержка, 
    мощность"""
    #fc = 5.6*10**9
    c = 3*10**8
    lamda = c / fc
    #k = 2*3.14 / lamda
    eta_brick = 3.75 - 1j * (17.98 * 0.038 / 5.6)
    eta_wood = 1.99 - 1j * (17.98 * 0.0047 * 5.6**1.0718 / 5.6)
    #P_tx = 10**(19/10)  # 19 dBm to mWt
    #losses = 7  # times for each crossing 
    #Ampl = 2*lamda / (4*np.pi)
    Ampl = 2
    det_clusters = np.zeros((len(cr_points) + 1, 6), dtype=np.float64)

    for i in range(len(cr_points) + 1):
        if i == 0:   # direct ray
            #is_los = float(is_crossing_wall(p1, p2, walls))
            dist_direct = vec_len(p1, p2)
            tau0 = dist_direct / (3*10**2)  # microsecond
            #tau0 = 0
            #ray0 = P0 / dist_direct
            #ray0 = np.exp(-2j*np.pi*fc*tau0) / dist_direct
            crossings = crossing_wall(p1, p2, n_walls, faces, segments, np.array(DRs), 
                            np.array(face_ps), np.array(face_vs))
            if crossings:
                is_los = 0
            else:
                is_los = 1
            #P0 = (Ampl / dist_direct)**2
            ray0 = Ampl * np.exp(-2j*np.pi*fc*dist_direct/c) / dist_direct
            faces_d_theta = d_crossing_wall(p1, p2, n_walls, faces, segments, np.array(DRs), 
                        np.array(face_ps), np.array(face_vs))
            for j in range(faces_d_theta.shape[1]):
                face_d = faces_d_theta[0, j]
                face_theta = faces_d_theta[1, j]
                eta = 3.75 - 1j * (17.98 * 0.038 / 5.6)   # brick
                q = 6.28*face_d/lamda * np.sqrt(eta - np.sin(face_theta)**2)
                tmp1 = np.cos(face_theta) - np.sqrt(face_theta - np.sin(face_theta)**2)
                tmp2 = np.cos(face_theta) + np.sqrt(face_theta - np.sin(face_theta)**2)
                R_prime = tmp1 / tmp2
                tmp2 = 1 - R_prime**2 * np.exp(-2j*q)
                tmp3 = (1 - R_prime**2)*(np.exp(-1j*q))
                T = tmp3 / tmp2
                #P0 = P0 * np.abs(T)
                ray0 = ray0 * T
            print("shape:",faces_d_theta.shape)
            #P0 = P0 / losses**crossings
            #print("ray0:", np.log10(np.abs(ray0)), faces_d_theta.shape, crossings)
            #print("faces_d_theta:", faces_d_theta)
            P0  = np.abs(ray0)**2
            AOA = azimuth(p2, p1)  # Tx -> Rx for departure
            ZOA = zenith(p2, p1)
            AOD = azimuth(p1, p2)
            ZOD = zenith(p1, p2)
            #print("angles:", AOA, ZOA, AOD, ZOD)
            cluster = np.array([AOA, ZOA, AOD, ZOD, tau0, P0])
            det_clusters[i, :] = cluster
        else:
            p = cr_points[i-1]
            dist = vec_len(p1, p) + vec_len(p, p2)
            tau = dist / (3*10**2)   # microsec
            d = d_faces[i-1]
            tmp1 = skal(p, p1, p2)
            tmp2 = vec_len(p1, p) * vec_len(p2, p)
            theta = np.arccos(tmp1 / tmp2) / 2
            #if cr_faces[i-1][0][2] > 0.707:
            if i < len(cr_points)-1:
                # vertical, TE, brick
                eta = eta_brick
                q = 6.28*d/lamda * np.sqrt(eta - np.sin(theta)**2)
                tmp1 = np.cos(theta) - np.sqrt(theta - np.sin(theta)**2)
                tmp2 = np.cos(theta) + np.sqrt(theta - np.sin(theta)**2)
                R_prime = tmp1 / tmp2
            else:
                eta = eta_wood
                q = 6.28*d/lamda * np.sqrt(eta - np.sin(theta)**2)
                tmp1 = eta*np.cos(theta) - np.sqrt(theta - np.sin(theta)**2)
                tmp2 = eta*np.cos(theta) + np.sqrt(theta - np.sin(theta)**2)
                R_prime = tmp1 / tmp2
            tmp1 = R_prime*(1-np.exp(-2j*q))
            tmp2 = 1 - R_prime**2 * np.exp(-2j*q)
            R = tmp1 / tmp2
            #P = (np.abs(Ampl * R) / dist)**2
            ray = Ampl * R * np.exp(-2j*np.pi*fc*dist/c) / dist
            #ray = np.abs(Ampl * R) / dist
            C1 = [p[j] - (p[j] - p1[j])*0.001 for j in range(3)] # TODO
            C2 = [p[j] - (p[j] - p2[j])*0.001 for j in range(3)] # TODO
            faces_d_theta1 = d_crossing_wall(p1, C1, n_walls, faces, segments, np.array(DRs), 
                        np.array(face_ps), np.array(face_vs))
            faces_d_theta2 = d_crossing_wall(p2, C2, n_walls, faces, segments, np.array(DRs), 
                            np.array(face_ps), np.array(face_vs))
            faces_d_theta = np.hstack((faces_d_theta1, faces_d_theta2))
            for j in range(faces_d_theta.shape[1]):
                #eta = 3.75 - 1j * (17.98 * 0.038 / 5.6)   # brick
                eta = eta_brick
                face_d = faces_d_theta[0, j]
                face_theta = faces_d_theta[1, j]
                q = 6.28*face_d/lamda * np.sqrt(eta - np.sin(face_theta)**2)
                tmp1 = np.cos(face_theta) - np.sqrt(face_theta - np.sin(face_theta)**2)
                tmp2 = np.cos(face_theta) + np.sqrt(face_theta - np.sin(face_theta)**2)
                R_prime = tmp1 / tmp2
                tmp2 = 1 - R_prime**2 * np.exp(-2j*q)
                tmp3 = (1 - R_prime**2)*(np.exp(-1j*q))
                T = tmp3 / tmp2
                #P = P * np.abs(T)
                ray = ray * T
            P = np.abs(ray)**2
            AOA = azimuth(p2, p) # first receiver
            ZOA = zenith(p2, p)
            AOD = azimuth(p1, p)  # first transmitter
            ZOD = zenith(p1, p)
            cluster = np.array([AOA, ZOA, AOD, ZOD, tau, P])
            det_clusters[i, :] = cluster
    return generate_subrays(p1, p2, det_clusters, is_los, fc)

def generate_subrays(p1, p2, det_clusters, is_los, fc):
    """Сгенерировать 2-мерный массив с подлучами: 4 угла, 
    мощность, фаза"""
    M = 20
    N = det_clusters.shape[0]
    alpha_m = [0.0447, 0.1413, 0.2492, 0.3715, 0.5129, 0.6797, 0.8844,
                1.1481, 1.5195, 2.1551]
    rays = np.zeros(((N-is_los), M, 6), dtype=np.float64)
    los_ray = np.zeros(6, dtype=np.float64)
    if is_los:
        los_ray[:4] = np.array(det_clusters[0,:4]) # add alpha_m?
        los_ray[4] = det_clusters[0, 5]
        los_ray[5] = -2*np.pi*fc * det_clusters[0, 4]/10**6  # phi_0
    for n in range(is_los, N, 1):
        for m in range(M):
            i = n - is_los
            ch = np.random.choice(alpha_m, 4)
            AOA_nm = det_clusters[n, 0] + c_asa(is_los)*(2*(np.random.random() > 0.5) - 1)*ch[0]
            AOD_nm = det_clusters[n, 2] + c_asd(is_los)*(2*(np.random.random() > 0.5) - 1)*ch[1]
            ZOA_nm = det_clusters[n, 1] + c_zsa(is_los)*(2*(np.random.random() > 0.5) - 1)*ch[2]
            if ZOA_nm >= 180 and ZOA_nm <= 360:
                ZOA_nm = 360 - ZOA_nm
            ZOD_nm = det_clusters[n, 3] + mu_lg_ZSD(is_los, fc/10**6)*(2*(np.random.random() > 0.5) - 1)*ch[3]
            #TODO random coupling
            P_nm = det_clusters[n, 5] / M
            #xpr_nm = np.random.randn() * 4 + 10
            phi_nm = (2*np.random.random()-1)*180
            rays[i, m, :] = np.array([AOA_nm, ZOA_nm, AOD_nm, ZOD_nm, P_nm, phi_nm])
    return generate_channel(p1, p2, rays, los_ray, fc)

def generate_channel(p1, p2, rays, los_ray, fc):
    H = np.zeros((3, 3), dtype=np.complex128)
    for i in range(3):
        for j in range(3):
            H[i, j] = single_channel(p1, p2, rays, los_ray, i-1, j-1, fc)
    return H


def single_channel(p1, p2, rays, los_ray, i, j, fc):
    #fc = 5.6*10**9
    #c = 3*10**8
    #shift = 82/1000
    #i, j = -1, -1
    h = 0.0 + 0.0j
    for n in range(rays.shape[0]):
        for m in range(rays.shape[1]):
            h += add_ray(p1, p2, rays[n, m], i, j, fc)
    h += add_ray(p1, p2, los_ray, i, j, fc)
    return h

def add_ray(p1, p2, ray, i, j, fc):
    #fc = 5.6*10**9
    c = 3*10**8
    shift = 82/1000
    AOA_nm, ZOA_nm, AOD_nm, ZOD_nm, P_nm, phi_nm = ray
    r_rx_nm = np.zeros(3)
    r_rx_nm[0] = np.sin(ZOA_nm/57.3) * np.cos(AOA_nm/57.3)
    r_rx_nm[1] = np.sin(ZOA_nm/57.3) * np.sin(AOA_nm/57.3)
    r_rx_nm[2] = np.cos(ZOA_nm/57.3)
    r_tx_nm = np.zeros(3)
    r_tx_nm[0] = np.sin(ZOD_nm/57.3) * np.cos(AOD_nm/57.3)
    r_tx_nm[1] = np.sin(ZOD_nm/57.3) * np.sin(AOD_nm/57.3)
    r_tx_nm[2] = np.cos(ZOD_nm/57.3)
    #d_rx = np.array([shift*i, 0, 0])
    d_tx = np.array([shift*j, 0, 0])
    d_rx = np.array(p2) - np.array(p1)
    d_rx[0] += shift*i
    h = (np.exp(1j*2*np.pi*fc/c * (r_rx_nm @ d_rx + r_tx_nm @ d_tx)) * 
                np.exp(1j*phi_nm/57.3) * np.sqrt(P_nm))
    return h

def generate_random_clusters():
    pass

def c_asa(is_los):
    """Return in degrees"""
    if is_los:
        return 8
    return 11

def c_asd(is_los):
    if is_los:
        return 5
    return 5

def c_zsa(is_los):
    if is_los:
        return 9
    return 9

def mu_lg_ZSD(is_los, fc):
    """fc in GHz"""
    if is_los:
        return -1.43*np.log10(1+fc) + 2.228
    return 1.08
    

def mimo_channel_matrix(p1, p2, walls, 
                        n_walls, faces, segments, DRs, face_ps, face_vs, fc):
    # вернуть полную канальную матрицу
    #global p1, p2
    #shift = 82/1000
    #H = [[0 for i in range(3)] for j in range(3)]
    cr_points, cr_faces, d_faces = ray_tracing(p1, p2, walls, 
                                n_walls, faces, segments, DRs, face_ps, face_vs)
    #print(len(cr_points), cr_points)
    print("crossings:", len(cr_points))
    H = step_3(p1, p2, cr_points, cr_faces, d_faces, walls, n_walls, 
                        faces, segments, DRs, face_ps, face_vs, fc)
    return H

def mimo_channel_matrix_rig(p1, p2, walls, 
                        n_walls, faces, segments, DRs, face_ps, face_vs, fc):
    shift = 82/1000
    H = np.zeros((3,3), dtype=np.complex128)
    for i in range(3):
        for j in range(3):
            p1_ij = list(p1)
            p1_ij[0] += shift * (i - 1)
            p2_ij = list(p2)
            p2_ij[0] += shift * (j - 1)
            cr_points, cr_faces, d_faces = ray_tracing(p1_ij, p2_ij, walls, 
                                n_walls, faces, segments, DRs, face_ps, face_vs)
            #print(i, j, len(cr_points))
            if i == j == 1:
                print("crossings:", len(cr_points))
            #H[i][j] = calc_amplitudes(p1_ij, p2_ij, cr_points, cr_faces, d_faces, walls_list)
            H[i][j] = calc_amplitudes(p1_ij, p2_ij, cr_points, cr_faces, d_faces, walls,
                                n_walls, faces, segments, DRs, face_ps, face_vs, fc)
    return H

icon_ap = "./icons/ap4.png"


#print('file values:', __name__)
if __name__ == '__main__':
    #print(__name__)
    #p1 = [12.0, 20.0, 1.0]
    #p2 = [1.0, 65.0, 1.0]

    #p1 = [48.0, 15.0, 1.0]
    #p2 = [53.0, 36.0, 1.0]

    p1 = [3.05, 1.99, 1.0]
    p2 = [5.05, 2.99, 1.0]
    p3 = [16.05, 1.99, 1.0]

    p4 = [8.05, 14.99, 1.0]
    p5 = [9.05, 51.99, 1.0]

    p6 = [3.05, 15.99, 1.0]
    p7 = [5.05, 18.99, 1.0]
    #points, walls_list = open_file("RTS1.map")
    #n_walls, faces, segments, DRs, face_ps, face_vs = walls_to_arrays(walls_list)
    #print(len(face_vs), face_vs[:20])
    #print(len(walls_list[0][0][1]))
    #points, walls_list = open_file("bonn13.map")
    #n_walls, faces, segments, DRs, face_ps, face_vs = walls_to_arrays(walls_list)

    H = mimo_channel_matrix(p1, p2, walls_list)
    #for h in H:
    #    print(h)
    #print(*H)
    #cr_points, cr_faces, d_faces = ray_tracing(p1, p2, walls_list)
    #rays = calc_amplitudes(p1, p2, cr_points, cr_faces, d_faces)
