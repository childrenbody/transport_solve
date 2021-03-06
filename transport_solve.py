# -*- coding: utf-8 -*-
import sys, copy
sys.setrecursionlimit(100000000)  # 设置最大递归深度，Python默认是1000


class Data():
    '''数据类，功能如下：
    1、一维列表变成二维矩阵
    2、根据产销是否平衡来适当的增加一列（虚拟销地）或一行（虚拟产地）
    3、根据转运结果，如果在2中有增加列或行，删除该列或行，输出最终的转运结果'''
    def __init__(self, _c, _a, _b):
        # 把一维列表构造成二维矩阵
        self.c = self.reshape(_c, _a, _b)
        # 产量约束条件
        self.a = _a[:]
        # 销量约束条件
        self.b = _b[:]
        # 产销平衡的标志位，如flag>0，产大于销，否则相反。
        self.flag = sum(_a) - sum(_b)
        # 经过划分后，产量和销量的剩余
        self.a_re = _a[:]
        self.b_re = _b[:]

    def new_fare_matrix(self):
        '''如果产销不平衡添加一列（虚拟销地）或一行（虚拟产地）'''
        res = copy.copy(self.c)
        # 产大于销，在末尾增加一列
        if self.flag > 0:
            for r in range(len(res)):
                res[r].append(0)
            self.b_re.append(abs(self.flag))
        # 销大于产，在末尾增加一行
        elif self.flag < 0:
            res.append([0] * len(res[0]))
            self.a_re.append(abs(self.flag))
        else:
            pass
        self.cf = res

    @staticmethod
    def reshape(_c, _a, _b):
        '''把一维列表转成二维矩阵'''
        al = len(_a)
        bl = len(_b)
        cl = len(_c)
        if al * bl != cl:
            raise Exception('cannot reshape array of size {} in shape ({},{})'.format(cl, al, bl))
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
                raise Exception('reshape function have a mistake')
            return row

    def final_matrix(self, new_transport):
        '''根据转运结果，如果在2中有增加列或行，删除该列或行，输出最终的转运结果'''
        temp = []
        for r in range(len(self.c)):
            _row = []
            for c in range(len(self.c[0])):
                _row.append(new_transport[r][c])
            temp.append(_row)
        return temp


class MinimumElement(Data):
    '''最小元素法：优先考虑具有最小运价的供销业务'''

    def make_index_list(self):
        '''构造矩阵中每个元素索引的列表'''
        rows = len(self.c)
        columns = len(self.c[0])
        index_list = []
        for r in range(rows):
            for c in range(columns):
                index_list.append((r, c))
        self.im = index_list

    def make_transport_matrix(self):
        '''构造零矩阵'''
        rows = len(self.cf)
        columns = len(self.cf[0])
        res = []
        for r in range(rows):
            _row = [0] * columns
            res.append(_row)
        self.ct = res

    def find_minimum_element_index(self):
        '''找到最小元素的索引'''
        _min = 0xffffffff
        min_index = None
        for r, c in self.im:
            if self.c[r][c] < _min:
                _min = self.c[r][c]
                min_index = r, c
        return min_index

    def update_transport_matrix(self, min_index):
        '''更新转运矩阵'''
        if min_index:
            r, c = min_index
            # 如果该行的产量与该列的销量都不为零
            if self.a_re[r] != 0 and self.b_re[c] != 0:
                # 如果产量较少，该点的最大运输量等于产量，否则等于销量
                if self.a_re[r] >= self.b_re[c]:
                    self.ct[r][c] = self.b_re[c]
                    self.a_re[r] -= self.b_re[c]
                    self.b_re[c] = 0
                elif self.a_re[r] < self.b_re[c]:
                    self.ct[r][c] = self.a_re[r]
                    self.b_re[c] -= self.a_re[r]
                    self.a_re[r] = 0
                else:
                    raise Exception('update transport matrix hava a mistake')
            else:
                raise Exception("index list haven't update")
        else:
            # 当没有最小元素的索引
            if self.flag > 0:
                # 产量大于销量，此时产量还有剩余，分配进虚拟销地中
                for i, v in enumerate(self.a_re):
                    if v != 0:
                        self.ct[i][-1] = self.a_re[i]
            elif self.flag < 0:
                # 销量大于产量，此时销量还有剩余，分配进虚拟产地中
                for i, v in enumerate(self.b_re):
                    if v != 0:
                        self.ct[-1][i] = self.b_re[i]
            else:
                pass

    def update_index_list(self, min_index):
        '''更新索引列表，把产量为零的行和销量为零的列删除'''
        r, c = min_index
        if self.a_re[r] == 0:
            try:
                self.im = list(filter(lambda x: x[0] != r, self.im))
            except:
                raise Exception('a constriant remove have a mistake')

        if self.b_re[c] == 0:
            try:
                self.im = list(filter(lambda x: x[1] != c, self.im))
            except:
                raise Exception('b constriant remove have a mistake')

    def solve(self):
        '''运行整个最小元素法，接受Exception错误，并打印信息，然后停止程序'''
        try:
            self.new_fare_matrix()
            # print 'fare matrix:\n{}'.format(show_matrix(self.cf))
            self.make_index_list()
            self.make_transport_matrix()
            # print 'transport matrix:\n{}'.format(show_matrix(self.ct))
            min_ind = True
            while min_ind:
                min_ind = self.find_minimum_element_index()
                self.update_transport_matrix(min_ind)
                # print 'transport matrix:\n{}'.format(show_matrix(self.ct))
                # print 'a re: {}'.format(self.a_re)
                # print 'b re: {}'.format(self.b_re)
                if min_ind:
                    self.update_index_list(min_ind)
            self.final_ct = self.final_matrix(self.ct)
        except Exception as e:
            print e
            sys.exit(1)

    def calc_fare(self):
        '''计算总的运费'''
        try:
            tm = self.final_ct
        except:
            self.final_ct = self.find_matrix(self.ct)
            tm = self.final_ct
        fare = 0
        for r in range(len(self.c)):
            for c in range(len(self.c[0])):
                fare += self.final_ct[r][c] * self.c[r][c]
        self.fare = fare


