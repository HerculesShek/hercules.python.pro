#-*- coding: utf8 -*-
import time
'''计算第n个斐波那契数最朴素的递归方式'''
def fibo(n):    
    if n == 1 or n == 2:
        return 1
    return fibo(n-1)+fibo(n-2)

def main():
    n=35
    fibo(n)

if __name__ == '__main__':
    begin = time.time()
    main()
    print 'total run time is', time.time()-begin
    
