import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt

# 录制参数（采样点1024个、采样率20KHz、声道数1、记录时间5s）
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 20000
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "recorded_audio.wav"

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

# 读取录制的音频文件并进行FFT
print("开始进行FFT分析...")
with wave.open(WAVE_OUTPUT_FILENAME, 'rb') as wf:
    # 读取音频数据
    data = wf.readframes(wf.getnframes())

    # 将音频数据转换为numpy数组
    audio_data = np.frombuffer(data, dtype=np.int16)

    # 进行FFT分析
    fft_result = np.fft.fft(audio_data)
    freq = np.fft.fftfreq(len(fft_result), 1.0 / RATE)

# 绘制频谱图
plt.figure(figsize=(10, 6))

plt.rcParams['mathtext.fontset'] = 'stix'  # 公式字体风格
plt.rcParams['font.sans-serif'] = ['SimSun']  # 指定非衬线字体
plt.rcParams['axes.unicode_minus'] = False  # 解决图像中的负号'-'显示为方块的问题

plt.plot(freq, np.abs(fft_result))
plt.title('频谱(Spectrum)')
plt.xlabel('频率Frequency (Hz)')
plt.ylabel('幅值Amplitude')
plt.grid(True)
plt.show()

# 计算频谱能量分布
spectrum_power = np.abs(fft_result) ** 2

# 绘制频谱能量图
plt.figure(figsize=(10, 6))
plt.plot(freq, spectrum_power)
plt.title('功率谱(Power Spectrum)')
plt.xlabel('频率Frequency (Hz)')
plt.ylabel('功率Power')
plt.grid(True)
plt.show()

# 播放录制的音频
print("开始播放录制的音频...")
with wave.open(WAVE_OUTPUT_FILENAME, 'rb') as wf:
    # 打开音频流
    audio = pyaudio.PyAudio()
    stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

    # 读取数据并播放
    data = wf.readframes(CHUNK)
    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)

    # 停止音频流和关闭音频
    stream.stop_stream()
    stream.close()
    audio.terminate()