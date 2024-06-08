import numpy as np
import matplotlib.pylab as plt  # 绘制图形

t = np.arange(-1.00, 10.00, 0.01)
print(len(t))   #t有多长？

np.seterr(divide='ignore', invalid='ignore')#numpy忽略除以零的警告

y1 = np.sinc(t/np.pi)*(np.heaviside(t+np.pi,0.5)-np.heaviside(t-np.pi,0.5))#不可以是中括号，不然维度不一致

y2 = np.sinc(t)*(np.heaviside(t+np.pi,0.5)-np.heaviside(t-np.pi,0.5))

plt.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体
plt.rcParams['axes.unicode_minus'] = False #解决图像中的负号'-'显示为方块的问题

plt.figure()#新建绘图
plt.subplot(211) #子图1
plt.grid() #显示网格
plt.plot(t, y1)

plt.subplot(212) #子图2
plt.grid() #显示网格
plt.plot(t, y2)

plt.tight_layout() #紧凑布局，防止标题重叠
plt.show()