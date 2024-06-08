# pyaudio是一个Python库，可以用于录制和播放音频。你可以使用它来实时获取电脑音频数据。
# librosa是一个用于音频和音乐分析的Python库，提供了各种音频信号处理和音乐信息提取的功能。你可以结合pyaudio和librosa，实时获取音频数据并使用librosa进行分析。
# https://blog.51cto.com/u_16099327/7475766
# https://zhuanlan.zhihu.com/p/445030720
# https://blog.csdn.net/qq_39798423/article/details/86764443
# https://pythonjishu.com/flqcjxpjfsugbfj/
# https://blog.csdn.net/sinat_18131557/article/details/106440692 自适应滤波

import numpy as np
from matplotlib import pyplot as plt
from scipy.fft import fft, fftfreq, ifft

SAMPLE_RATE = 44100  # Hertz
DURATION = 5  # Seconds

# 生成一个正弦信号
def generate_sine_wave(freq, sample_rate, duration):
    x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
    frequencies = x * freq
    # 2pi because np.sin takes radians
    y = np.sin((2 * np.pi) * frequencies)
    return x, y

# Generate a 2 hertz sine wave that lasts for 5 seconds
x, y = generate_sine_wave(2, SAMPLE_RATE, DURATION)
plt.plot(x, y)
plt.show()

# 生成正弦信号和噪声信号然后叠加
_, nice_tone = generate_sine_wave(400, SAMPLE_RATE, DURATION)
_, noise_tone = generate_sine_wave(4000, SAMPLE_RATE, DURATION)
noise_tone = noise_tone * 0.3

# 对产生的数据进行归一化
mixed_tone = nice_tone + noise_tone
normalized_tone = np.int16((mixed_tone / mixed_tone.max()) * 32767)

# 绘制出合成的时域波形图
plt.plot(normalized_tone[:1000])
plt.show()

# Number of samples in normalized_tone
N = SAMPLE_RATE * DURATION

# 计算波形的FFT
# 计算变换本身
yf = fft(normalized_tone)
# 计算的输出中每个bin中心的频率fft()
xf = fftfreq(N, 1 / SAMPLE_RATE)

plt.plot(xf, np.abs(yf))
plt.show()

yf = fft(normalized_tone)
xf = fftfreq(N, 1 / SAMPLE_RATE)

# rfft，rfft()只返回一半的输出fft()，产生正半轴的频率
from scipy.fft import rfft, rfftfreq

# Note the extra 'r' at the front
yf = rfft(normalized_tone)
xf = rfftfreq(N, 1 / SAMPLE_RATE)

plt.plot(xf, np.abs(yf))
plt.show()

# 过滤信号
# The maximum frequency is half the sample rate
points_per_freq = len(xf) / (SAMPLE_RATE / 2)

# Our target frequency is 4000 Hz
target_idx = int(points_per_freq * 4000)

yf[target_idx - 1 : target_idx + 2] = 0
plt.plot(xf, np.abs(yf))
plt.show()

# Scipy ifft 逆向傅里叶变换
from scipy.fft import irfft
new_sig = irfft(yf)
plt.plot(new_sig[:1000])
plt.show()