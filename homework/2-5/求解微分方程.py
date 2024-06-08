from sympy import *
import sympy as sy
'''定义微分方程'''
# 定义自变量和函数，对于单输入单输出系统，只需要定义t和y
t = symbols('t')
e, r = symbols('e r', cls=Function)
# 激励信号
e = sy.Heaviside(t)

# 建立微分方程，格式为一个Eq（等式）
diffeq = Eq(r(t).diff(t, 2) + 3 * r(t).diff(t) + 2 * r(t), e.diff(t) + 3*e)

# 求通解（包括特解），调用dsolve函数,返回一个Eq对象
respone = dsolve(diffeq, r(t), ics={r(0): 1, r(t).diff(t).subs(t, 0): 2})
# 两种显示方式
print(respone)  # 常规方式，如果形式复杂，可以尝试调用simplify进行化简
print(pretty(respone))  # 易读方式