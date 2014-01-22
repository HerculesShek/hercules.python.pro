#-*- coding: utf8 -*-
import time
'''计算第n个斐波那契数 自底向上的动态规划方式'''
f = {1:1, 2:1}
def fibo(n):    
    if f.has_key(n):
        return f[n]
    for i in xrange(3, n+1):
        f[i] = f[i-1]+f[i-2]
    return f[n]

def main():
    n=900
    print fibo(n)

if __name__ == '__main__':
    begin = time.time()
    main()
    print 'total run time is', time.time()-begin
    
