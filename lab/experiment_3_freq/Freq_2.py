import numpy as np
import time
import matplotlib.pyplot as plt

# https://blog.csdn.net/weixin_38346042/article/details/119181014
'''
设置UI界面时需要注意：
函数信号发生器，你能能产生的波形频率范围（增加采样率按钮或者文本输入）
函数信号发生器产生的波形种类：下拉框形式
'''

# 采样率96000Hz，正确测量的最高频率是采样率的一半，即48kHz。
sampling_rate = 96000

"""
    生成方波信号
    Parameters:
        frequency (float): 方波的频率
        duration (float): 方波的持续时间
    Returns:
        numpy.ndarray: 生成的方波信号
"""
def generate_square_wave(frequency, duration):
    # 生成一个指定大小，指定数据区间的均匀分布序列,不包含最大值，我们使用96000的采样率
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    # 生成方波信号（先产生正弦信号，再使用sign判断正负）
    signal = np.sign(np.sin(2 * np.pi * frequency * t))
    return signal

"""
    测量信号的周期
    Parameters:
        signal (numpy.ndarray): 输入信号
    Returns:
        float: 信号的周期（秒）
"""
def measure_period(signal):

    start_time = time.time()  # 记录开始时间
    num_cycles = np.sum(signal[1:] != signal[:-1]) / 2  # 我们使用边沿检测，判断布尔数组
    duration = len(signal) / sampling_rate  # 96000 是采样率
    period = duration / num_cycles if num_cycles != 0 else 0
    end_time = time.time()  # 记录结束时间
    print("测量时间:", end_time - start_time, "秒")
    return period

""" 
绘制方波信号
   Parameters:
       signal (numpy.100ndarray): 方波信号
       frequency (float): 方波的频率
"""
def plot_square_wave(signal, frequency):

    duration = len(signal) / sampling_rate
    t = np.linspace(0, duration, len(signal))
    plt.rcParams['mathtext.fontset'] = 'stix'  # 公式字体风格
    plt.rcParams['font.sans-serif'] = ['SimSun']  # 指定非衬线字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决图像中的负号'-'显示为方块的问题

    plt.plot(t, signal)
    plt.xlabel('时间 (秒)')
    plt.ylabel('幅值')
    plt.title('频率为{} Hz的方波'.format(frequency))
    plt.grid(True)
    plt.show()

def main():
    frequency = float(input("请输入方波的频率（Hz）："))

    # 计算每个周期的持续时间
    period_duration = 1 / frequency
    # 计算总的持续时间，确保在画板上呈现5-10个完整周期的方波
    total_duration = period_duration * 10  # 假设我们希望至少呈现10个周期

    # 生成方波信号
    signal = generate_square_wave(frequency, total_duration)

    # 测量周期
    measured_period = measure_period(signal)
    measured_freq = 1 / measured_period

    # 绘制方波信号
    plot_square_wave(signal, frequency)

    # 打印测量结果
    print("测量得到的周期:", measured_period, "秒")
    print("测量得到的频率:", measured_freq, "HZ")


if __name__ == "__main__":
    main()
