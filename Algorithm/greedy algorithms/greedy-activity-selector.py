# -*- coding: utf-8 -*-
import time, sys

# a(activity)代表所有活动的开始时间和结束时间
a = [[5,7],[1,4],[3,5],[0,6],[3,9],[5,9],[6,10],[8,11],[8,12],[2,14],[12,16]]
# 首先对a 按照活动的结束时间进行单调递增的排序
a = sorted(a, key=lambda e:e[1])

def greedy_activity_selector(s, f):
    n = len(s)
    A = [a[0]]              # 由于已经排好序，直接加入第一个没错
    k=0                     # k用来记录最近加入集合A的活动的下标
    for m in xrange(1, n):  # 因为已经按照结束时间递增排序，所以只要一次向后遍历就行了
        if s[m]>=f[k]:      # 一旦和上次加入的活动没有交集即可， hit it!
            A.append(a[m])
            k = m           # 重置k        
    return A

def main():
    s, f = [e[0] for e in a], [e[1] for e in a]
    r = greedy_activity_selector(s, f)
    print r

if __name__ == '__main__':
    main()
