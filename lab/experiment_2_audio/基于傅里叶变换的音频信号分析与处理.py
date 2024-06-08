import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

'''
# 录制参数
CHUNK：录制音频时每个缓冲区的帧数
FORMAT：音频数据的格式。pyaudio.paInt16表示16位整数格式
CHANNELS：音频通道的数量
RATE：采样率，即每秒钟捕获的样本数
RECORD_SECONDS：音频录制的持续时间
'''
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 20000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "recorded_audio.wav"

'''
PyAudio音频录制
'''
# 初始化PyAudio
audio = pyaudio.PyAudio()
# 打开音频流
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
print("开始录制音频...")
# 录制音频数据，循环写入音频数据
frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print("录制完成.")
# 停止录制并关闭音频流
stream.stop_stream()
stream.close()
audio.terminate()

# 保存录制的音频到文件
with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
print("音频已保存至:", WAVE_OUTPUT_FILENAME)

'''
语音处理前FFT声音可视化
'''
# 读取录制的音频文件
y, sr = librosa.load(WAVE_OUTPUT_FILENAME, sr=RATE)
# 对录制的音频进行FFT（处理前）
fft_result_before = np.fft.fft(y)
freq_before = np.fft.fftfreq(len(fft_result_before), 1.0 / RATE)
# 计算频谱能量分布（处理前）
spectrum_power_before = np.abs(fft_result_before) ** 2

'''
语音处理：librosa.effects.preemphasis()：预加重是一种简单的去噪技术，它通过减少低频分量的影响来增强高频分量。
'''
# 对录制的音频进行降噪和滤波处理
y_filtered = librosa.effects.preemphasis(y)  # 预加重处理

'''
语音处理后，声音可视化
'''
# 对处理后的音频进行FFT
fft_result_after = np.fft.fft(y_filtered)
freq_after = np.fft.fftfreq(len(fft_result_after), 1.0 / RATE)
# 计算频谱能量分布（处理后）
spectrum_power_after = np.abs(fft_result_after) ** 2

# 对处理后的频谱和功率谱图进行归一化处理
max_power = max(np.max(spectrum_power_before), np.max(spectrum_power_after))
min_power = min(np.min(spectrum_power_before), np.min(spectrum_power_after))
spectrum_power_before_norm = (spectrum_power_before - min_power) / (max_power - min_power)
spectrum_power_after_norm = (spectrum_power_after - min_power) / (max_power - min_power)

# 调整 "Processed Audio Waveform (After)" 的波形图的 y 轴范围
waveform_amp_range = (-0.4, 0.4)

'''
绘制处理前后频谱、功率谱和波形图
'''
plt.figure(figsize=(10, 10))

# 绘制处理前的频谱图
plt.subplot(3, 2, 1)
plt.plot(freq_before, np.abs(fft_result_before))
plt.title('Processed Audio Spectrum (Before)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.grid(True)

# 绘制处理前的功率谱图
plt.subplot(3, 2, 3)
plt.plot(freq_before, spectrum_power_before_norm)
plt.title('Processed Audio Power Spectrum (Before)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power')
plt.grid(True)

# 绘制处理前的音频波形图
plt.subplot(3, 2, 5)
librosa.display.waveplot(y, sr=sr)
plt.title('Processed Audio Waveform (Before)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.ylim(waveform_amp_range)

# 绘制处理后的频谱图
plt.subplot(3, 2, 2)
plt.plot(freq_after, np.abs(fft_result_after))
plt.title('Processed Audio Spectrum (After)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.grid(True)

# 绘制处理后的功率谱图
plt.subplot(3, 2, 4)
plt.plot(freq_after, spectrum_power_after_norm)
plt.title('Processed Audio Power Spectrum (After)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power')
plt.grid(True)

# 绘制处理后的音频波形图
plt.subplot(3, 2, 6)
librosa.display.waveplot(y_filtered, sr=sr)
plt.title('Processed Audio Waveform (After)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.ylim(waveform_amp_range)

plt.tight_layout()
plt.show()

'''
IFFT播放声音
'''
# 使用IFFT将处理后的声音播放出来
y_processed_waveform = np.fft.ifft(fft_result_after).real

# 将声音播放出来
print("开始播放处理后的音频...")
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=RATE,
                    output=True)

stream.write(y_processed_waveform.astype(np.float32).tobytes())
stream.stop_stream()
stream.close()
audio.terminate()
