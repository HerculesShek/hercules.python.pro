#-*- coding: utf8 -*-
import time 
''' “自顶向下”朴素递归带备忘 top-down with memoization 同时打印出解决方案'''
c = 1   #每次切割的成本c
def EXTENDED_MEMOIZED_CUT_ROD_WITH_COST(p, n):
    r, s = [], []      # r用来存储长度为n的最大收益，就是所有子问题的解
                        # 用来存储长为n的钢条切割最优解对应的第一段的切割的长度
    for i in xrange(0, n+1):    # 初始化r [0 to n]   r的长度是n+1
        r.append(-1)
        s.append(0)
    return EXTENDED_MEMOIZED_CUT_ROD_WITH_COST_AUX(p, n, r, s), s

def EXTENDED_MEMOIZED_CUT_ROD_WITH_COST_AUX(p, n, r, s):
    if r[n]>=0:
        return r[n]     #这里就是已经存在的长度为n的最大收益，如果存在则直接取出，不再计算
    if n is 0:
        q = 0
    else:
        q = -1
        for i in xrange(1, n+1):    # 1 to n
            if q < p[i] + EXTENDED_MEMOIZED_CUT_ROD_WITH_COST_AUX(p, n-i, r, s):
                q = p[i] + EXTENDED_MEMOIZED_CUT_ROD_WITH_COST_AUX(p, n-i, r, s)
                s[n] = i
    if s[n]==n:
        r[n]=q
    else:
        r[n]=q-c
    
    return r[n]

def PRINT_CUT_ROD_SOLUTION(p, n):
    q, s = EXTENDED_MEMOIZED_CUT_ROD_WITH_COST(p, n)
    print 'max revenue is', q
    while n>0:
        print s[n]
        n = n-s[n]

p = {0:0, 1:1, 2:5, 3:8, 4:9, 5:10, 6:17, 7:17, 8:20, 9:24, 10:30}
def main():
    n = 4
    max_key = max(p.keys())
    if n > max_key:
        for i in xrange(max_key+1, n+1):
            p[i] = 0        #原来的没有p[i]，否则报keyerror
    PRINT_CUT_ROD_SOLUTION(p, n)
    
if __name__ == '__main__':
    begin = time.time()
    main()
    print 'total run time', time.time()-begin