class Vogel(Data):
    pass


class Examine():
    '''位势法：检验是否是最优解'''
    def __init__(self, transport_matrix, fare_matrix):
        self.tm = copy.copy(transport_matrix)  # 初始运输矩阵
        self.fm = copy.copy(fare_matrix)       # 费用矩阵
        self.init_ab_potential()

    def create_examine_matrix(self):
        '''构造保存检验数的矩阵，未计算出的元素用None代替'''
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
        '''初始化行和列的势，没有用None代替'''
        self.ap = [None] * len(self.tm)
        self.bp = [None] * len(self.tm[0])

    def make_nonzero_element_index(self):
        '''记录运输矩阵中非零元素的索引'''
        index_list = []
        for r in range(len(self.tm)):
            for c in range(len(self.tm[0])):
                if self.tm[r][c] > 0:
                    index_list.append((r, c))
        self.ind = index_list

    def fill_ab_potential(self):
        '''根据非零元素的运费，计算行和列的势'''
        for r, c in self.ind:
            if self.ap[r] is not None and self.bp[c] is None:
                self.bp[c] = self.fm[r][c] - self.ap[r]
            elif self.ap[r] is None and self.bp[c] is not None:
                self.ap[r] = self.fm[r][c] - self.bp[c]
            else:
                pass

    def init_potential(self):
        '''初始化行和列的势，在该列填零，然后在该行填该点的运费'''
        for r, c in self.ind:
            if self.ap[r] is None and self.bp[c] is None:
                self.bp[c] = 0
                self.ap[r] = self.em[r][c]
                break

    def fill_potential(self):
        '''计算行和列中未计算的势'''
        _a = self.find_none_element(self.ap)
        _b = self.find_none_element(self.bp)
        last = sum(_a + _b)
        # 如果行和列的势中还有None，就一直循环
        while sum(_a + _b) > 0:
            self.fill_ab_potential()
            _a = self.find_none_element(self.ap)
            _b = self.find_none_element(self.bp)
            if sum(_a + _b) < last:
                last = sum(_a + _b)
            else:
                # 如果行和列的势中None数量跟上一次循环相比并没有变化，就给其中一个None，采用初始化策略
                self.init_potential()

    def calc_examine_matrix(self):
        '''计算检验矩阵中未计算的检验数'''
        for r in range(len(self.em)):
            for c in range(len(self.em[0])):
                if (r, c) not in self.ind:
                    self.em[r][c] = self.fm[r][c] - (self.ap[r] + self.bp[c])

    def find_minimum_index(self):
        '''找到检验矩阵中小于零元素的索引，如果有多个，取最小的，如果相等取运费最小的'''
        _min = 0
        min_index = None
        for r in range(len(self.em)):
            for c in range(len(self.em[0])):
                if self.em[r][c] < 0 and self.em[r][c] < _min:
                    _min = self.em[r][c]
                    min_index = r, c
                elif self.em[r][c] < 0 and self.em[r][c] == _min:
                    if self.fm[r][c] < self.fm[min_index[0]][min_index[1]]:
                        min_index = r, c
        return min_index

    def solve_examine(self):
        '''运用位势法进行检验，并返回需要优化元素的索引'''
        self.create_examine_matrix()
        # print 'init examine matrix:\n{}'.format(show_matrix(self.em))
        self.make_nonzero_element_index()
        self.fill_potential()
        self.calc_examine_matrix()
        min_index = self.find_minimum_index()
        if min_index:
            # print 'position {} need to optimize'.format(min_index)
            pass
        else:
            # print 'good job!'
            pass
        return min_index

    @staticmethod
    def find_none_element(_list):
        '''返回列表中元素是否等于None的列表'''
        return list(map(lambda x: 1 if x is None else 0, _list))


