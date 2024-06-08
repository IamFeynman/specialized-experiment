import matplotlib.pylab as plt  # 绘制图形
from sympy import *

#定义函数和自变量
t = Symbol('t')
w = 1
t0 = 0.5
x = symbols('x', cls=Function)

x1 = sin(w*t)*Heaviside(t)
x2 = sin(w*(t-t0))*Heaviside(t)
x3 = sin(w*t)*Heaviside(t-t0)
x4 = sin(w*(t-t0))*Heaviside(t-t0)

p0=plot(x1,(t,-4,4),title='x1(t)',xlabel='t',show=False)
p1=plot(x2,(t,-4,4),title='x2(t)',xlabel='t',show=False)
p2=plot(x3,(t,-4,4),title='x3(t)',xlabel='t',show=False)
p3=plot(x4,(t,-4,4),title='x4(t)',xlabel='t',show=False)

p = plotting.PlotGrid(2,2,p0,p1,p2,p3)




