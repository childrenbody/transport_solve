# -*- coding: utf-8 -*-

class Data():
    def __init__(self, _c, _a, _b):
        self.c = self.reshape(_c, _a, _b)
        self.a = _a[:]
        self.b = _b[:]
        self.flag = sum(_a) - sum(_b)
        self.a_re = _a[:]
        self.b_re = _b[:]

    def new_fare_matrix(self):
        res = matrix_copy(self.c)
        if self.flag > 0:
            for r in range(len(res)):
                res[r].append(0)
            self.b_re.append(abs(self.flag))
        elif self.flag < 0:
            res.append([0] * len(res[0]))
            self.a_re.append(abs(self.flag))
        else:
            pass
        self.cf = res

    @staticmethod
    def reshape(_c, _a, _b):
        al = len(_a); bl = len(_b); cl = len(_c)
        if al * bl != cl:
            print 'cannot reshape array of size {} in shape ({},{})'.format(cl, al, bl)
            return False
        else:
            row = []
            for i, v in enumerate(_c):
                if i % bl == 0:
                    column = [v]
                elif (i + 1) % bl == 0:
                    column.append(v)
                    row.append(column)
                else:
                    column.append(v)
            if len(row) != al:
                print 'reshape function have a mistake'
            return row

class MinimumElement(Data):
    def make_index_list(self):
        rows = len(self.c)
        columns = len(self.c[0])
        index_list = []
        for r in range(rows):
            for c in range(columns):
                index_list.append((r, c))
        self.im = index_list

    def make_transport_matrix(self):
        rows = len(self.cf)
        columns = len(self.cf[0])
        res = []
        for r in range(rows):
            _row = [0] * columns
            res.append(_row)
        self.ct = res

    def find_minimum_element_index(self):
        _min = 0xffffffff
        min_index = None
        for r, c in self.im:
            if self.c[r][c] < _min:
                _min = self.c[r][c]
                min_index = r, c
        return min_index

    def update_transport_matrix(self, min_index):
        if min_index:
            r, c = min_index
            if self.a_re[r] != 0 and self.b_re[c] != 0:
                if self.a_re[r] >= self.b_re[c]:
                    self.ct[r][c] = self.b_re[c]
                    self.a_re[r] -= self.b_re[c]
                    self.b_re[c] = 0
                elif self.a_re[r] < self.b_re[c]:
                    self.ct[r][c] = self.a_re[r]
                    self.b_re[c] -= self.a_re[r]
                    self.a_re[r] = 0
                else:
                    print 'update transport matrix hava a mistake'
            else:
                print "index list haven't update"	
        else: 
            def only_one_nonzero(_list):
                _all = list(map(lambda x: 1 if x != 0 else 0, _list))
                return True if sum(_all) == 1 else False

            if self.flag > 0:
                if only_one_nonzero(self.a_re):
                    r = self.a_re.index(sum(self.a_re))
                    self.ct[r][-1] = sum(self.a_re)
                else:
                    print 'a remained is error'
            elif self.flag < 0:
                if only_one_nonzero(self.b_re):
                    c = self.b_re.index(sum(self.b_re))
                    self.ct[-1][c] = sum(self.b_re)
                else:
                    print 'b remained is error'
            else:
                pass

    def update_index_list(self, min_index):
        r, c = min_index
        if self.a_re[r] == 0:
            try:
                self.im = list(filter(lambda x: x[0] != r, self.im))
            except:
                print 'a constriant remove have a mistake'

        if self.b_re[c] == 0:
            try:
                self.im = list(filter(lambda x: x[1] != c, self.im))
            except:
                print 'b constriant remove have a mistake'

    def sum_transport(self):
        res = 0
        for r in range(len(self.ct)):
            for c in range(len(self.ct[0])):
                res += self.ct[r][c]
        return res
    
    def final_transport_matrix(self):
        rows = len(self.c)
        columns = len(self.c[0])
        res = []
        for r in range(rows):
            _row = []
            for c in range(columns):
                _row.append(self.ct[r][c])
            res.append(_row)
        self.final_ct = res
            
    def solve(self):
        self.new_fare_matrix()
        self.make_index_list()
        self.make_transport_matrix()
        min_ind = True
        while min_ind:
            min_ind = self.find_minimum_element_index()
            self.update_transport_matrix(min_ind)
            if min_ind:
                self.update_index_list(min_ind)
        self.final_transport_matrix()

    def calc_fare(self):
        try:
            tm = self.final_ct
        except:
            self.final_transport_matrix()
            tm = self.final_ct
        fare = 0
        for r in range(len(self.c)):
            for c in range(len(self.c[0])):
                fare += self.final_ct[r][c] * self.c[r][c]
        self.fare = fare