class ClosedLoop():
    '''寻找待优化位置的闭合回路，然后进行调整，返回优化后的矩阵'''
    def __init__(self, transport_matrix, fare_matrix, optimize_index):
        self.tm = copy.copy(transport_matrix)
        self.fm = copy.copy(fare_matrix)
        self.optimize_index = optimize_index

    def create_directions(self):
        '''闭合回路的行走方向，总共有上下左右四个方向'''
        up = lambda x, y: (x - 1, y)
        down = lambda x, y: (x + 1, y)
        left = lambda x, y: (x, y - 1)
        right = lambda x, y: (x, y + 1)
        self.directions = [up, down, left, right]

    def forward(self, index, enter):
        '''返回该点的下一步可前进方向的列表'''
        enter_op = {1: 0, 0: 1, 2: 3, 3: 2}
        _path = []
        if enter is not None:
            # 如果该点的值为零，则直走
            if self.tm[index[0]][index[1]] == 0:
                if not self.arrival_boundary(self.directions[enter](*index)):
                    _path.append(self.directions[enter](*index))
            else:
                # 如果该点的值不为零，则除了不能往回走，其他方向都可以
                temp = [_ for _ in range(4) if _ != enter_op[enter]]
                for d in temp:
                    if not self.arrival_boundary(self.directions[d](*index)):
                        _path.append(self.directions[d](*index))
        else:
            # 如果该点是起点，则四个方向都可走
            for func in self.directions:
                if not self.arrival_boundary(func(*index)):
                    _path.append(func(*index))
        return _path

    def arrival_boundary(self, index):
        '''判断该点是否达到边界'''
        rows = len(self.tm)
        columns = len(self.tm[0])
        r, c = index
        if r < 0 or r >= rows or c < 0 or c >= columns:
            return True
        else:
            return False

    @staticmethod
    def backward(enter_index, outer_index):
        '''上一个点是从哪个方向到达该点的'''
        _er, _ec = enter_index
        _or, _oc = outer_index
        if _ec == _oc:
            code = 0 if _er > _or else 1
        else:
            code = 2 if _ec > _oc else 3
        return code

    def go(self, node):
        '''递归遍历查找回路'''
        # print '{} -> {}'.format(node[0], node[1])
        if node[1] == []:
            return False
        if self.optimize_index not in node[1]:
            for i, j in node[1]:
                # print 'code: {}'.format(self.backward(node[0], (i, j)))
                # print 'enter: {}'.format((i, j))
                forward_path = self.forward(
                    index=(i, j), enter=self.backward(node[0], (i, j)))
                if forward_path:
                    if self.go([(i, j), forward_path]):
                        self.go_path.append((i, j))
                        return True
                else:
                    # print 'over'
                    pass
        else:
            return True

    def go_path_drop_non(self):
        '''只保留闭合回路的顶点'''
        temp = self.go_path[:] + [self.go_path[0]]
        for i in range(1, len(temp) - 1):
            if self.backward(temp[i - 1], temp[i]) == self.backward(temp[i], temp[i + 1]):
                try:
                    self.go_path.remove(temp[i])
                except:
                    pass

    def find_close_loop(self):
        '''寻找闭合回路'''
        self.create_directions()
        self.go_path = [self.optimize_index]
        _node = [self.optimize_index, self.forward(
            self.optimize_index, enter=None)]
        self.go(_node)

    def create_unit(self, unit): 
        '''确定最小调运量 '''
        self.unit = unit

    def make_adjust_dict(self):
        '''确定各个顶点的转运量'''
        def without_none(_dict):
            # 确定是否有None值
            temp = [v for k, v in _dict.items() if v is None]
            return True if len(temp) == 0 else False

        if len(self.go_path) % 2 == 0:
            self.adjust_dict = {index: None for index in self.go_path}
            self.adjust_dict[self.optimize_index] = self.unit
            while not without_none(self.adjust_dict):
                for index, v in self.adjust_dict.items():
                    if v is None:
                        # 确保行和列的运输量守恒
                        _row = [_v for _i, _v in self.adjust_dict.items() if _v is not None and _i[0] == index[0]]
                        _column = [_v for _i, _v in self.adjust_dict.items() if _v is not None and _i[1] == index[1]]
                        if _row:
                            self.adjust_dict[index] = 0 - sum(_row)
                        elif _column:
                            self.adjust_dict[index] = 0 - sum(_column)
                        else:
                            pass
        else:
            raise Exception('go path is wrong')

    def examine_adjust_dict(self):
        '''生成调运方案'''
        def count_more_than_zero(_dict):
            '''检验调运方案是否合理'''
            # 重新调配之后不能有负值
            if [v for v in _dict.values() if v < 0]:
                return False
            # 重新调配之后一定会有一个及以上为零的元素
            elif not [v for v in _dict.values() if v == 0]:
                return False
            return True

        # 以每个点作为最小调运量，生成调运方案，如果该方案合理则采用
        for r, c in self.go_path[1:]:
            unit = self.tm[r][c]
            self.create_unit(unit)
            self.make_adjust_dict()
            self.calc_node_transport()
            if count_more_than_zero(self.node_transportion):
                break

    def calc_node_transport(self):
        '''根据调运方案重新计算闭回路上各个顶点的运输量'''
        temp = dict()
        for index, v in self.adjust_dict.items():
            temp[index] = self.tm[index[0]][index[1]] + self.adjust_dict[index]
        self.node_transportion = temp

    def create_new_transport_matrix(self):
        '''根据调运方案生成新的运输矩阵'''
        self.new_tm = copy.copy(self.tm)
        for r in range(len(self.new_tm)):
            for c in range(len(self.new_tm[0])):
                if (r, c) in self.adjust_dict:
                    self.new_tm[r][c] += self.adjust_dict[(r, c)]

    def calc_new_fare(self):
        '''计算新的运输矩阵的总运费'''
        fare = 0
        for r in range(len(self.new_tm)):
            for c in range(len(self.new_tm[0])):
                fare += self.new_tm[r][c] * self.fm[r][c]
        self.fare = fare

    def solve(self):
        '''运行整个闭回路法，接收Exception错误，并停止程序'''
        try:
            self.find_close_loop()
            # print 'go path: {}'.format(self.go_path)
            self.go_path_drop_non()
            # print 'go path: {}'.format(self.go_path)
            self.examine_adjust_dict()
            self.create_new_transport_matrix()
            self.calc_new_fare()
        except Exception as e:
            print e
            sys.exit(1)


