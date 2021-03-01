import numpy as np
import os
from multiprocessing import Pool
from sim_utilities import *
from sim_dyn import *


def sim_main(kwargs, Z=[]):
    """
    :param
    :return:
    """
    N = kwargs["N"]

    if kwargs['init']:
        # tmp_Z_static = 2 * np.random.rand(N, kwargs["M_static"]) - 1 # -1 to 1
        tmp_Z_static = np.random.normal(0, .25, size=(N, kwargs["M_static"]))  # -1 to 1
        tmp_Z_static[tmp_Z_static < -1] = -1
        tmp_Z_static[tmp_Z_static > 1] = 1
        # tmp_Z_dyn = 2 * np.random.rand(N, kwargs["M_dyn"]) - 1
        tmp_Z_dyn = np.random.normal(0, .25, size=(N, kwargs["M_dyn"]))
        tmp_Z_dyn[tmp_Z_dyn < -1] = -1
        tmp_Z_dyn[tmp_Z_dyn > 1] = 1

        # static
        tmp_Z_static = np.ones((N, kwargs["M_static"]))  # -1 to 1
        tmp_Z_static[:int(N // 2), :] = -1
        tmp_Z_static[int(N // 2):, :] = 1

        Z = np.hstack((tmp_Z_dyn, tmp_Z_static))

        # kwargs["M_dyn"] to unit ball
        for i in range(N):
            norm = np.linalg.norm(Z[i, :kwargs["M_dyn"]], ord=2)
            if norm > 1.:
                Z[i, :kwargs["M_dyn"]] /= norm
    else:  # for hysteresis tests, input the final Z of the previous round to the next
        pass

    kwargs.update({"A": []})

    print("into funcs -- ")
    Z = sim(Z, kwargs)  # Z is changed inplace

    return Z


def sim(Z, kwargs):  # kwargs is changed within the func
    """

    :param Z:
    :param kwargs:
    :return:
    """
    # model parameters
    # party division: N2 vs. N-N2
    N = kwargs["N"]

    Z = update_we(Z, kwargs)
    print("update finished;")  # reached

    return Z

def run(kwargs):
    subfolder = 'current'
    try:
        os.mkdir(kwargs['path'])
    except FileExistsError:
        pass

    try:
        os.mkdir(kwargs['path'] + '{}/'.format(subfolder))
    except FileExistsError:
        pass

    trials = kwargs['T']
    Z = []

    # hys test
    if kwargs['shock_incre'] == True:
        '''
        forward/backward for the shock importance \gamma, \sigma is not used here
        '''
        for i in range(trials):
            shock_l = np.hstack([np.arange(0, 1, 0.1), [1]])
            start = True
            for direct in [0, 1]:
                kwargs['direct'] = direct
                if direct == 1:
                    shock_l = shock_l[::-1]
                for shock in shock_l:
                    kwargs['shock'] = shock
                    if start:
                        kwargs["init"] = True
                        kwargs['step_lim'] = 50000
                        Z = sim_main(kwargs)
                        start = False
                    else:
                        kwargs["init"] = False
                        kwargs['step_lim'] = 50000
                        if shock == 0:
                            kwargs['step_lim'] = 50000
                        Z = sim_main(kwargs, Z)
                        Z = Z[:, 1:]
                        kwargs["M_dyn"] -= 1
                # if kwargs['M_dyn'] <= 3:
            #     sim_visual.generate_gif()
    elif kwargs['alpha_incre'] == True:
        alpha_start = kwargs['alpha']
        alpha_end = kwargs['alpha_end']
        for i in range(trials):
            l = np.hstack([np.arange(alpha_start, alpha_end, .2), [1]])  # demo
            start = True
            for direct in [0, 1]:
                kwargs['direct'] = direct
                if direct == 1:  # alpha decrease
                    l = l[::-1]
                for cond in l:
                    kwargs['alpha'] = cond
                    if start:
                        kwargs["init"] = True
                        kwargs['step_lim'] = 50000
                        Z = sim_main(kwargs)
                        start = False
                    else:
                        kwargs["init"] = False
                        kwargs['step_lim'] = 50000
                        Z = sim_main(kwargs, Z)
    elif kwargs['party_w_incre'] == 1:  # todo: generalize the hys test
        party_w_start = kwargs['party_w']
        party_w_end = kwargs['party_w_end']
        for i in range(trials):
            l = np.hstack([np.arange(party_w_start, party_w_end, .2), [1]])  # demo
            start = True
            for direct in [0, 1]:
                kwargs['direct'] = direct
                if direct == 1:  # alpha decrease
                    l = l[::-1]
                for cond in l:
                    kwargs['party_w'] = cond
                    if start:
                        kwargs["init"] = True
                        kwargs['step_lim'] = 50000
                        Z = sim_main(kwargs)
                        start = False
                    else:
                        kwargs["init"] = False
                        kwargs['step_lim'] = 50000
                        Z = sim_main(kwargs, Z)
    else:
        kwargs["init"] = True
        for i in range(trials):
             _ = sim_main(kwargs)



if __name__ == "__main__":

    params = [{
        "N": N,
        "log_s": log_s,
        "alpha": alpha,  # radius of attraction
        "alpha_end": alpha_end,  # radius of attraction
        "alpha_incre": alpha_incre,
        "party_w": party_w,
        "party_w_end": party_w,
        "party_w_incre": party_w_incre,
        'shock': shock,
        'shock_incre': shock_incre,
        'shock_time_std': shock_time_std,
        'path': path,
        'step_lim': step_lim,
        "M_dyn": M_dyn,
        "M_static": M_static,
        "T": T,
    }
        for alpha in [.5]
        for alpha_end in [-1]
        for alpha_incre in [False]
        for party_w in [.5]
        for party_end in [-1]
        for party_w_incre in [False]
        for shock in [.5]  # exo-shock weight
        for shock_incre in [False]
        for shock_time_std in [.4]
        for step_lim in [50000]  # use 40000-50000 for log_s = 10
        for T in [1]
        for path in [
            'log/',
        ]
        for log_s in [10]
        for (M_dyn, M_static) in [(10, 1)]
        for N in [100]
    ]

    # multiprocessing -
    # cores = 10
    # pool = Pool(cores)
    # res = pool.map(run, params)
    # pool.close()
    # pool.join()

    run(params[0])