class Vogel(Data):
    pass

class Examine():
    def __init__(self, transport_matrix, fare_matrix):
        self.tm = matrix_copy(transport_matrix)
        self.fm = matrix_copy(fare_matrix)
        self.init_ab_potential()
    
    def create_examine_matrix(self):
        temp = []
        for r in range(len(self.tm)):
            _row = []
            for c in range(len(self.tm[0])):
                if self.tm[r][c] > 0:
                    _row.append(self.fm[r][c])
                else:
                    _row.append(None)
            temp.append(_row)
        self.em = temp

    def init_ab_potential(self):
        self.ap = [None] * len(self.tm)
        self.bp = [None] * len(self.tm[0])

    def make_nonzero_element_index(self):
        index_list = []
        for r in range(len(self.tm)):
            for c in range(len(self.tm[0])):
                if self.tm[r][c] > 0:
                    index_list.append((r, c))
        self.ind = index_list
    
    def fill_ab_potential(self):
        for r, c in self.ind:
            if self.ap[r] != None and self.bp[c] == None:
                self.bp[c] = self.em[r][c] - self.ap[r]
            elif self.ap[r] == None and self.bp[c] != None:
                self.ap[r] = self.em[r][c] - self.bp[c]
            else:
                pass
    
    def init_potential(self):
        for r, c in self.ind:
            if self.ap[r] == None and self.bp[c] == None:
                self.bp[c] = 0
                self.ap[r] = self.em[r][c]
                break
    
    def fill_potential(self):
        _a = self.find_none_element(self.ap)
        _b = self.find_none_element(self.bp)
        last = sum(_a + _b)
        while sum(_a + _b) > 0:
            self.fill_ab_potential()
            _a = self.find_none_element(self.ap)
            _b = self.find_none_element(self.bp)
            if sum(_a + _b) < last:
                last = sum(_a + _b)
            else:
                self.init_potential()
        
    def calc_examine_matrix(self):
        for r in range(len(self.em)):
            for c in range(len(self.em[0])):
                if (r, c) not in self.ind:
                    self.em[r][c] = self.fm[r][c] - (self.ap[r] + self.bp[c])

    def find_minimum_index(self):
        _min = 0
        min_index = None
        for r in range(len(self.em)):
            for c in range(len(self.em[0])):
                if self.em[r][c] < 0 and self.em[r][c] < _min:
                    _min = self.em[r][c]
                    min_index = r, c
                elif self.em[r][c] < 0 and self.em[r][c] == _min:
                    if self.fm[r][c] <  self.fm[min_index[0]][min_index[1]]:
                        min_index = r, c 
        return min_index

    def solve_examine(self):
        self.create_examine_matrix()
        self.make_nonzero_element_index()
        self.fill_potential()
        self.calc_examine_matrix()
        min_index = self.find_minimum_index()
        if min_index:
            #print 'position {} need to optimize'.format(min_index)
            pass
        else:
            #print 'good job!'
            pass
        return min_index
    
    @staticmethod
    def find_none_element(_list):
        return list(map(lambda x: 1 if x == None else 0, _list))