def show_matrix(matrix):
    '''展示矩阵'''
    string = list(map(str, matrix))
    res = '\n'.join(string)
    return res


def dataset(v=0):
    '''可供测试的数据集'''
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
        c = [3, 12, 3, 4, 11, 2, 5, 9, 6, 7, 1, 5]
        a = [8, 5, 9]
        b = [8, 4, 6, 7]
        '''
        result
        [8, 0, 0, 0]
        [0, 4, 0, 1]
        [0, 0, 6, 3]
        '''
    elif v == 2:
        # produce > sale
        c = [1, 2, 3, 6, 5, 4]
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
        c = [3, 11, 3, 10, 1, 9, 2, 8, 7, 4, 10, 5]
        a = [7, 4, 9]
        b = [3, 6, 5, 6]
        '''
        result
        [0, 0, 5, 2]
        [3, 0, 0, 1]
        [0, 6, 0, 3]
        '''
    elif v == 4:
        # product < sale
        # need to optimize
        c = [22, 92, 22, 33, 91, 35, 2, 56, 13, 40, 52, 20,
             3, 65, 97, 86, 46, 76, 39, 44, 80, 54, 7, 55]
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
    elif v == 5:
        # product < sale
        c = [40, 24, 54, 67, 91, 88, 49, 98]
        a = [90, 16]
        b = [18, 33, 79, 36]
    elif v == 6:
        # product < sale
        # need to optimize
        c = [60, 43, 50, 8, 27, 16, 78, 52, 40, 46, 28, 33, 17, 7, 45, 81, 59, 67,
             35, 62, 94, 72, 58, 90, 18, 65, 10, 41, 39, 90, 28, 51, 68, 26, 73, 72]
        a = [70, 61, 22, 32, 70, 94]
        b = [70, 99, 4, 85, 17, 82]
        '''
        result
        [0, 0, 0, 32, 0, 38]
        [0, 0, 0, 0, 17, 44]
        [0, 22, 0, 0, 0, 0]
        [4, 28, 0, 0, 0, 0]
        [66, 0, 4, 0, 0, 0]
        [0, 41, 0, 53, 0, 0]
        '''
    elif v == 7:
        # product < sale
        c = [86, 97, 94, 71, 29, 29, 73, 72, 11, 20, 36,
             91, 6, 42, 44, 2, 32, 59, 64, 76, 31, 6, 38, 14]
        a = [47, 16, 36, 59]
        b = [24, 15, 2, 67, 41, 28]
        '''
        result
        [0, 0, 0, 0, 41, 6]
        [0, 0, 2, 14, 0, 0]
        [24, 0, 0, 12, 0, 0]
        [0, 0, 0, 41, 0, 18]
        '''
    elif v == 8:
        c = [8, 11, 16, 90, 2, 80, 75, 84, 42, 40, 23, 68, 7, 64, 18, 40]
        a = [73, 47]
        b = [60, 85, 35, 2, 73, 78, 46, 84]
        '''
        result
        [47, 0, 0, 0, 26, 0, 0, 0]
        [0, 0, 0, 0, 47, 0, 0, 0]
        '''
    return c, a, b


