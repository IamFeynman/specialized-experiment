import datetime
import numpy as np
import matplotlib.pyplot as plt
import sympy as sy
import scipy.signal as sgn

sample_freq = 4096  # 采样频率
sample_interval = 1 / sample_freq  # 采样间隔(deltaT)
T = 5 # 实际是半个周期
tao = 1  # 脉冲宽度

# 定义区间
t = np.linspace(-T, 2*T,  T * sample_freq)
#t = np.arange(-T,T+sample_interval,sample_interval)
# 定义e(t)和h(t)
x = np.piecewise(t, [t >= 0, t >= 5],[lambda t: t, 0])
h = np.piecewise(t, [t < 0, t >= 0, t > 5], [0, 1, 0])

# 对比：FFT卷积
r = np.convolve(x, h, mode='same') * sample_interval

plt.rcParams['font.serif'] = ['SimSun']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决图像中的负号'-'显示为方块的问题
plt.figure()
plt.subplot(2, 2, 1)  # 画布位置1
plt.title("x(t)", loc='left')
plt.plot(t, x, c='r')
plt.grid()

plt.subplot(2, 2, 2)
plt.title("h(t)", loc='left')
plt.plot(t, h, c='g')
plt.grid()

plt.subplot(2, 1, 2)
plt.title("r(t)", loc='left')

plt.plot(t, r, c='b')
plt.grid()

plt.tight_layout()  # 紧凑布局，防止标题重叠
plt.show()