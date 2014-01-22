import time

groups = []
items = []
for i in xrange(20):
    for j in xrange(200):
        groups.append((i,j))
        for m in xrange(30):
            items.append((i,j,m))

begin = time.time()
for g in groups:
    t = sorted((elem for elem in items
                if elem[0] is g[0] and elem[1] is g[1]), key = lambda e:e[2])

end = time.time()
print 'total run time is', (end - begin)
