import numpy as np
import matplotlib.pyplot as plt

"""
   使用标准差规则检测异常值
   参数：
   data: 待检测异常值的数据
   threshold: 异常值的阈值，通常为标准差的倍数，默认为2
   返回：
   outliers: 异常值的索引列表
   """
def detect_outliers(data, threshold=2):

    mean = np.mean(data)
    std = np.std(data)
    outliers = []
    for i, value in enumerate(data):
        if abs(value - mean) > threshold * std:
            outliers.append(i)
    return outliers

# 生成随机数据
np.random.seed(42)  # 设置随机种子以确保可重复性
data = np.random.normal(loc=0, scale=1, size=100)#从正态（高斯）分布中抽取随机样本

# 在随机数据中引入一些异常值
data[20] = 5
data[45] = -3

# 检测异常值
outliers = detect_outliers(data)

# 绘制箱线图
plt.boxplot(data)

plt.rcParams['mathtext.fontset'] = 'stix'  # 公式字体风格
plt.rcParams['font.sans-serif'] = ['SimSun']  # 指定非衬线字体
plt.rcParams['axes.unicode_minus'] = False  # 解决图像中的负号'-'显示为方块的问题

# 标记异常值
for i in outliers:
    plt.plot(1, data[i], 'ro')  # 将异常点标记为红色圆点
    print("异常的数据是：",i)

plt.title('温度传感器的箱线图')
plt.xlabel('Data')
plt.ylabel('Value')

plt.show()