class ClosedLoop():
    def __init__(self, transport_matrix, fare_matrix, optimize_index):
        self.tm = matrix_copy(transport_matrix)
        self.fm = matrix_copy(fare_matrix)
        self.optimize_index = optimize_index

    def create_directions(self):
        up = lambda x, y: (x - 1, y)
        down = lambda x, y: (x + 1, y)
        left = lambda x, y: (x, y - 1)
        right = lambda x, y: (x, y + 1)
        self.directions = [up, down, left, right]

    def forward(self, index, enter):
        enter_op = {1:0, 0:1, 2:3, 3:2}
        _path = []
        if enter != None:
            if self.tm[index[0]][index[1]] == 0:
                if not self.arrival_boundary(self.directions[enter](*index)):
                    _path.append(self.directions[enter](*index))
                    #print 'add {}'.format(self.directions[enter](*index))
            else:
                temp = [_ for _ in range(4) if _ != enter_op[enter]]
                #temp = [2, 3] if enter <= 1 else [0, 1]
                for d in temp:
                    if not self.arrival_boundary(self.directions[d](*index)):
                        _path.append(self.directions[d](*index))
        else:
            for func in self.directions:
                if not self.arrival_boundary(func(*index)):
                    _path.append(func(*index))
        return _path
    
    def arrival_boundary(self, index):
        rows = len(self.tm); columns = len(self.tm[0])
        r, c = index
        if r < 0 or r >= rows or c < 0 or c >= columns:
            return True
        else:
            return False

    @staticmethod
    def backward(enter_index, outer_index):
        _er, _ec = enter_index
        _or, _oc = outer_index
        if _ec == _oc:
            code = 0 if _er > _or else 1
        else:
            code = 2 if _ec > _oc else 3
        return code

    def go(self, node):
        print '{} -> {}'.format(node[0], node[1])
        if node[1] == []:
            return False
        if self.optimize_index not in node[1]:
            for i, j in node[1]:
                print 'code: {}'.format(self.backward(node[0], (i, j)))
                print 'enter: {}'.format((i, j))
                forward_path = self.forward(index=(i, j), enter=self.backward(node[0], (i, j)))
                if forward_path:
                    if self.go([(i, j), forward_path]):
                        self.go_path.append((i, j))
                        return True
                else:
                    print 'over'
                    return False
        else:
            return True

    def go_path_drop_non(self):
        for r, c in self.go_path[1:]:
            if self.tm[r][c] == 0:
                self.go_path.remove((r, c))

    def find_close_loop(self):
        self.create_directions()
        self.go_path = [self.optimize_index]
        _node = [self.optimize_index, self.forward(self.optimize_index, enter=None)]
        self.go(_node)

    def create_unit(self, unit=1):
        _min = 0xffffffff
        for r, c in self.go_path[1:]:
            if self.tm[r][c] < _min:
                _min = self.tm[r][c]
        self.unit = _min

    def make_adjust_dict(self):
        if len(self.go_path) % 2 == 0:
            self.adjust_dict = {index: None for index in self.go_path}
            self.adjust_dict[self.optimize_index] = self.unit
            for index, v in self.adjust_dict.items():
                if v == None:
                    _row = [_v for _i, _v in self.adjust_dict.items() if _v != None and _i[0] == index[0]]
                    _column = [_v for _i, _v in self.adjust_dict.items() if _v != None and _i[1] == index[1]]
                    if _row:
                        if sum(_row) != 0:
                            self.adjust_dict[index] = 0 - sum(_row)
                    elif _column:
                        if sum(_column) != 0:
                            self.adjust_dict[index] = 0 - sum(_column)
                    else:
                        print 'adjustment make a mistake'
        else:
            print 'go path is wrong'

    def create_new_transport_matrix(self):
        self.new_tm = matrix_copy(self.tm)
        for r in range(len(self.new_tm)):
            for c in range(len(self.new_tm[0])):
                if (r, c) in self.adjust_dict:
                    self.new_tm[r][c] += self.adjust_dict[(r, c)]

    def calc_new_fare(self):
        fare = 0
        for r in range(len(self.new_tm)):
            for c in range(len(self.new_tm[0])):
                fare += self.new_tm[r][c] * self.fm[r][c]
        self.fare = fare

    def solve(self):
        self.find_close_loop()
        print 'go path: {}'.format(self.go_path)
        self.go_path_drop_non()
        self.create_unit()
        print 'go path: {}'.format(self.go_path)
        self.make_adjust_dict()
        self.create_new_transport_matrix()
        self.calc_new_fare()

def matrix_copy(matrix):
    temp = []
    for r in range(len(matrix)):
        _row = []
        for c in range(len(matrix[0])):
            _row.append(matrix[r][c])
        temp.append(_row)
    return temp

def show_matrix(matrix): 
    string = list(map(str, matrix))
    res = '\n'.join(string)
    return res

def dataset(v=0):
    if v == 0:
        # product == sale
        c = [4, 12, 4, 11, 2, 10, 3, 9, 8, 5, 11, 6]
        a = [16, 10, 22]
        b = [8, 14, 12, 14]
        '''
        result
        [0, 0, 12, 4]
        [8, 0, 2, 0]
        [0, 14, 0, 8]
        '''
    elif v == 1:   
        # produce < sale
        c = [3,12,3,4,11,2,5,9,6,7,1,5]
        a = [8,5,9]
        b = [8,4,6,7]
        '''
        result
        [8, 0, 0, 0]
        [0, 4, 0, 1]
        [0, 0, 6, 3]
        '''
    elif v == 2:
        # produce > sale
        c =[1, 2, 3, 6, 5, 4]
        a = [6, 8]
        b = [4, 3, 2]
        '''
        result
        [4. 2. 0.]
        [0. 1. 2.]
        '''
    elif v == 3:
        # proudct = sale
        # need to optimize
        c = [3,11,3,10,1,9,2,8,7,4,10,5]
        a = [7,4,9]
        b = [3,6,5,6]
        '''
        result
        [0, 0, 5, 2]
        [3, 0, 0, 1]
        [0, 6, 0, 3]
        '''
    elif v == 4:
        # product < sale
        # need to optimize
        c = [22, 92, 22, 33, 91, 35, 2, 56, 13, 40, 52, 20, 3, 65, 97, 86, 46, 76, 39, 44, 80, 54, 7, 55]
        a = [25, 5, 54, 37, 95, 55]
        b = [88, 30, 72, 96]
        '''
        result
        [13.  0. 12.  0.]
        [ 0.  0.  5.  0.]
        [38. 15.  0.  1.]
        [37.  0.  0.  0.]
        [ 0.  0.  0. 95.]
        [ 0.  0. 55.  0.]
        '''
    return c, a, b
    
