import matplotlib.pylab as plt  # 绘制图形
import numpy as np
from numpy.fft import fft,ifft, fftfreq, fftshift
import datetime
E = 1
tao = 1
sample_freq = 2048  # 采样频率
sample_interval = 1 / sample_freq  # 采样间隔v
T = 5  # 实际是半个周期
tao = 1  # 脉冲宽度
# 定义区间
t = np.arange(0, 5 * tao, sample_interval)
# 定义时域信号：门函数
ft = E * np.heaviside(t, 1) - E * np.heaviside(t - 2*tao, 1)
# 定义时域信号：指数函数
ft1 = tao * np.exp(-tao*3 * t)

t1 = datetime.datetime.now()
rt = np.convolve(ft, ft1, mode='full') * sample_interval
t2 = datetime.datetime.now()
print("时域卷积运算时间：", t2 - t1)
# ------------------
'''计算FFT'''
# 注意所有的频轴用的都是一个，因为他们的时间轴和采样密度等是一样的
# 如果卷积时采用了full模式，则时轴发生变化，频轴也要重新计算
t1 = datetime.datetime.now()
f = fftshift(fftfreq(len(t), sample_interval))  # fft的双边频域坐标
Fw = fftshift(fft(ft))
Fw1 = fftshift(fft(ft1))
rx=Fw * Fw1
rxt=ifft(fftshift(rx))
t2 = datetime.datetime.now()
print("FFT运算时间：", t2 - t1)

# 绘图
plt.rcParams['mathtext.fontset'] = 'stix'  # 公式字体风格
plt.rcParams['font.sans-serif'] = ['SimSun']  # 指定非衬线字体
plt.rcParams['axes.unicode_minus'] = False  # 解决图像中的负号'-'显示为方块的问题


plt.grid()  # 显示网格
plt.xlim(0, 5)
plt.plot(t, rxt, 'darkviolet')

plt.suptitle("时域卷积定理验证")
plt.tight_layout()  # 紧凑布局，防止标题重叠
plt.show()
exit()
