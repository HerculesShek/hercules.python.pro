#-*- coding: utf-8 -*-
import time 
'''钢条切割问题的自顶向下版本，直接进行递归
   p是长度对应的价格表
   n是现在的钢条长度
   求解最大利润'''
def CUT_ROD(p, n):
    if n is 0:
        return 0
    q = 0
    for i in xrange(1, n+1):
        q = max(q, p[i]+CUT_ROD(p, n-i))
    return q

p = {0:0,1:1,2:5,3:8,4:9,5:10,6:17,7:17,8:20,9:24,10:30}
def main():
    n = 24
    max_key = max(p.keys())
    if n > max_key:
        for i in xrange(max_key+1, n+1):
            p[i] = 0        #原来的没有p[i]，否则报keyerror
            p[i] = CUT_ROD(p, i)
    print n, p[n]
    
if __name__ == '__main__':
    begin = time.time()
    main()
    print 'total run time', time.time()-begin
