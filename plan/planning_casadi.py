from casadi import *
import matplotlib.pyplot as plt
import numpy as np

class Wall:
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

'''
start: 始点
end: 終点
max_v: 最大速度
max_a: 最大加速度
robot_edge: ロボットの大きさ
wheel_base: ロボットの中心からタイヤまでの距離
wall: 考慮する壁
N: 経路点数
pre_path: 前の計算結果
'''
def planning(start:list, end:list, max_a:float, robot_edge:float, angle_min:float, angle_max:float, vt_max:float, wheel_base:float, walls:list, N:int, pre_path:str):
    opti = Opti()

    # 状態量 x, y, t, vx, vy, omega
    X = opti.variable(6,N+1)
    x = X[0,:]
    y = X[1,:]
    t = X[2, :]
    vx = X[3, :]
    vy = X[4, :]
    vt = X[5, :]

    # 入力
    U = opti.variable(3,N)
    ax = U[0, :]
    ay = U[1, :]
    at = U[2, :]

    # 終端時間
    T = opti.variable()

    # 時間を最小化する
    opti.minimize(T)

    # 微小時間
    dt = T/N

    # 移動による拘束条件
    for k in range(N):
        opti.subject_to(x[k+1]==x[k] + dt*vx[k])
        opti.subject_to(y[k+1]==y[k] + dt*vy[k])
        opti.subject_to(t[k+1]==t[k] + dt/wheel_base*vt[k])
        opti.subject_to(vx[k+1]==vx[k] + dt*ax[k])
        opti.subject_to(vy[k+1]==vy[k] + dt*ay[k])
        opti.subject_to(vt[k+1]==vt[k] + dt*at[k])

    # ロボットの大きさ
    robot_2 = robot_edge / 2
    robot2 = (robot_edge / 2) **2
    robot_edges = np.array([[robot_2, robot_2], [-robot_2, robot_2], [-robot_2, -robot_2], [robot_2, -robot_2]])

    # 経路の範囲
    opti.subject_to(opti.bounded(-np.pi, t, np.pi))

    # 障害物
    c = cos(t)
    s = sin(t)

    robot_edge_1 = [x + c * robot_edges[0, 0] - s * robot_edges[0, 1], y + s * robot_edges[0, 0] + c * robot_edges[0, 1]]
    robot_edge_2 = [x + c * robot_edges[1, 0] - s * robot_edges[1, 1], y + s * robot_edges[1, 0] + c * robot_edges[1, 1]]
    robot_edge_3 = [x + c * robot_edges[2, 0] - s * robot_edges[2, 1], y + s * robot_edges[2, 0] + c * robot_edges[2, 1]] 
    robot_edge_4 = [x + c * robot_edges[3, 0] - s * robot_edges[3, 1], y + s * robot_edges[3, 0] + c * robot_edges[3, 1]]

    def hlines(y, x_min, x_max, edge1, edge2):
        a1 = edge1[0] - edge2[0]
        b1 = edge1[1] - edge2[1]
        s1 = a1 * (y-edge1[1]) - b1*(x_min-edge1[0])
        t1 = a1 * (y-edge1[1]) - b1*(x_max-edge1[0])
        s2 = edge1[1] - y
        t2 = edge2[1] - y
        opti.subject_to(fmax(s1*t1, s2*t2) > 0)
        
    def vlines(x, y_min, y_max, edge1, edge2):
        a1 = edge1[0] - edge2[0]
        b1 = edge1[1] - edge2[1]
        s1 = a1 * (y_min-edge1[1]) - b1*(x-edge1[0])
        t1 = a1 * (y_max-edge1[1]) - b1*(x-edge1[0])
        s2 = edge1[0] - x
        t2 = edge2[0] - x
        opti.subject_to(fmax(s1*t1, s2*t2) > 0)
        
    for wall in walls:
        if wall.y1 == wall.y2:
           # 水平の壁
            hlines(wall.y1, wall.x1, wall.x2, robot_edge_1, robot_edge_2)
            hlines(wall.y1, wall.x1, wall.x2, robot_edge_2, robot_edge_3)
            hlines(wall.y1, wall.x1, wall.x2, robot_edge_3, robot_edge_4)
            hlines(wall.y1, wall.x1, wall.x2, robot_edge_4, robot_edge_1)
        else:
            # 垂直の壁
            vlines(wall.x1, wall.y1, wall.y2, robot_edge_1, robot_edge_2)
            vlines(wall.x1, wall.y1, wall.y2, robot_edge_2, robot_edge_3)
            vlines(wall.x1, wall.y1, wall.y2, robot_edge_3, robot_edge_4)
            vlines(wall.x1, wall.y1, wall.y2, robot_edge_4, robot_edge_1)

    # 速度の制約
    #opti.subject_to(opti.bounded(-9, vx**2 + vy**2, 9))
    # 加速度の制約
    opti.subject_to(opti.bounded(-max_a**2, ax**2 + ay**2 + at**2, max_a**2))

    # 初期条件
    opti.subject_to(x[0]==start[0])
    opti.subject_to(y[0]==start[1])
    opti.subject_to(t[0]==start[2])
    opti.subject_to(vx[0]==0)
    opti.subject_to(vy[0]==0)
    opti.subject_to(vt[0]==0)
    if angle_min != None:
        opti.subject_to(t >= angle_min)
    if angle_max != None:
        opti.subject_to(t <= angle_max)
    #opti.subject_to(ax[0]==0)
    #opti.subject_to(ay[0]==0)

    # 終端条件
    opti.subject_to(vx[-1]==0)
    opti.subject_to(vy[-1]==0)
    opti.subject_to(vt[-1]==0)
    #opti.subject_to(ax[-1]==0)
    #opti.subject_to(ay[-1]==0)
    opti.subject_to(x[-1]==end[0])
    opti.subject_to(y[-1]==end[1])
    opti.subject_to(t[-1]==end[2])
    if vt_max != None:
        opti.subject_to(opti.bounded(-vt_max, vt, vt_max))
    
    # 時間的拘束
    opti.subject_to(opti.bounded(2.0, T, 3.6))
    #opti.subject_to(T > 1)

    # 初期値入力
    if os.path.isfile(pre_path):
        pre_data = np.load(pre_path)
        opti.set_initial(X, pre_data['X'])
        opti.set_initial(U, pre_data['U'])
        opti.set_initial(T, pre_data['T'])
    else:
        opti.set_initial(T, 3.0)

    opti.solver("ipopt")
    sol = opti.solve()
    
    # 結果を保存
    np.savez_compressed(pre_path, X=sol.value(X), U=sol.value(U), T=sol.value(T))
        
