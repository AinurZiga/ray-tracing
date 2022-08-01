import numpy as np
import multiprocessing
import values5 as values   # TODO


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


class Ray_tracing:
    def __init__(self, p_BS, walls_list, 
                n_walls, facets, segments, 
                DRs, face_ps, face_vs, fc) -> None:
        self.p_BS = p_BS
        self.walls_list = walls_list
        self.n_walls = n_walls
        self.facets = facets
        self.segments = segments 
        self.DRs = DRs
        self.face_ps = face_ps
        self.face_vs = face_vs
        self.fc = fc
        pass

    def mimo_rates_help(self, p1):
        p1 = list(p1)
        p1[2] = 1.0
        fc = 5.6 * 10**9
        c = 3 * 10**8
        lamda = c / fc
        p_BS = [54.0, 35.0, 2.5]
        p_rates = []
        H = values.mimo_channel_matrix(p1, p_BS, self.walls_list, 
                    self.n_walls, self.facets, self.segments, 
                    self.DRs, self.face_ps, self.face_vs, fc)
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
            gammas = waterpouring(3, H)
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

