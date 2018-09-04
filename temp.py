# -*- coding: utf-8 -*-
import numpy as np
from scipy.optimize import linprog
from transport_solve import Data, show_matrix


def linporg_calc(_c, _a, _b):
    def make_cof(size, r=None, c=None):
        t1 = np.ones(size)
        if r != None:
            t2 = np.zeros((size[0], size[0]))
            t2[r, 0] = 1
            return np.dot(t2, t1)
        elif c != None:
            t3 = np.zeros(size)
            t3[:, c] = 1
            return t3
        else:
            print '请输入正确参数'

    def make_constriant(cm, a, b):
        # produce constraint
        if len(a) == cm.shape[0]:
            A = []
            for r in range(len(a)):
                teq = make_cof(cm.shape, r=r, c=None)
                A.append(teq.flatten())
            A = np.array(A)
        else:
            print "produce constriant don't match transport matrix"
            return
        # sale constraint
        if len(b) == cm.shape[1]:
            B = []
            for c in range(len(b)):
                tub = make_cof(cm.shape, r=None, c=c)
                B.append(tub.flatten())
            B = np.array(B)
        else:
            print "sale constriant don't match transport matrix"
            return
        return A, B

    def Lpsolve(cm, A, a, B, b):
        bounds = [(0, None) for _ in range(len(cm.flatten()))]
        if np.sum(a) == np.sum(b):
            b_eq = np.hstack((a, b))
            a_eq = np.vstack((A, B))
            res = linprog(cm.flatten(), A_eq=a_eq, b_eq=b_eq, bounds=bounds)
        elif np.sum(a) < np.sum(b):
            res = linprog(cm.flatten(), A_ub=B, b_ub=b,
                          A_eq=A, b_eq=a, bounds=bounds)
        elif np.sum(a) > np.sum(b):
            res = linprog(cm.flatten(), A_ub=A, b_ub=a,
                          A_eq=B, b_eq=b, bounds=bounds)
        return res

    cm = np.asarray(c)
    a = np.asarray(_a)
    b = np.asarray(_b)
    cm = cm.reshape((a.shape[0], b.shape[0]))
    A, B = make_constriant(cm, a, b)
    res = Lpsolve(cm, A, a, B, b)
    return res

c = [8, 11, 16, 90, 2, 80, 75, 84, 42, 40, 23, 68, 7, 64, 18, 40]
a = [73, 47]
b = [60, 85, 35, 2, 73, 78, 46, 84]
res = linporg_calc(c, a, b)
data = Data.reshape(res.x.astype(int).tolist(), a, b)
print 'final matrix:\n{}'.format(show_matrix(data))
print 'fare: {}'.format(res.fun)
