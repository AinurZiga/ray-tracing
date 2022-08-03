import numba as nb
import numpy as np
import struct

#----------------------------------------------------------------------
# files

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

def bin_to_string1(file):  # new
    material = ''
    file.read(1)
    text = file.read(1)#.decode("utf-8")
    #count = 0
    while text != b'\x00':
        #print("text:", text)
        #if count > 20:
            #print('error:', material)
            #return
        #count += 1
        material += text.decode("utf-8")
        #print("material:", material, len(material))
        text = file.read(1)#.decode("utf-8")
    #print("return")
    #print(material)
    return material

def bin_to_string(file):
    text = file.read(6)
    return text.decode("utf-8")

def bin_to_string7(file, k):
    text = file.read(k)
    return text.decode("utf-8")

def open_file(filename):
    f = open(filename, 'rb')
    try:
        f.read(8)
        Zones = bin_to_int(f)
        points = []
        walls_list = []
        materials = []
        for i in range(Zones):
            f.read(24)
            Npoints = bin_to_int(file = f)
            for _ in range(Npoints):
                points.append(bin_to_float(f))
        Nfigures = bin_to_int(file = f)
        for i1 in range(Nfigures):
            #f.read(80)
            f.read(4*8)
            #print("i1:", i1)
            material = bin_to_string1(f)
            f.read(302-len(material))
            """if i1 == 0:
                material = bin_to_string1(f)
            if i1 == 69:
                f.read(1)
                k = 5
                material = bin_to_string7(f, k)
                f.read(304-k-1)
            elif i1 == 70:
                material = bin_to_string7(f, 9)
                f.read(295)
            else:
                material = bin_to_string(f)
                f.read(298)"""
            materials.append(material)
            #print(i1, material)
            #f.read(298)
            faces = bin_to_int(f)
            #print('faces:', faces)
            #if i1 == 0 and faces != 9:
            #    print("error:", faces)
            #    return 0, 0,0
            #if faces < 1 and faces > 20:
            #    return 0, 0
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
        #print(len(walls_list))
    return points, walls_list, materials

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
        faces.append(faces[-1] + len(walls[i]))
    return len(walls), faces, segments, DRs, np.array(face_ps), np.array(face_vs)

#----------------------------------------------------------------------

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
def d_crossing_wall(p1, p2, n_walls, faces, segments, materials, 
            DRs=np.array([[]]), face_ps=np.array([[]]), face_vs=np.array([[]])):
    #cr_walls = 0
    #faces_d = []
    #faces_theta = []
    pool = np.zeros((2, 3))
    faces_d = nb.typed.List.empty_list(nb.float64)
    faces_theta = nb.typed.List.empty_list(nb.float64)
    #faces_materials = nb.typed.List.empty_list(nb.float64)
    faces_idxs = nb.typed.List.empty_list(nb.float64)
    for i in range(n_walls):  # walls
        if i not in [2]:
            continue
        cr_p1 = [0.0] * 3
        cr_p2 = [0.0] * 3
        #cr_points = []
        for j in range(faces[i+1]-faces[i]):  # faces
            ind = faces[i] + j
            DR = DRs[ind]
            D0 = (DR[0] * face_ps[segments[ind+1]][0] + DR[1] * face_ps[segments[ind+1]][1]
                    + DR[2] * face_ps[segments[ind+1]][2])
            #tmp1 = D0 - DR[0] * p1[0] - DR[1] * p1[1] - DRs[ind][2] * p1[2]
            tmp1 = D0 - DR[0] * p1[0] - DR[1] * p1[1] - DR[2] * p1[2]
            tmp2 = DR[0] * (p2[0] - p1[0]) + DR[1] *(p2[1] - p1[1]) + DR[2] * (p2[2] - p1[2])
            if tmp2 == 0.0:
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
                if not check(pool, np.array(crossing_p)):
                    old_pool = pool[:, :]
                    pool = np.empty((old_pool.shape[0] + 1, old_pool.shape[1]))
                    pool[:-1, :] = old_pool
                    pool[-1,:] = np.array(crossing_p)
                    if cr_p1 != [0.0]*3:
                        cr_p2 = list(crossing_p)
                        #print("Yes i,j,cr_p2:", i, j, cr_p2)
                        tmp = vec_len(cr_p1, cr_p2)
                        if tmp > 1.0:
                            tmp = 1.0
                        faces_d.append(tmp)
                        cr_p1 = [p1[i] - crossing_p[i] for i in range(3)]
                        theta = np.arccos(skal_mul(cr_p1, DR) / vec_len(p1, crossing_p))
                        if theta > np.pi/2:
                            theta = np.pi - theta
                        faces_theta.append(theta)
                        #faces_materials.append(materials[i])
                        faces_idxs.append(i)
                        cr_p1 = [0.0]*3
                        #break
                    else:
                        cr_p1 = list(crossing_p)
    res = np.zeros((3, len(faces_d)), dtype=nb.float64) #TODO
    for i in range(len(faces_d)):
        res[0, i] = faces_d[i]
        res[1, i] = faces_theta[i]
        res[2, i] = faces_idxs[i]
    return res

    
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

@nb.njit(cache=True)
def vec_abs(v):
    s = 0.0
    for i in range(3):
        s += v[i]**2
    return np.sqrt(s)

@nb.njit(cache=True)
def check(A, b):
    a = np.empty(A.shape[1], dtype=np.bool_)
    rows = A.shape[0]
    for r in range(rows):
        a = A[r] == b
        if a.all():
            return True 
    return False
    


def waterpouring(Mt, H_chan):
    r = Mt
    H_sq = np.dot(H_chan,np.matrix(H_chan, dtype=complex).H)
    lambdas = np.linalg.eigvals(H_sq) 
    lambdas = np.sort(lambdas)[::-1]
    p = 1
    gammas = np.zeros((r,1))
    flag = True
    while flag == True:
        lambdas_r_p_1 = lambdas[0:(r-p+1)]
        inv_lambdas_sum =  np.sum(1/lambdas_r_p_1)
        mu = ( Mt / (r - p + 1) ) * ( 1 + inv_lambdas_sum)
        for idx, item in enumerate(lambdas_r_p_1):
            gammas[idx] = mu - (Mt/(item))
        if gammas[r-p] < 0:
            gammas[r-p] = 0
            p = p + 1
        else:
            flag = False
    res = []
    for gamma in gammas:
        res.append(float(gamma))
    return np.array(res)