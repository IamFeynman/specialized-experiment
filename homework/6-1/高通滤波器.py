import datetime
import matplotlib.pylab as plt  # 绘制图形
import numpy as np
from numpy.fft import fft, fftfreq, fftshift, ifft, ifftshift

sample_freq = 1024000  # 采样频率
sample_interval = 1 / sample_freq  # 采样间隔
f_l = 1000  # 截止频率单位是Hz，注意低通的总宽度实际是两倍，但带宽只算正半轴
''' ----------------------
第一部分：两种理想低通的定义方式
----------------------'''
'''定义t、f
把t的宽度加长到1000/f_l，或者适当增加sample_freq，使得总采样点数增加，
可以更好的看到视频域计算时间的差异。
'''
t = np.arange(-500 / f_l, 500/ f_l, sample_interval)
f = fftshift(fftfreq(len(t), sample_interval))
# ------------------
'''1,从时域定义理想低通
注意对照公式乘系数，使得频域门高度为1
'''
ht1 = 2 * f_l * np.sinc(2 * f_l * t)
'''求fft，得到幅度响应'''
Hw1 = (fftshift(fft(fftshift(ht1))) * sample_interval)
Hw1_amp = np.ones(1024000) - np.abs(Hw1)


plt.rcParams['mathtext.fontset'] = 'stix'  # 公式字体风格
plt.rcParams['font.sans-serif'] = ['SimSun']  # 指定非衬线字体
plt.rcParams['axes.unicode_minus'] = False  # 解决图像中的负号'-'显示为方块的问题

plt.subplot(211)
plt.grid()  # 显示网格
plt.xlim(-2 / f_l, 2 / f_l)
plt.title("在时域定义$h(t)$($Sa$函数)", loc='left')
plt.xlabel(r'$time\rm{(s)}$', loc='right')
plt.plot(t, ht1)
# 双边谱
plt.subplot(212)
plt.grid()  # 显示网格
plt.xlim(- 2 * f_l, 2 * f_l)
plt.title("通过$FFT$计算$H(jf)$", loc='left')
plt.xlabel(r'$frequency\rm{(Hz)}$', loc='right')
plt.plot(f, Hw1_amp)


plt.tight_layout()  # 紧凑布局，防止标题重叠
plt.show()

