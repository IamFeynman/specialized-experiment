import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# 设置频率和幅值
frequency = 5
amplitude = 2

# X轴上产生0-1，0.001为间隔的矩阵
axisX = np.arange(0, 2, 0.001)

# 产生方波，axisY为方便数据存储数组
period = 1.0 / frequency
t = np.linspace(0, 2, 1000, endpoint=False)
axisY = amplitude * signal.square(2 * np.pi * frequency * axisX)
print(axisY)

# 使用time计算周期和频率
# 寻找信号上升沿和下降沿的位置
rising_edges = np.where(np.diff(axisY > 0) == 1)[0]
falling_edges = np.where(np.diff(axisY > 0) == -1)[0]

# 确保信号至少有一个完整的周期
if len(rising_edges) > 0 and len(falling_edges) > 0:
    # 确保边缘数量相同
    min_len = min(len(rising_edges), len(falling_edges))
    rising_edges = rising_edges[:min_len]
    falling_edges = falling_edges[:min_len]

    # 计算信号周期
    periods = t[falling_edges] - t[rising_edges]

    # 计算平均周期
    mean_period = np.mean(periods)
    print("平均周期:", mean_period, "秒")
else:
    print("信号周期太短，无法计算平均周期。")


# 绘图
plt.rcParams['mathtext.fontset'] = 'stix'  # 公式字体风格
plt.rcParams['font.sans-serif'] = ['SimSun']  # 指定非衬线字体
plt.rcParams['axes.unicode_minus'] = False  # 解决图像中的负号'-'显示为方块的问题

plt.plot(axisX, axisY)
plt.xlabel('时间')
plt.ylabel('幅值')
plt.title('方波')

plt.grid(True)

# plt.show
plt.show()
# 上述方法我们使用数组来产生一个方波，方波的频率比较低