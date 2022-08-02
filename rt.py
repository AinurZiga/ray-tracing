import numpy as np
import multiprocessing
import numba as nb

#import values5 as values   # TODO
import functions
import logging
logging.basicConfig(filename='./logs/rt.log', filemode='w',level=logging.INFO)

import warnings
warnings.filterwarnings("ignore")


class Ray_tracing:
    def __init__(self, p_BS, walls, materials, 
                n_walls, facets, segments, 
                DRs, facet_ps, facet_vs, fc, method='image',
                type='rigorous') -> None:
        self.p_BS = p_BS
        self.walls = walls
        self.materials = materials
        self.n_walls = n_walls
        self.facets = facets
        self.segments = segments 
        self.DRs = DRs
        self.facet_ps = facet_ps
        self.facet_vs = facet_vs
        self.fc = fc
        self.method = method
        self.type = type

        self.floor_h = 0.0
        self.ceil_h = 4.0

        self._init()
        pass

    def _init(self):
        self.dict_materials = {}
        self.dict_materials['Brick': 3.75 - 1j * (17.98 * 0.038 / (self.fc/10**9))]
        self.dict_materials['Wood': 1.99 - 1j * (17.98 * 0.0047 * (self.fc/10**9)**(1.0718-1))]
        #self.dict_materials['Ceiling decking': 3.75 - 1j * (17.98 * 0.038 / self.fc * 10**9)]
        self.dict_materials['Metal': 3.75 - 1j * (17.98 * 0.038 / self.fc * 10**9)]  #TODO

    def mimo_rates_help(self, p1):
        p1 = list(p1)
        p1[2] = 1.0
        #fc = 5.6 * 10**9
        c = 3 * 10**8
        lamda = c / self.fc
        #p_BS = [54.0, 35.0, 2.5]
        p_rates = []
        H = self.mimo_channel_matrix_rigorous(self.p_BS, p1)
        try:
            H = H * lamda / (4*np.pi) * 10**(119/20)
            eig_values, _ = np.linalg.eig(np.dot(H, np.conj(H).T))
            eig_values = eig_values.real
            eig_values = np.sort(eig_values)[::-1]
            p_rates += p1[:2]
            value1 = np.sum(eig_values/np.max(eig_values) > 0.05)
            value2 = np.sum(np.log2(1 + eig_values/3))
            value5 = np.log2(1 + np.abs(H[1,1])**2)
            value6 = np.sum(eig_values) / np.min(eig_values)  # Demmel
            gammas = functions.waterpouring(3, H)
            #print("gammas:", gammas)
            value4 = np.sum(np.log2(1 + gammas*eig_values/3))
            value3 = np.sum(gammas > 0.01)
        except:
            print("except:", H)
            p_rates += p1[:2]
            value1 = 1
            value2 = 1
            value3 = 1
            value4 = 1
            value5 = 1
            value6 = 10**4
        p_rates += value1,
        p_rates += value2,
        p_rates += value3,
        p_rates += value4,
        p_rates += value5,  # make sense for rt_rig
        p_rates += value6,
        return p_rates

    def mimo_channel_matrix(self, p1, p2):
        if self.type == 'rigorous':
            return self._mimo_channel_matrix_rigorous(p1, p2)

    def _mimo_channel_matrix_rigorous_old(self, p1, p2):
        # вернуть полную канальную матрицу
        shift = 82/1000
        H = np.zeros((3,3), dtype=np.complex128)
        for i in range(3):
            for j in range(3):
                p1_ij = list(p1)
                p1_ij[0] += shift * (i - 1)
                p2_ij = list(p2)
                p2_ij[0] += shift * (j - 1)
                cr_points, filter_idx, d_facets = self._image_method(p1_ij, p2_ij)
                H[i][j] = self._calc_amplitudes(p1, p2, cr_points, d_facets)
        #cr_points, cr_facets, d_facets = self.image_method(p1, p2)
        return H

    def _mimo_channel_matrix_rigorous(self, p1, p2):
        # вернуть полную канальную матрицу
        shift = 82/1000
        H = np.zeros((3,3), dtype=np.complex128)
        cr_points, d_facets, filter_idx = self._image_method(p1, p2)
        for i in range(3):
            for j in range(3):
                p1_ij = list(p1)
                p1_ij[0] += shift * (i - 1)
                p2_ij = list(p2)
                p2_ij[0] += shift * (j - 1)
                #cr_points, filter_idx, d_facets = self._image_method(p1_ij, p2_ij)
                logging.info("H[i][j]:" + str((i,j)) + '\n')
                cr_points, d_facets, _ = self._image_method(p1_ij, p2_ij, filter_idx)
                H[i][j] = self._calc_amplitudes(p1, p2, cr_points, d_facets)
        #cr_points, cr_facets, d_facets = self.image_method(p1, p2)
        return H

    def _calc_amplitudes(self, p1, p2, cr_points, d_facets):
        c = 3*10**8
        lamda = c / self.fc
        #k = 2*3.14 / lamda
        eta_brick = 3.75 - 1j * (17.98 * 0.038 / 5.6)
        eta_wood = 1.99 - 1j * (17.98 * 0.0047 * 5.6**1.0718 / 5.6)
        #Ampl = 2*lamda / (4*np.pi)  # + antenna gain
        Ampl = 2  # + antenna gain
        #eta = eta_brick
        D_direct = functions.vec_len(p1, p2)
        ray0 = Ampl * np.exp(-2j*np.pi*self.fc*D_direct/c) / D_direct
        facets_d_theta = self.d_crossing_wall(p1, p2)
        logging.info("facets_d_theta:" +str(facets_d_theta))
        #print("facets_d_theta:", facets_d_theta)
        for i in range(facets_d_theta.shape[1]):
            facet_d = facets_d_theta[0, i]
            facet_theta = facets_d_theta[1, i]
            #eta = 3.75 - 1j * (17.98 * 0.038 / 5.6)   # brick
            eta = eta_brick
            q = 6.28*facet_d/lamda * np.sqrt(eta - np.sin(facet_theta)**2)
            tmp1 = np.cos(facet_theta) - np.sqrt(facet_theta - np.sin(facet_theta)**2)
            tmp2 = np.cos(facet_theta) + np.sqrt(facet_theta - np.sin(facet_theta)**2)
            R_prime = tmp1 / tmp2
            tmp2 = 1 - R_prime**2 * np.exp(-2j*q)
            tmp3 = (1 - R_prime**2)*(np.exp(-1j*q))
            T = tmp3 / tmp2
            ray0 = ray0 * T
            logging.info('Direct ray wall passes i, T: ' + str((i, np.abs(T))) + '\n')
        rays = ray0
        logging.info('Direct ray0: ' + str(np.abs(ray0))+ '\n')

        for i, point in enumerate(cr_points):
            d = d_facets[i]
            tmp1 = sum([(p1[i] - point[i])*(p2[i] - point[i]) for i in range(3)])
            tmp2 = functions.vec_len(p1, point) * functions.vec_len(p2, point)
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
            D = functions.vec_len(p1, point) + functions.vec_len(p2, point)
            tau = D / c
            ray = Ampl * R * np.exp(-2j*np.pi*self.fc*tau) / D
            C1 = [point[j] - (point[j] - p1[j])*0.001 for j in range(3)]
            C2 = [point[j] - (point[j] - p2[j])*0.001 for j in range(3)]
            facets_d_theta1 = self.d_crossing_wall(p1, C1)
            facets_d_theta2 = self.d_crossing_wall(p2, C2)
            facets_d_theta = np.hstack((facets_d_theta1, facets_d_theta2))
            for i in range(facets_d_theta.shape[1]):  # crossings through wall
                #eta = 3.75 - 1j * (17.98 * 0.038 / 5.6)   # brick
                eta = eta_brick
                facet_d = facets_d_theta[0, i]
                facet_theta = facets_d_theta[1, i]
                q = 6.28*facet_d/lamda * np.sqrt(eta - np.sin(facet_theta)**2)
                tmp1 = np.cos(facet_theta) - np.sqrt(facet_theta - np.sin(facet_theta)**2)
                tmp2 = np.cos(facet_theta) + np.sqrt(facet_theta - np.sin(facet_theta)**2)
                R_prime = tmp1 / tmp2
                tmp2 = 1 - R_prime**2 * np.exp(-2j*q)
                tmp3 = (1 - R_prime**2)*(np.exp(-1j*q))
                T = tmp3 / tmp2
                ray = ray * T     
                logging.info('Reflection i,T: ' + str((i,np.abs(T))) + '\n')   
            rays += ray
            logging.info('Reflections d_refl, theta, R, tau, ray: ' + str((d,theta*57.3, 
                    np.abs(R), tau*10**6, np.abs(ray))) + '\n')
        return rays
    
    def _image_method(self, p1, p2, filter_idx=None):
        """ Finds reflected rays """
        cr_points = []
        #cf_facets = []
        d_facets = []
        idx_walls = []
        count = 0

        los_crossings = self.crossing_wall(p1, p2)
        for i in range(len(self.walls)):
            if filter_idx and i not in filter_idx:
                continue
            for j in range(len(self.walls[i])):
                # Проверим, находяться ли точки p1 и p2 по одну сторону от плоскости
                # подставим их в уравнение плоскости
                facet = self.walls[i][j]
                #print(face); return
                DR = facet[0]
                D = -(DR[0]*facet[1][0][0] + DR[1]*facet[1][0][1] + DR[2]*facet[1][0][2])
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
                    facet_p, facet_v = [], []
                    for k in range(len(facet[1])//2):
                        facet_p.append(facet[1][2*k])
                        facet_v.append(facet[1][2*k+1])
                    if not functions.is_point_inside_figure(C, np.array(facet[0]), np.array(facet_p), np.array(facet_v)):
                        continue
                    #if i == 20 and j == 7:
                    #    print("YES")
                    impinging = [C[i] - p1[i] for i in range(3)]  # падающий луч
                    if functions.skal_mul(impinging, DR) >= 0:
                        continue
                    C1 = [C[i] - (C[i] - p1[i])*0.001 for i in range(3)]
                    C2 = [C[i] - (C[i] - p2[i])*0.001 for i in range(3)]
                    los1 = self.crossing_wall(p1, C1)
                    los2 = self.crossing_wall(p2, C2)
                    if (los1 + los2 <= los_crossings+1) and (C not in cr_points):
                        #cf_facets.append(facet)
                        cr_points.append(C)
                        idx = 2*(j-2)-1
                        if idx < 1:
                            idx += 2
                            if idx < 1:
                                idx = 1
                        #print(self.walls[i][0][1][2*(j-2)-1])
                        #print(self.walls[i][0][1][idx])
                        d = functions.vec_abs(self.walls[i][0][1][idx])  #TODO
                        print(d)
                        if d > 0.5:
                            d = 0.5
                        d_facets.append(d)
                        idx_walls.append(i)
                        count += 1
                        #print("cr_points:", i,j, C)
                        logging.info("Found reflection i,j,los,C:" + str((i,j,los1+los2, C)))
        #print("cr_points:", cr_points)
        C = self._floor_reflect(p1, p2, los_crossings)
        if C and (C not in cr_points):
            cr_points.append(C)
            d_facets.append(0.3)
        C = self._ceil_reflect(p1, p2, los_crossings)
        if C and (C not in cr_points):
            cr_points.append(C)
            d_facets.append(0.3)
        #print("cr_points:", len(cr_points), cr_points)
        return cr_points, d_facets, idx_walls

    def _floor_reflect(self, p1, p2, los_crossings):
        k = p2[2] / p1[2]
        C = [0.0]*3
        #C = [self.floor_h]*3
        C[2] = self.floor_h
        C[0] = p1[0] + (p2[0] - p1[0])/(k + 1)
        C[1] = p1[1] + (p2[1] - p1[1])/(k + 1)
        C1 = [C[i] - (C[i] - p1[i])*0.001 for i in range(3)]
        C2 = [C[i] - (C[i] - p2[i])*0.001 for i in range(3)]
        los1 = self.crossing_wall(p1, C1)
        los2 = self.crossing_wall(p2, C2)
        if los1 + los2 <= los_crossings+1:
            return C
        return None

    def _ceil_reflect(self, p1, p2, los_crossings):
        k = p2[2] / p1[2]
        C = [0.0]*3
        #C = [self.ceil_h]*3
        C[2] = self.ceil_h
        C[0] = p1[0] + (p2[0] - p1[0])/(k + 1)
        C[1] = p1[1] + (p2[1] - p1[1])/(k + 1)
        C1 = [C[i] - (C[i] - p1[i])*0.001 for i in range(3)]
        C2 = [C[i] - (C[i] - p2[i])*0.001 for i in range(3)]
        los1 = self.crossing_wall(p1, C1)
        los2 = self.crossing_wall(p2, C2)
        if los1 + los2 <= los_crossings+1:
            return C
        return None

    def d_crossing_wall(self, p1, p2):
        return functions.d_crossing_wall(p1, p2, self.n_walls, self.facets, self.segments, 
                np.array(self.DRs), np.array(self.facet_ps), np.array(self.facet_vs))

    """@nb.njit(cache=True)
    def d_crossing_wall(self, p1, p2):
        cr_walls = 0
        #faces_d = []
        #faces_theta = []
        pool = np.zeros((2, 3))
        facets_d = nb.typed.List.empty_list(nb.float64)
        facets_theta = nb.typed.List.empty_list(nb.float64)
        for i in range(self.n_walls):  # walls
            cr_p1 = [0.0] * 3
            cr_p2 = [0.0] * 3
            for j in range(self.facets[i+1]-self.facets[i]):  # facets
                #cr_p1 = [0.0] * 3
                #cr_p2 = [0.0] * 3
                #cr_p2 = np.zeros(3)
                #face_crossings = np.zeros((2, 3))
                #face_crossings = []
                ind = self.facets[i] + j
                DR = self.DRs[ind]
                D0 = (DR[0] * self.facet_ps[self.segments[ind]][0] + 
                            DR[1] * self.facet_ps[self.segments[ind]][1] +
                            DR[2] * self.facet_ps[self.segments[ind]][2])
                tmp1 = D0 - DR[0] * p1[0] - DR[1] * p1[1] - self.DRs[ind][2] * p1[2]
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
                                    self.facet_ps[self.segments[ind]:self.segments[ind + 1], :], 
                                    self.facet_vs[self.segments[ind]:self.segments[ind + 1], :]):
                    #if not cr_walls:
                    #    pool = np.zeros((2, 3))
                    #    pool[0,:] = np.array(crossing_p)
                    #    pool[1,:] = np.array(crossing_p)
                        #pool = np.vstack((np.array(crossing_p), np.array(crossing_p)))
                        #cr_p1 = np.array(crossing_p)
                    #    cr_p1 = list(crossing_p)
                    #    print("Yes cr_p1:", cr_p1)
                    #    cr_walls += 1
                    if not functions.check(pool, np.array(crossing_p)):
                        old_pool = pool[:, :]
                        pool = np.empty((old_pool.shape[0] + 1, old_pool.shape[1]))
                        pool[:-1, :] = old_pool
                        pool[-1,:] = np.array(crossing_p)
                        if cr_p1 != [0.0]*3:
                            #cr_p2 = np.array(crossing_p)
                            cr_p2 = list(crossing_p)
                            #print("Yes cr_p2:", cr_p2)
                            tmp = functions.vec_len(cr_p1, cr_p2)
                            if tmp > 1.0:
                                tmp = 1.0
                            facets_d.append(tmp)
                            cr_p1 = [p1[i] - crossing_p[i] for i in range(3)]
                            theta = np.arccos(functions.skal_mul(cr_p1, DR) / 
                                                functions.vec_len(p1, crossing_p))
                            if theta > np.pi/2:
                                theta = np.pi - theta
                            facets_theta.append(theta)
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
                facets_d.append(0.15)
                facets_theta.append(45/57.3)
        res = np.zeros((2, len(facets_d)), dtype=nb.float64) #TODO
        for i in range(len(facets_d)):
            res[0, i] = facets_d[i]
            res[1, i] = facets_theta[i]
        #res[0, :] = np.array(faces_d)
        #res[1, :] = np.array(faces_theta)
        #res[0, :] = faces_d
        #res[1, :] = faces_theta
        return res"""

    def crossing_wall(self, p1, p2):
        return functions.crossing_wall(p1, p2, self.n_walls, self.facets, self.segments, 
                np.array(self.DRs), np.array(self.facet_ps), np.array(self.facet_vs))

    """@nb.njit(cache=True)
    def crossing_wall(self, p1, p2):
        cr_walls = 0
        #pool_cr_points = np.array([])
        #pool_cr_points = None
        for i in range(self.n_walls):  # walls
            first_interaction = False
            for j in range(self.facets[i+1]-self.facets[i]):  # faces
                ind = self.facets[i] + j
                DR = self.DRs[ind]
                D0 = (DR[0] * self.facet_ps[self.segments[ind]][0] + DR[1] * self.face_ps[self.segments[ind]][1]
                        + DR[2] * self.face_ps[self.segments[ind]][2])
                tmp1 = D0 - DR[0] * p1[0] - DR[1] * p1[1] - self.DRs[ind][2] * p1[2]
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
                                    self.facet_ps[self.segments[ind]:self.segments[ind + 1], :], 
                                    self.facet_vs[self.segments[ind]:self.segments[ind + 1], :]):
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
                    elif not functions.check(pool, np.array(crossing_p)):
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
        return cr_walls"""

    #@nb.njit(cache=True)
    def is_crossing_wall(self, p1, p2):
        cr_walls = 0
        #print('len walls: ', len(walls))
        for i in range(len(self.walls)):
            for j in range(len(self.walls[i])):
                facet = self.walls[i][j]
                DR = facet[0]
                #print(i)
                #print('DR:', DR)
                #print('face:', face[1], len(face[1]))
                D0 = (DR[0] * facet[1][0][0] + DR[1] * facet[1][0][1]
                        + DR[2] * facet[1][0][2])
                tmp1 = D0 - DR[0] * p1[0] - DR[1] * p1[1] - DR[2] * p1[2]
                tmp2 = DR[0] * (p2[0] - p1[0]) + DR[1] *(p2[1] - p1[1]) + DR[2] * (p2[2] - p1[2])
                if tmp2 == 0:
                    continue
                t0 = tmp1 / tmp2
                crossing_p = [0.0] * 3
                for k in range(3):
                    crossing_p[k] = (p2[k] - p1[k]) * t0 + p1[k]
                if functions.skal(crossing_p, p1, p2) > 0:
                    continue
                facet_p, facet_v = [], []
                for i in range(len(facet[1])//2):
                    facet_p.append(facet[1][2*i])
                    facet_v.append(facet[1][2*i+1])
                if functions.is_point_inside_figure(crossing_p, np.array(facet[0]), np.array(facet_p), np.array(facet_v)):
                    #print('crossing point:', crossing_p)
                    return True
        return False
        

    """@nb.njit(cache=True)
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
        return False"""
        


def fun(f, q_in, q_out):
    while True:
        i, x = q_in.get()
        if i is None:
            break
        print(i)
        q_out.put((i, f(x)))


def parmap(f, X, nprocs=multiprocessing.cpu_count()-2):
    q_in = multiprocessing.Queue(1)
    q_out = multiprocessing.Queue()
    #print(nprocs)

    proc = [multiprocessing.Process(target=fun, 
            args=(f, q_in, q_out)) for _ in range(nprocs)]
    for p in proc:
        p.daemon = True
        p.start()

    sent = [q_in.put((i, x)) for i, x in enumerate(X)]
    [q_in.put((None, None)) for _ in range(nprocs)]
    res = [q_out.get() for _ in range(len(sent))]

    [p.join() for p in proc]

    return [x for i, x in sorted(res)]

