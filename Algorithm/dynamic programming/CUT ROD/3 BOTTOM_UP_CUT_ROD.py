#-*- coding: utf8 -*-
import time 
''' 自底向上法 bottom-up method '''
def BOTTOM_UP_CUT_ROD(p, n):
    r = []          #用来存储长度为n的最大收益，就是所有子问题的最优解
    for i in xrange(0, n+1):    # 初始化r [0 to n]  长度是n+1
        r.append(-1)
    r[0] = 0        #长度为0, 收益为0, 遍历的基础 
    for j in xrange(1, n+1):
        q = -1
        for i in xrange(1, j+1):
            q = max(q, p[i]+r[j-i])
        r[j] = q
    return r[n]

p = {0:0,1:1,2:5,3:8,4:9,5:10,6:17,7:17,8:20,9:24,10:30}
def main():
    n = 800
    max_key = max(p.keys())
    if n > max_key:
        for i in xrange(max_key+1, n+1):
            p[i] = 0        #原来的没有p[i]，否则报keyerror
    print BOTTOM_UP_CUT_ROD(p, n)
    
if __name__ == '__main__':
    begin = time.time()
    main()
    print 'total run time', time.time()-begin