def test_min():
    c, a, b = dataset(4)
    me = MinimumElement(c, a, b)
    print 'fare matrix:\n{}'.format(show_matrix(me.c))
    print 'a : {}'.format(me.a)
    print 'b : {}'.format(me.b)
    me.new_fare_matrix()
    me.make_index_list()
    print 'index list: {}'.format(me.im)
    me.make_transport_matrix()
    print 'trasnport matrix:\n{}'.format(show_matrix(me.ct))
    print 'a remained: {}'.format(me.a_re)
    print 'b remained: {}'.format(me.b_re)
    min_ind = True
    while min_ind:
        print 'c matrix:\n{}'.format(show_matrix(me.c))
        min_ind = me.find_minimum_element_index()
        print 'minimum index: {}'.format(min_ind)
        me.update_transport_matrix(min_ind)
        print 'transport matrix:\n{}'.format(show_matrix(me.ct))
        print 'a remained: {}'.format(me.a_re)
        print 'b remained: {}'.format(me.b_re)
        if min_ind:
            me.update_index_list(min_ind)
        print 'index list:\n{}'.format(me.im)

def test_examine():
    c, a, b = dataset(3)
    me = MinimumElement(c, a, b)
    me.solve()
    me.calc_fare()
    print 'fare: {}'.format(me.fare)
    _ct = matrix_copy(me.ct)
    _cf = matrix_copy(me.cf)
    exm = Examine(_ct, _cf)
    error_index = exm.solve_examine()
    print 'fare matrix:\n{}'.format(show_matrix(_cf))
    print 'transport matrix:\n{}'.format(show_matrix(_ct))
    print 'examine matrix:\n{}'.format(show_matrix(exm.em))
    print 'ap: {}'.format(exm.ap)
    print 'bp: {}'.format(exm.bp)

def test_closed():
    c, a, b = dataset(4)
    me = MinimumElement(c, a, b)
    me.solve()
    print 'transport_matrix:\n{}'.format(show_matrix(me.ct))
    me.calc_fare()
    print 'fare: {}'.format(me.fare)
    exm = Examine(me.ct, me.cf)
    optimize_index = exm.solve_examine()
    if optimize_index:
        cl = ClosedLoop(me.ct, me.cf, optimize_index)
        cl.find_close_loop()
        print 'closed loop: {}'.format(cl.go_path)
        cl.create_unit()
        cl.make_adjust_dict()
        cl.create_new_transport_matrix()
        print 'new transport matrix:\n{}'.format(show_matrix(cl.new_tm))
        cl.calc_new_fare()
        print 'fare: {}'.format(cl.fare)

def main():
    c, a, b = dataset(4)
    me = MinimumElement(c, a, b)
    me.solve()
    me.calc_fare()
    me_fare = me.fare
    print 'min transport matrix:\n{}'.format(show_matrix(me.final_ct))
    print 'fare: {}'.format(me.fare)
    _ct = me.final_ct
    _fm = me.cf
    op_ind = True
    min_fare = me_fare
    while op_ind:
        exm = Examine(_ct, _fm)
        op_ind = exm.solve_examine()
        print 'examine matrix:\n{}'.format(show_matrix(exm.em))
        print 'ap: {}'.format(exm.ap)
        print 'bp: {}'.format(exm.bp)
        if op_ind:
            print 'optimize matrix: {}'.format(op_ind)
            cl = ClosedLoop(_ct, _fm, op_ind)
            cl.solve()
            _ct = cl.new_tm
            print 'new matrix:\n{}'.format(show_matrix(_ct))
            print 'fare: {}'.format(cl.fare)
            if cl.fare < min_fare:
                min_fare = cl.fare
    print 'final transport matrix:\n{}'.format(show_matrix(_ct))

if __name__ == '__main__':
	#test_min()
    main()
    #test_examine()
    #test_closed()