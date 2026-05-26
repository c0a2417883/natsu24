from scipy import interpolate
import matplotlib.pyplot as plt
import numpy as np
import math

plan = [
    [
        [3.15, 0.35],
        [3.0, 2.0],
        [2.5, 3.1],
        [2.0, 3.2],
    ],
    [
        [2.0, 3.0],
        [1.9, 3.0],
        [1.7, 2.1],
        [0.9, 2.0],
        [0.5, 1.5],
        [0.6, 1.1],
        [1.7, 1.0],
        [1.74, 0.4],
        [1.75, 0.35],
    ],
    [
        [2.0, 3.0],
        [1.9, 3.0],
        [1.7, 2.1],
        [0.9, 2.0],
        [0.5, 1.5],
        [0.6, 1.1],
        [1.00, 1.0],
        [1.04, 0.4],
        [1.05, 0.35],
    ],
    [
        [2.0, 3.0],
        [1.9, 3.0],
        [1.7, 2.1],
        [0.9, 2.0],
        [0.35, 0.4],
        [0.35, 0.35],
    ]
]

def splineSplprep(x, y, ds, deg):
    s = 0
    for i in range(len(x)-1):
        s += math.hypot(x[i+1]-x[i], y[i+1]-y[i])
    tck,u = interpolate.splprep([x,y],k=deg,s=0)
    u = np.linspace(0,1,num=int(s/ds),endpoint=True) 
    spline = interpolate.splev(u,tck)
    return spline[0],spline[1]

def plotMap():
    # 横線
    plt.hlines(0, 0, 3.6, color='k')
    plt.hlines(1.5, 0.9, 2.1, color='k')
    plt.hlines(2.5, 0, 1.2, color='k')
    plt.hlines(3.6, 0, 3.6, color='k')
    plt.hlines(0.7, 2.8, 3.6, color='k')
    # 縦線
    plt.vlines(0, 0, 3.6, color='k')
    plt.vlines(3.6, 0, 3.6, color='k')
    plt.vlines(0.7, 0, 0.5, color='k')
    plt.vlines(1.4, 0, 0.5, color='k')
    plt.vlines(2.1, 0, 2.5, color='k')
    plt.vlines(2.8, 0, 0.7, color='k')

plan_size = []

for path_i, path in enumerate(plan):
    x = []
    y = []
    for p in path:
        x.append(p[0])
        y.append(p[1])
    

    path_x, path_y = splineSplprep(x, y, 0.1, 3)
    path_t = []
    for i in range(len(path_x)):
        path_t.append(0.0)
    plan_size.append(len(path_x))

    plotMap()
    plt.plot(x, y, 'ro',label="controlpoint")
    plt.plot(path_x,path_y, label="splineSplprep")
    plt.xlim([-0.5, 4.0])
    plt.ylim([-0.5, 4.0])
    plt.title("spline")
    plt.legend(loc='lower right')
    plt.show()
    plt.cla()
    
    print('float _x'+str(path_i)+'[] = {', end='')
    for x in path_x:
        print(f'{x:.3}, ', end='')
    print('};\nfloat _y'+str(path_i)+'[] = {', end='')
    for y in path_y:
        print(f'{y:.3}, ', end='')
    print('};\nfloat _t'+str(path_i)+'[] = {', end='')
    for t in path_t:
        print(f'{t:.3}, ', end='')
    print('};')
        

print('\nfloat *_plan[][3] = {', end='')
for i in range(len(plan)):
    print("{_x"+str(i)+", _y"+str(i)+", _t" + str(i) + "}, ", end='')
print("};")

print('\nint _plan_size[] = {', end='')
for path_size in plan_size:
    print(f'{path_size}, ', end='')
print("};")