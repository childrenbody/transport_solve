# -*- coding: utf-8 -*-
import numpy as np
from scipy.optimize import linprog
from transport_solve import MinimumElement, Examine, ClosedLoop, show_matrix, Data


def test_lp(_c, _a, _b):
    data = Data(_c, _a, _b)
    me = MinimumElement(_c, _a, _b)
    me.solve()
    me.calc_fare()
    me_fare = me.fare
    _ct = me.ct
    _fm = me.cf
    op_ind = True
    min_fare = me_fare
    while op_ind:
        exm = Examine(_ct, _fm)
        op_ind = exm.solve_examine()
        if op_ind:
            try:
                cl = ClosedLoop(_ct, _fm, op_ind)
                cl.solve()
                _ct = cl.new_tm
            except:
                break
            if cl.fare < min_fare:
                min_fare = cl.fare
    return np.array(data.final_matrix(_ct)).flatten().tolist()


def linporg_calc(_c, _a, _b):
    def make_cof(size, r=None, c=None):
        t1 = np.ones(size)
        if r is not None:
            t2 = np.zeros((size[0], size[0]))
            t2[r, 0] = 1
            return np.dot(t2, t1)
        elif c is not None:
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
            print("produce constriant don't match transport matrix")
            return
        # sale constraint
        if len(b) == cm.shape[1]:
            B = []
            for c in range(len(b)):
                tub = make_cof(cm.shape, r=None, c=c)
                B.append(tub.flatten())
            B = np.array(B)
        else:
            print("sale constriant don't match transport matrix")
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


result = 0

for i in range(100):
    print 'iter: {}'.format(i)
    rows, columns = np.random.randint(2, 10, 2).tolist()
    c = np.random.randint(1, 100, rows * columns).tolist()
    a = np.random.randint(1, 100, rows).tolist()
    b = np.random.randint(1, 100, columns).tolist()

    lin = linporg_calc(c, a, b)
    if lin.status == 0:
        lp = test_lp(c, a, b)
        # print lp
        # print lin.x.tolist()
        if (lp == lin.x).all():
            result += 1
        else:
            print "c matrix:\n{}".format(show_matrix(Data.reshape(c, a, b)))
            print "a: {}".format(a)
            print 'b: {}'.format(b)


print 'result: {} / 100'.format(result)
