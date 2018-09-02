# -*- coding: utf-8 -*-

def create_directions():
    global directions
    up = lambda x, y: (x - 1, y)
    down = lambda x, y: (x + 1, y)
    left = lambda x, y: (x, y - 1)
    right = lambda x, y: (x, y + 1)
    directions = [up, down, left, right]

def arrival_boundary(matrix, index):
    rows = len(matrix); columns = len(matrix[0])
    r, c = index
    if r < 0 or r >= rows or c < 0 or c >= columns:
        return True
    else:
        return False

def backward(enter_index, outer_index):
    _er, _ec = enter_index
    _or, _oc = outer_index
    if _ec == _oc:
        code = 0 if _er > _or else 1
    else:
        code = 2 if _ec > _oc else 3
    return code

def forward(matrix, index, enter):
    enter_op = {1:0, 0:1, 2:3, 3:2}
    _path = []
    if enter != None:
        if matrix[index[0]][index[1]] == 0:
            if not arrival_boundary(matrix, directions[enter](*index)):
                _path.append(directions[enter](*index))
                #print 'add {}'.format(self.directions[enter](*index))
        else:
            temp = [_ for _ in range(4) if _ != enter_op[enter]]
            #temp = [2, 3] if enter <= 1 else [0, 1]
            for d in temp:
                if not arrival_boundary(matrix, directions[d](*index)):
                    _path.append(directions[d](*index))
    else:
        for func in directions:
            if not arrival_boundary(matrix, func(*index)):
                _path.append(func(*index))
    return _path

def go(node):
    print '{} -> {}'.format(node[0], node[1])
    if node[1] == []:
        return False
    if optimize_index not in node[1]:
        for i, j in node[1]:
            print 'code: {}'.format(backward(node[0], (i, j)))
            print 'enter: {}'.format((i, j))
            forward_path = forward(tm, index=(i, j), enter=backward(node[0], (i, j)))
            if forward_path:
                if go([(i, j), forward_path]):
                    go_path.append((i, j))
                    return True
            else:
                print 'over'
                return False
    else:
        return True

def show_matrix(matrix): 
    string = list(map(str, matrix))
    res = '\n'.join(string)
    return res

tm = [[0, 0, 12, 13]]

# optimize_index = (2, 1)

# print show_matrix(tm)
# create_directions()
# go_path = [optimize_index]
# go([go_path[0], forward(tm, optimize_index, enter=None)])
# print 'go path: {}'.format(go_path)


