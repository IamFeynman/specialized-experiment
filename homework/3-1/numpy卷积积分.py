import datetime
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sgn
from numpy.fft import fftfreq, fftshift, fft, ifft

# 公共参数
E = 1
tao = 1
sample_freq = 2048  # 采样频率
sample_interval = 1 / sample_freq  # 采样间隔v
# 时间轴
t = np.arange(0, 5 * tao, sample_interval)
# 定义时域信号：门函数
ft = E * np.heaviside(t, 1) - E * np.heaviside(t - 2*tao, 1)
# 定义时域信号：指数函数
ft1 = tao * np.exp(-tao*3 * t)


#裁切之后，实际只剩下从时间从1到3的数据

r1 = np.convolve(ft, ft1, mode='same') * sample_interval
#此时卷积范围应该是0到4，但实际有效数据是从0到2，从2到4是全零的
t1 = datetime.datetime.now()
r2 = np.convolve(ft, ft1, mode='full') * sample_interval
r2 = r2[:len(t)]#把后面的零裁切掉
t2 = datetime.datetime.now()
print("FFT运算时间：", t2 - t1)
plt.rcParams['font.serif'] = ['SimSun']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决图像中的负号'-'显示为方块的问题
plt.figure()
plt.subplot(2, 2, 1)  # 画布位置1
plt.title("e(t)", loc='left')
plt.plot(t, ft, c='r')
plt.grid()

plt.subplot(2, 2, 2)
plt.title("h(t)", loc='left')
plt.plot(t, ft1, c='g')
plt.grid()

plt.subplot(2,2, 3)
plt.title("r(t)-same mode", loc='left')
plt.plot(t, r1, c='purple')
plt.grid()

plt.subplot(2, 2, 4)
plt.title("r(t)-full mode", loc='left')
plt.plot(t, r2, c='purple')
plt.grid()
plt.tight_layout()  # 紧凑布局，防止标题重叠
plt.show()
