import sys
import pyaudio
import wave
import numpy as np
import librosa
import librosa.display
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import threading

'''
报告中增加处理前后音频图像、效果的处理
'''
# 录制参数
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 20000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "recorded_audio.wav"


class AudioRecorder(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.y = None
        self.sr = None
        self.y_filtered = None
        self.fft_result_before = None
        self.fft_result_after = None
        self.is_recording = False

    def initUI(self):
        self.setGeometry(600, 600, 600, 400)    # 窗口位置
        self.setWindowTitle('专业实验二：FFT音频处理')
        self.setStyleSheet("background-color: #f2f2f2;")

        self.startButton = QtWidgets.QPushButton('Start开始录制~~~', self)
        self.startButton.clicked.connect(self.startRecording)
        self.startButton.setGeometry(50, 50, 200, 40)
        self.startButton.setStyleSheet('background-color: blue; color: white;')

        self.reRecordButton = QtWidgets.QPushButton('Re-Record重新录制~~~', self)
        self.reRecordButton.clicked.connect(self.reRecord)
        self.reRecordButton.setGeometry(50, 100, 200, 40)
        self.reRecordButton.setStyleSheet("background-color: #e74c3c; color: white;")
        self.reRecordButton.setEnabled(False)

        self.playButton = QtWidgets.QPushButton('Play点击播放', self)
        self.playButton.clicked.connect(self.playAudio)
        self.playButton.setGeometry(50, 150, 200, 40)
        self.playButton.setEnabled(False)
        self.playButton.setStyleSheet("background-color: #2ecc71; color: white;")

        self.exitButton = QtWidgets.QPushButton('Exit退出', self)
        self.exitButton.clicked.connect(self.close)
        self.exitButton.setGeometry(50, 200, 200, 40)

        self.statusLabel = QtWidgets.QLabel(self)
        self.statusLabel.setGeometry(125, 250, 500, 20)
        self.statusLabel.setText("准备就绪")

        # 使用setStyleSheet让按钮圆滑好看
        self.startButton.setStyleSheet('background-color: blue; color: white; border-radius: 20px;')
        self.reRecordButton.setStyleSheet("background-color: #e74c3c; color: white; border-radius: 20px;")
        self.playButton.setStyleSheet("background-color: #2ecc71; color: white; border-radius: 20px;")
        self.exitButton.setStyleSheet("background-color: gray; color: white; border-radius: 20px;")

    def startRecording(self):
        self.statusLabel.setText("录制中...")
        self.is_recording = True
        self.frames = []  # 清空之前的录制数据
        threading.Thread(target=self.recordAudio).start()

    def recordAudio(self):
        self.stream = self.audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = self.stream.read(CHUNK, exception_on_overflow=False)
            self.frames.append(data)
        self.stream.stop_stream()
        self.stream.close()
        self.is_recording = False
        self.statusLabel.setText("录制完成")
        self.reRecordButton.setEnabled(True)
        self.playButton.setEnabled(True)
        self.processAudio()

    def processAudio(self):
        with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(self.frames))

        self.y, self.sr = librosa.load(WAVE_OUTPUT_FILENAME, sr=RATE)

        # 预加重处理
        self.y_filtered = librosa.effects.preemphasis(self.y)

        # 处理前FFT
        self.fft_result_before = np.fft.fft(self.y)
        freq_before = np.fft.fftfreq(len(self.fft_result_before), 1.0 / self.sr)
        spectrum_power_before = np.abs(self.fft_result_before) ** 2

        # 处理后FFT
        self.fft_result_after = np.fft.fft(self.y_filtered)
        freq_after = np.fft.fftfreq(len(self.fft_result_after), 1.0 / self.sr)
        spectrum_power_after = np.abs(self.fft_result_after) ** 2

        max_power = max(np.max(spectrum_power_before), np.max(spectrum_power_after))
        min_power = min(np.min(spectrum_power_before), np.min(spectrum_power_after))
        spectrum_power_before_norm = (spectrum_power_before - min_power) / (max_power - min_power)
        spectrum_power_after_norm = (spectrum_power_after - min_power) / (max_power - min_power)

        self.plotAudio(freq_before, spectrum_power_before_norm, freq_after, spectrum_power_after_norm)

    def plotAudio(self, freq_before, spectrum_power_before, freq_after, spectrum_power_after):
        dialog = PlotDialog(freq_before, spectrum_power_before, freq_after, spectrum_power_after, self.y, self.y_filtered)
        dialog.exec_()

    def reRecord(self):
        self.statusLabel.setText("重新录制中...")
        threading.Thread(target=self.recordAudio).start()

    def playAudio(self):
        y_processed_waveform = np.fft.ifft(self.fft_result_after).real
        stream = self.audio.open(format=pyaudio.paFloat32, channels=1, rate=RATE, output=True)
        stream.write(y_processed_waveform.astype(np.float32).tobytes())
        stream.stop_stream()
        stream.close()

    def closeEvent(self, event):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()
        super().closeEvent(event)

