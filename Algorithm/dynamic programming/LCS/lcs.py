# -*- coding: utf-8 -*-
import time
gk = lambda i,j:str(i)+','+str(j)

def LSC_length(x, y):
    m = len(x)
    n = len(y)
    b, c = {}, {} # b用来存储解决的方案， c用来存储x序列前缀i和y序列前缀j对应的LCS的长度
    for i in xrange(0, m):
        c[gk(i, -1)] = 0
    for j in xrange(0, n):
        c[gk(-1, j)] = 0
    for i in xrange(0, m):
        for j in xrange(0, n):
            if x[i] == y[j]:
                c[gk(i, j)] = c[gk(i-1, j-1)]+1
                b[gk(i, j)] = 'hit'
            elif c[gk(i-1, j)] >= c[gk(i, j-1)]:
                c[gk(i, j)] = c[gk(i-1, j)]
                b[gk(i, j)] = "fromUp"
            else:
                c[gk(i, j)] = c[gk(i, j-1)]
                b[gk(i, j)] = "fromLeft"
    return c, b

def print_LCS(b, x, i, j):
    '''将b从最后一个元素顺着箭头往前数就会得到LCS的输出'''
    if i == -1 or j == -1:
        return
    if b[gk(i, j)] == 'hit':
        print_LCS(b, x, i-1, j-1)
        print x[i]
    elif b[gk(i, j)] == 'fromUp':
        print_LCS(b, x, i-1, j)
    else:
        print_LCS(b, x, i, j-1)


def test():
    x = ['a','b','c','b','d','a','b']
    y = ['b','d','c','a','b','a']
    c, b = LSC_length(x, y)
    print 'length of LSC of x and y is', c[gk(len(x)-1, len(y)-1)]
    print_LCS(b, x, len(x)-1, len(y)-1)
    
if __name__ == '__main__':
    begin = time.time()
    test()
    print 'total runtime is', time.time()-begin
