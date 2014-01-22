#-*- coding: utf-8 -*-
import sys, time
gk = lambda i,j:str(i)+','+str(j)

def optimal_BST(p, q, n):   #p是关键字的概率(n个)， q是伪关键字的概率(n+1个)， n是关键字的个数
    MAX = (max(p)>max(q) and max(p) or max(q))*(n+1)*(len(p)+len(q))  #设置最大值 取出p和q中的最大的一个概率值，
                                                                      #乘以n+1(深度)，共有len(p)+len(q)个节点，
                                                                      #树的搜索期望不可能比这个值大
    e, w, root = {}, {}, {} #e存放期望 w存放概率和 root存放子树的根节点
    for i in xrange(1, n+2): #初始化e和w i属于[1,n+1]
        e[gk(i, i-1)] = q[i-1]
        w[gk(i, i-1)] = q[i-1]
    for l in xrange(1, n+1):   #l代表的是字数的长度 l属于[1,n]
        for i in xrange(1, n-l+2): # i是长度为l的每个子树的关键字的最小的索引值 i属于[1,n-l+1]
            j = i+l-1        #i是子树关键字的开始处，j是结束处的坐标，关键的索引是从1开始的，而p是从0开始的，需要做+1操作
            e[gk(i, j)] = MAX
            w[gk(i, j)] = w[gk(i, j-1)]+p[j-1]+q[j]
            for r in xrange(i, j+1): #r属于[i,j]
                t = e[gk(i, r-1)]+e[gk(r+1, j)]+w[gk(i, j)]
                if t<e[gk(i, j)]:
                    e[gk(i, j)] = t
                    root[gk(i, j)] = r
    return e, root

def main():
    p = [0.15, 0.10, 0.05, 0.10, 0.20]
    q = [0.05, 0.10, 0.05, 0.05, 0.05, 0.10]
    e, root = optimal_BST(p, q, len(p))
    print e[gk(1,len(p))]
    
if __name__ == '__main__':
    main()
