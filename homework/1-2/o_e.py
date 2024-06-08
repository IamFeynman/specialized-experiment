import matplotlib.pylab as plt  # 绘制图形
from sympy import *

#定义函数和自变量
t = Symbol('t')
x = symbols('x', cls=Function)

x1 = sin(2*pi*t)*(Heaviside(t-1)-Heaviside(t-2))
x2 = x1.subs(t,-t)

#奇分量
x3 = (x1-x2)/2
#偶分量
x4 = (x1+x2)/2


#如果需要显示中文，则需要加入下面两行
plt.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体
plt.rcParams['axes.unicode_minus'] = False #解决图像中的负号'-'显示为方块的问

p0=plot(x1,(t,-4,4),title='x1(t)',xlabel='t',show=False)
p1=plot(x2,(t,-4,4),title='x2(t)',xlabel='t',show=False)
p2=plot(x3,(t,-4,4),title='奇分量',xlabel='t',show=False)
p3=plot(x4,(t,-4,4),title='偶分量',xlabel='t',show=False)

p = plotting.PlotGrid(2,2,p0,p1,p2,p3)