def test_min():
    '''测试最小元素法'''
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
    '''测试位势法'''
    c, a, b = dataset(3)
    me = MinimumElement(c, a, b)
    me.solve()
    me.calc_fare()
    print 'fare: {}'.format(me.fare)
    _ct = copy.copy(me.ct)
    _cf = copy.copy(me.cf)
    exm = Examine(_ct, _cf)
    error_index = exm.solve_examine()
    print 'fare matrix:\n{}'.format(show_matrix(_cf))
    print 'transport matrix:\n{}'.format(show_matrix(_ct))
    print 'examine matrix:\n{}'.format(show_matrix(exm.em))
    print 'ap: {}'.format(exm.ap)
    print 'bp: {}'.format(exm.bp)


def test_closed():
    '''测试闭回路法'''
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
        cl.go_path_drop_non()
        print 'go path: {}'.format(cl.go_path)
        cl.create_unit()
        cl.make_adjust_dict()
        cl.create_new_transport_matrix()
        print 'new transport matrix:\n{}'.format(show_matrix(cl.new_tm))
        cl.calc_new_fare()
        print 'fare: {}'.format(cl.fare)


def main():
    '''运行整个表上作业法'''
    c, a, b = dataset(8)
    me = MinimumElement(c, a, b)
    print 'fare matrix:\n{}'.format(show_matrix(me.c))
    me.solve()
    me.calc_fare()
    me_fare = me.fare
    print 'final min transport matrix:\n{}'.format(show_matrix(me.final_ct))
    print 'fare: {}'.format(me.fare)
    _ct = me.ct
    _fm = me.cf
    print 'min transprot matrix:\n{}'.format(show_matrix(_ct))
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
    # test_min()
    main()
    # test_examine()
    # test_closed()
