'''import sympy as sp

# 定义符号变量
t = sp.symbols('t')

# 定义 x(t) 和 y(t) 的表达式
x_t = sp.Function('x')(t)
y_t = x_t + x_t.subs(t, t + 1)

# 检查 y(t) 是否只依赖于 t 和 t+1
depends_on_future = sp.solveset(sp.Eq(y_t, y_t.subs(t, t + 2)), x_t, domain=sp.S.Reals)

if depends_on_future == sp.EmptySet:
    print("系统 y(t) = x(t) + x(t+1) 是因果系统")
else:
    print("系统 y(t) = x(t) + x(t+1) 不是因果系统")
'''
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

# 定义符号变量
t = sp.symbols('t')

# 定义 x(t) 为 Heaviside 阶跃函数
x_t = sp.Heaviside(t)

# 计算 y(t) = x(t) + x(t+1)
y_t = x_t + x_t.subs(t, t + 1)

# 将 x(t) 和 y(t) 转换为 Python 函数
x = sp.lambdify(t, x_t, "numpy")
y = sp.lambdify(t, y_t, "numpy")

# 生成时间范围
t_values = np.linspace(-1, 5, 1000)

# 计算 x(t) 和 y(t) 在给定时间范围内的值
x_values = x(t_values)
y_values = y(t_values)

# 绘制 x(t) 和 y(t) 的图形
plt.figure(figsize=(10, 6))
plt.plot(t_values, x_values, label='x(t) = Heaviside(t)')
plt.plot(t_values, y_values, label='y(t) = x(t) + x(t+1)')
plt.xlabel('t')
plt.ylabel('Amplitude')
plt.title('Plot of x(t) and y(t)')
plt.legend()
plt.grid(True)
plt.show()
