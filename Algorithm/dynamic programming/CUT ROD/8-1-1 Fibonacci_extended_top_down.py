#-*- coding: utf8 -*-
import time
'''计算第n个斐波那契数 普通递归方式 进行动态规划的改进'''
f = {1:1, 2:1}
def fibo(n):    
    if f.has_key(n):
        return f[n]
    f[n] = fibo(n-1)+fibo(n-2)
    return f[n]

def main():
    n=900
    print fibo(n)

if __name__ == '__main__':
    begin = time.time()
    main()
    print 'total run time is', time.time()-begin
    
