import datetime
import matplotlib.pylab as plt  # 绘制图形
import numpy as np
from numpy.fft import fft, fftfreq, fftshift, ifft, ifftshift
import sounddevice as sd
import time

sample_freq = 102400  # 采样频率
sample_interval = 1 / sample_freq  # 采样间隔
f_l = 1000  # 截止频率单位是Hz，注意低通的总宽度实际是两倍，但带宽只算正半轴
''' ----------------------
第一部分：两种理想低通的定义方式
----------------------'''
'''定义t、f
把t的宽度加长到1000/f_l，或者适当增加sample_freq，使得总采样点数增加，
可以更好的看到视频域计算时间的差异。
'''
t = np.arange(0,1,sample_interval)
f = fftshift(fftfreq(len(t), sample_interval))
# ------------------
'''2,从频域定义理想低通'''
Hw2_amp =np.ones(102400)-( np.heaviside(f + f_l, 1) - np.heaviside(f - f_l, 1))
# 可以定义时延量
t0 = 0  # 0.05
Hw2 = Hw2_amp * np.exp(t0 * -1j * f * 2 * np.pi)
'''求ifft，得到应ht，
1. Hw2或Hw2_amp相当于进行过幅度修正和fftshift，因此要反向操作一下
2. 由于时域的t是个对称区间，因此要对ifft结果再进行一次ifftshift
3. 考虑到ifft的精度问题，可能得到的ht2不是纯实的，其结果可以取个实部
'''
ht2 = ifftshift(ifft(ifftshift(Hw2 / sample_interval))).real

# 参数

length = 1  # 时长s
sig = np.sin(2 * np.pi * 1250 *t)+np.sin(2 * np.pi * 750 *t)
sd.play(sig, sample_freq)  # 播放
time.sleep(length)

'''计算FFT'''
# 原信号频谱
sig_fft_amp = fftshift(np.abs(fft(sig)) * sample_freq)  # 双边幅度谱,范围为正负sample_freq/2

# 滤波后频谱
sig2_fft_amp= sig_fft_amp*Hw2

sig2 = ifftshift(ifft(ifftshift(sig2_fft_amp / sample_interval))).real
sd.play(sig2, sample_freq)  # 播放
time.sleep(length)
plt.rcParams['mathtext.fontset'] = 'stix'  # 公式字体风格
plt.rcParams['font.sans-serif'] = ['SimSun']  # 指定非衬线字体
plt.rcParams['axes.unicode_minus'] = False  # 解决图像中的负号'-'显示为方块的问题

plt.subplot(221)
plt.grid()  # 显示网格
plt.xlim(0, 0.01)
plt.title("原信号$($Sa$函数)", loc='left')
plt.xlabel(r'$time\rm{(s)}$', loc='right')
plt.plot(t, sig)
# 双边谱
plt.subplot(222)
plt.grid()  # 显示网格
plt.xlim(-2 * f_l, 2 * f_l)
plt.title("原信号频谱", loc='left')
plt.xlabel(r'$frequency\rm{(Hz)}$', loc='right')
plt.plot(f, sig_fft_amp)
plt.subplot(223)
plt.grid()  # 显示网格
plt.xlim(0, 0.01)
plt.title("滤波后信号$($Sa$函数)", loc='left')
plt.xlabel(r'$time\rm{(s)}$', loc='right')
plt.plot(t, sig2)
# 双边谱
plt.subplot(224)
plt.grid()  # 显示网格
plt.xlim(- 2 * f_l, 2 * f_l)
plt.title("滤波后信号频谱", loc='left')
plt.xlabel(r'$frequency\rm{(Hz)}$', loc='right')
plt.plot(f, sig2_fft_amp)

plt.tight_layout()  # 紧凑布局，防止标题重叠
plt.show()