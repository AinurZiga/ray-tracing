import numba as nb
import numpy as np

    
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