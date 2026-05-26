import os
import numpy as np

PATH_NUM = 4
MIN_V = 0.5

PATH_SIZE = 100

SAVE_HEADER_PATH_1 = os.path.join(os.path.dirname(__file__), "..", "include", "natsu24", 'Path.h')
SAVE_HEADER_PATH_2 = os.path.join(os.path.dirname(__file__), "..", "gr-sakura", "natsu24", 'Path.h')

out = "#pragma once\n\n"

for path_i in range(PATH_NUM):
    
    PRE_PATH = os.path.join(os.path.dirname(__file__), "output", f'X{path_i}.npz')
    pre_data = np.load(PRE_PATH)
    X = pre_data['X']
    
    path_x = X[0,:]
    path_y = X[1,:]
    path_t = X[2,:]
    path_v = np.hypot(X[3,:].T, X[4, :].T)
    
    out = out + 'float _x'+str(path_i)+'[] = {'
    for x in path_x:
        out = out + f'{x:.3}, '
    out = out + '};\nfloat _y'+str(path_i)+'[] = {'
    for y in path_y:
        out = out + f'{y:.3}, '
    out = out + '};\nfloat _t'+str(path_i)+'[] = {'
    for t in path_t:
        out = out + f'{t:.3}, '
    out = out + '};\nfloat _v'+str(path_i)+'[] = {'
    for v in path_v:
        out = out + f'{max(v, MIN_V):.3}, '
    out = out + '};\n'
        

out = out + '\nfloat *_plan[][4] = {'
for i in range(PATH_NUM):
    out = out + "{_x"+str(i)+", _y"+str(i)+", _t"+str(i)+", _v"+str(i)+"}, "
out = out + "};"

out = out + '\nint _plan_size[] = {'
for i in range(PATH_NUM):
    out = out + f'{PATH_SIZE+1}, '
out = out + "};"

with open(SAVE_HEADER_PATH_1, mode='w') as f:
    f.write(out)
    
with open(SAVE_HEADER_PATH_2, mode='w') as f:
    f.write(out)

print(out)