class PlotDialog(QtWidgets.QDialog):
    def __init__(self, freq_before, spectrum_power_before, freq_after, spectrum_power_after, y_before, y_after):
        super().__init__()
        self.freq_before = freq_before
        self.spectrum_power_before = spectrum_power_before
        self.freq_after = freq_after
        self.spectrum_power_after = spectrum_power_after
        self.y_before = y_before
        self.y_after = y_after
        self.initUI()

    def initUI(self):
        self.setWindowTitle('音频分析图像')

        # 图形UI铺满全屏
        desktop = QtWidgets.QApplication.desktop()
        screen_rect = desktop.screenGeometry()
        width, height = screen_rect.width(), screen_rect.height()
        self.setGeometry(0, 0, width, height)

        self.fig, axes = plt.subplots(3, 2, figsize=(12, 12))

        plt.rcParams['mathtext.fontset'] = 'stix'  # 公式字体风格
        plt.rcParams['font.sans-serif'] = ['SimSun']  # 指定非衬线字体
        plt.rcParams['axes.unicode_minus'] = False  # 解决图像中的负号'-'显示为方块的问题

        self.plotSpectrum(axes[0, 0], self.freq_before, self.spectrum_power_before, 'Spectrum 频谱（处理前）')
        self.plotSpectrum(axes[0, 1], self.freq_after, self.spectrum_power_after, 'Spectrum 频谱（处理后）')
        self.plotPowerSpectrum(axes[1, 0], self.freq_before, self.spectrum_power_before, 'Power Spectrum 功率谱（处理前）')
        self.plotPowerSpectrum(axes[1, 1], self.freq_after, self.spectrum_power_after, 'Power Spectrum 功率谱（处理后）')
        self.plotWaveform(axes[2, 0], self.y_before, 'Waveform 波形图（处理前）')
        self.plotWaveform(axes[2, 1], self.y_after, 'Waveform 波形图（处理后）')

        self.canvas = FigureCanvas(self.fig)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plotSpectrum(self, ax, freq, spectrum_power, title):
        ax.plot(freq, spectrum_power)
        ax.set_title(title)
        ax.set_xlabel('Frequency 频率 (Hz)')
        ax.set_ylabel('Amplitude')

    def plotPowerSpectrum(self, ax, freq, spectrum_power, title):
        ax.plot(freq, spectrum_power)
        ax.set_title(title)
        ax.set_xlabel('Frequency 频率 (Hz)')
        ax.set_ylabel('Power')

    def plotWaveform(self, ax, y, title):
        librosa.display.waveplot(y, sr=RATE, ax=ax)
        ax.set_title(title)
        ax.set_xlabel('Time 时间 (s)')
        ax.set_ylabel('Amplitude 幅值')
        ax.set_ylim([-1, 1])  # 根据数据动态调节范围

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = AudioRecorder()
    mainWindow.show()
    sys.exit(app.exec_())
