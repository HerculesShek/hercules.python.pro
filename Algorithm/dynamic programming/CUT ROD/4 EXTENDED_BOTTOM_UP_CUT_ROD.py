#-*- coding: utf8 -*-
import time 
''' 输出最优解的自底向上法 bottom-up method '''
def EXTENDED_BOTTOM_UP_CUT_ROD(p, n):
    r, s = [], []   # r用来存储长度为n的最大收益，就是所有子问题的最优解
                    # s存储对长度为n的钢条切割的最优解对应的第一段钢条的切割长度，这个地方很精妙
                    # 主要是抓住了子问题的关键结构
    
    for i in xrange(0, n+1):    # 初始化  [0 to n] 
        r.append(-1)
        s.append(0)
    r[0] = 0        #长度为0， 收益为0
    for j in xrange(1, n+1):
        q = -1
        for i in xrange(1, j+1):
            if q < p[i]+r[j-i]:
                q = p[i]+r[j-i]
                s[j] = i
        r[j] = q
    return r, s

def PRINT_CUT_ROD_SOLUTION(p, n):
    r, s = EXTENDED_BOTTOM_UP_CUT_ROD(p, n)
    print 'max revenue is', r[n]
    while n>0:
        print s[n]
        n = n-s[n]

p = {0:0, 1:1, 2:5, 3:8, 4:9, 5:10, 6:17, 7:17, 8:20, 9:24, 10:30}
def main():
    n = 14
    max_key = max(p.keys())
    if n > max_key:
        for i in xrange(max_key+1, n+1):
            p[i] = 0        #原来的没有p[i]，否则报keyerror
    PRINT_CUT_ROD_SOLUTION(p, n)
    
if __name__ == '__main__':
    begin = time.time()
    main()
    print 'total run time', time.time()-begin
