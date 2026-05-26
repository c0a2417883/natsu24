import planning_casadi as pl
from planning_casadi import Wall
import os
import numpy as np

# 始点
start = [3.218, 0.24, 0.0]

# 終点
end = [1.8, 3.235, 0.0]

# 最大加速度
max_a = 3.0

# ロボットの大きさ
robot_edge = 0.65

# 半径
wheel_base = 0.25

# 経路点の数
N = 100

# 前回の初期値
pre_path = os.path.join(os.path.dirname(__file__), "output", "X0.npz")

# 角度最低値
angle_min = - np.pi/4

# 角度最高値
angle_max = None

# 最高角速度
vt_max = 0.2

# 考慮する壁
walls = []
# 横壁
# 縦壁
walls.append(Wall(3.443, 3.443, 2.0, 3.6))
walls.append(Wall(2.214, 2.214, 0, 2.576))

pl.planning(start, end, max_a, robot_edge, angle_min, angle_max, vt_max, wheel_base, walls, N, pre_path)

pl.plot(pre_path)