def plot(pre_path):
    pre_data = np.load(pre_path)
    X = pre_data['X']
    U = pre_data['U']
    T = pre_data['T']
    
    # 状態量 x, y, t, vx, vy, omega
    x = X[0,:]
    y = X[1,:]
    t = X[2, :]
    vx = X[3, :]
    vy = X[4, :]
    vt = X[5, :]

    # 入力
    ax = U[0, :]
    ay = U[1, :]
    at = U[2, :]
    # 表示
    def plotMap():
        # 横線 (板の中心のy, xmin, xmax)
        ax1.hlines(-0.019, 0, 3.481, color='k')
        ax1.hlines(1.519, 0.9, 2.176, color='k')
        ax1.hlines(2.557, 0, 1.276, color='k')
        ax1.hlines(3.6445, 0, 2.743, color='k')
        ax1.hlines(0.7, 2.743, 3.443, color='k')

        # 縦線 (板の中心のx, ymin, ymax)
        ax1.vlines(-0.019, 0, 3.6, color='k')
        ax1.vlines(3.462, 0, 3.6, color='k')
        ax1.vlines(0.719, 0, 0.5, color='k')
        ax1.vlines(1.457, 0, 0.5, color='k')
        ax1.vlines(2.195, 0, 2.576, color='k')
        ax1.vlines(2.743, 0, 0.7, color='k')
    fig = plt.figure(figsize=(3.5*3*2, 3.6*2))
    ax1 = fig.add_subplot(1, 3, 1)
    ax2 = fig.add_subplot(1, 3, 2)
    ax3 = fig.add_subplot(1, 3, 3)
    plotMap()
    ax1.plot(x,y, label="path")
    ax1.legend(loc="upper left")
    ax1.set_xlim((0, 3.5))
    ax1.set_ylim((0, 3.6))

    ax2.plot(vx, label="vx")
    ax2.plot(vy, label="vy")
    ax2.plot(vt, label="vt")
    ax2.plot(t, label="t")
    ax2.legend(loc="upper left")

    ax3.plot(ax, label="ax")
    ax3.plot(ay, label="ay")
    ax3.plot(at, label="at")
    ax3.legend(loc="upper left")

    fig.suptitle(f'time: {T:.3}s')
    plt.savefig(os.path.join(os.path.dirname(__file__), "output", "X1.png"), format="png", dpi=300)
    plt.show()