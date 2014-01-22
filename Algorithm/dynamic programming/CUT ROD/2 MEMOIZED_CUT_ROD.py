#-*- coding: utf8 -*-
import time 
''' “自顶向下”朴素递归带备忘 top-down with memoization '''
def MEMOIZED_CUT_ROD(p, n):
    r = []      #用来存储长度为n的最大收益，就是所有子问题的解
    for i in xrange(0, n+1):    # 初始化r [0 to n]   r的长度是n+1
        r.append(-1)
    return MEMOIZED_CUT_ROD_AUX(p, n, r)

def MEMOIZED_CUT_ROD_AUX(p, n, r):
    if r[n]>=0:
        return r[n]     #这里就是已经存在的长度为n的最大收益，如果存在则直接取出，不再计算
    if n is 0:
        q = 0
    else:
        q = -1
        for i in xrange(1, n+1):    # 1 to n
            q = max(q, p[i] + MEMOIZED_CUT_ROD_AUX(p, n-i, r))
    r[n]=q
    return q
    
p = {0:0, 1:1, 2:5, 3:8, 4:9, 5:10, 6:17, 7:17, 8:20, 9:24, 10:30}
def main():
    n = 800
    max_key = max(p.keys())
    if n > max_key:
        for i in xrange(max_key+1, n+1):
            p[i] = 0        #原来的没有p[i]，否则报keyerror
    print MEMOIZED_CUT_ROD(p, n)
    
    
if __name__ == '__main__':
    begin = time.time()
    main()
    print 'total run time', time.time()-begin
