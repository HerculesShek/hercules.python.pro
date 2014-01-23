# -*- coding: utf-8 -*-
import time, sys

# a(activity)代表所有活动的开始时间和结束时间
a = [[5,7],[1,4],[3,5],[0,6],[3,9],[5,9],[6,10],[8,11],[8,12],[2,14],[12,16]]
# 首先对a 按照活动的结束时间进行单调递增的排序
a = sorted(a, key=lambda e:e[1])
a.insert(0, [-1,0])

def recurisive_activity_selector(s, f, k, n):   # n是所有活动的个数，就是a的长度
                                                # k是上次选上的活动的索引，从1开始计数，因此就要在a的最前面加一个虚拟活动形成a[0]
                                                # 让a[0]的结束时间为0，否则 s[m]<f[k] 无法进行判断， 但是这里传入的n不用加1
    m = k+1
    while m<=n and s[m]<f[k]:
        m = m+1
    if m<=n:
        r = recurisive_activity_selector(s, f, m, n)
        r.insert(0, a[m])
        return r
    else:
        return []
    
def main():
    s, f = [e[0] for e in a], [e[1] for e in a]
    r = recurisive_activity_selector(s, f, 0, len(a)-1)
    print r

if __name__ == '__main__':
    main()
