from scipy.signal import find_peaks
import numpy as np
import time
import matplotlib.pyplot as plt

'''
写在最前面：
写一个函数信号发生器，产生方波、三角波、正弦波（检测方式不同）
设置UI界面时需要注意：
函数信号发生器，你能能产生的波形频率范围（增加采样率按钮或者文本输入）
函数信号发生器产生的波形种类：下拉框形式
'''
# 采样率96000Hz，正确测量的最高频率是采样率的一半，即48kHz。
sampling_rate = 960000

'''
generate_waveform
根据input产生三种波形
'''
def generate_waveform(waveform_type, frequency, duration):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    if waveform_type == '正弦波':
        waveform = np.sin(2 * np.pi * frequency * t)
    elif waveform_type == '方波':
        waveform = np.sign(np.sin(2 * np.pi * frequency * t))
    elif waveform_type == '三角波':
        waveform = 2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1
    return waveform

'''
measure_period
使用time模块，计算开始计数、结束计数时间
'''
def measure_period(waveform):
    start_time = time.time()
    zero_crossings = np.where(np.diff(np.sign(waveform)))[0]  # 返回行索引
    # 计算相邻零交叉点之间的间隔，并求平均值
    periods = np.diff(zero_crossings)
    measured_period = np.mean(periods) / sampling_rate  # 转换为秒
    end_time = time.time()
    print("测量时间:", end_time - start_time, "秒")
    return measured_period

'''
measure_period_triangular
测量三角波函数，使用峰峰+零交叉点检测
'''
def measure_period_triangular(waveform):
    start_time = time.time()
    peaks, _ = find_peaks(waveform)
    valleys, _ = find_peaks(-waveform)
    zero_crossings = np.sort(np.concatenate([peaks, valleys]))

    # 计算相邻极值点之间的间隔，并求平均值
    periods = np.diff(zero_crossings)
    measured_period = np.mean(periods) / sampling_rate  # 转换为秒
    end_time = time.time()
    print("测量时间:", end_time - start_time, "秒")
    return measured_period

'''
calculate_error
计算误差
'''
def calculate_error(measured_freq, true_freq):
    return ((measured_freq - true_freq) / true_freq) * 100


'''
plot_waveform
绘制波形,根据input频率自适应调节，保持figure上10个周期左右
'''
def plot_waveform(waveform, waveform_type, frequency):
    duration = len(waveform) / sampling_rate
    t = np.linspace(0, duration, len(waveform))

    plt.rcParams['mathtext.fontset'] = 'stix'  # 公式字体风格
    plt.rcParams['font.sans-serif'] = ['SimSun']  # 指定非衬线字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决图像中的负号'-'显示为方块的问题

    plt.plot(t, waveform)
    plt.xlabel('时间 (秒)')
    plt.ylabel('幅值')
    plt.title('{} - 频率{} Hz'.format(waveform_type.capitalize(), frequency))
    plt.grid(True)
    plt.show()


def main():
    waveform_type = input("请输入波形类型 (正弦波, 方波, 三角波): ")
    frequency = float(input("请输入频率（Hz）: "))

    period_duration = 1 / frequency
    total_duration = period_duration * 10

    waveform = generate_waveform(waveform_type, frequency, total_duration)

    if waveform_type == '三角波':
        measured_period = measure_period_triangular(waveform)
    else:
        measured_period = measure_period(waveform)

    measured_freq = 1 / (measured_period * 2)

    true_freq = frequency  # 真实频率与输入频率相同

    plot_waveform(waveform, waveform_type, frequency)

    print("测量得到的周期:", measured_period, "秒")
    print("测量得到的频率:", measured_freq, "Hz")
    error = calculate_error(measured_freq, true_freq)
    print("频率误差:", error, "%")


if __name__ == "__main__":
    main()
