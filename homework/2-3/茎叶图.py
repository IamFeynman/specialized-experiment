import numpy as np
import matplotlib.pylab as plt  # 绘制图形

x = np.arange(-1, 10, 1)
print(len(x))
sig = np.exp((-0.5 + 10j) * x)

re_sig = sig.real       #实部
im_sig = sig.imag       #虚部
abs_sig = np.abs(sig)   #模值
ang_sig = np.unwrap(np.angle(sig))  # 解卷绕

plt.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体
plt.rcParams['axes.unicode_minus'] = False #解决图像中的负号'-'显示为方块的问题

plt.figure()#新建绘图
plt.subplot(221)
plt.grid()  # 显示网格
plt.title("复函数-实部", loc='left')
plt.stem(x, re_sig)

plt.subplot(222)
plt.grid()  # 显示网格
plt.title("复函数-虚部", loc='left')
plt.stem(x, im_sig)

plt.subplot(223)
plt.grid()  # 显示网格
plt.title("复函数-模值", loc='left')
plt.stem(x, abs_sig)

plt.subplot(224)
plt.grid()  # 显示网格
plt.title("复函数-相位", loc='left')
plt.stem(x, ang_sig)

plt.tight_layout()
plt.show()  # 显示

