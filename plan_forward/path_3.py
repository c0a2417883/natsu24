import planning_casadi as pl
from planning_casadi import Wall
import os
import numpy as np

# 始点
start = [1.8, 3.235, 0.0]

# 終点
end = [0.35, 0.600, -np.pi]

# 最大加速度
max_a = 3.0

# ロボットの大きさ
robot_edge = 0.65

# 半径
wheel_base = 0.25

# 経路点の数
N = 100

# 前回の初期値
pre_path = os.path.join(os.path.dirname(__file__), "output", "X3.npz")

# 角度最低値
angle_min = None

# 角度最高値
angle_max = None

# 最高角速度
vt_max = None

# 考慮する壁
walls = []
# 横壁
walls.append(Wall(0, 1.276, 2.538, 2.538))
walls.append(Wall(0.9, 2.176, 1.538, 1.538))

# 縦壁
walls.append(Wall(0, 0, 0, 3.6))
walls.append(Wall(2.176, 2.176, 0, 2.576))

pl.planning(start, end, max_a, robot_edge, angle_min, angle_max, vt_max, wheel_base, walls, N, pre_path)


pl.plot(pre_path)