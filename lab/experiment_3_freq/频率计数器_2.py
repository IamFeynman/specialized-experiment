import sys
from PyQt5.QtGui import QColor, QPalette, QBrush, QFont, QIcon, QPixmap, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from scipy.signal import find_peaks
import numpy as np
import time
import matplotlib.pyplot as plt
from PyQt5 import QtCore
from PyQt5.QtCore import Qt



class WaveformGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Freq.ui', self)
        self.setWindowTitle("专业实验三：频率计数器（任子昂）")

        self.generate_button.clicked.connect(self.generate_waveform)
        self.random_button.clicked.connect(self.generate_random)
        self.close_button.clicked.connect(self.close)

    ''' 
    根据input获取三种波形和频率
    '''
    def generate_waveform(self):
        waveform_type = self.waveform_combobox.currentText()
        frequency = float(self.frequency_lineedit.text())
        self.generate_and_plot_waveform(waveform_type, frequency)

    '''
        根据random获取三种波形和频率
    '''
    def generate_random(self):
        waveform_type = self.waveform_combobox.currentText()
        frequency = np.random.randint(10, 10001)  # 生成10到10K Hz之间的随机频率
        self.frequency_lineedit.setText(str(frequency))
        self.generate_and_plot_waveform(waveform_type, frequency)

    '''
        main
        产生并绘制波形：自适应周期，每个Figure有10个周期波形
     '''
    def generate_and_plot_waveform(self, waveform_type, frequency):

        # 采样率96000Hz，正确测量的最高频率是采样率的一半，即48kHz。
        sampling_rate = 960000
        duration = 10/frequency

        t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
        if waveform_type == '正弦波':
            waveform = np.sin(2 * np.pi * frequency * t)
        elif waveform_type == '方波':
            waveform = np.sign(np.sin(2 * np.pi * frequency * t))
        elif waveform_type == '三角波':
            waveform = 2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1

        measured_period, measured_freq = self.measure_period(waveform)

        self.plot_waveform(waveform, waveform_type, frequency)

        result = f"生成 {waveform_type} ，频率为 {frequency} Hz\n"
        result += f"测量得到的周期: {measured_period*2:.6f} 秒\n"   # F*2操作
        result += f"测量得到的频率: {measured_freq:.6f} Hz\n"
        error = self.calculate_error(measured_freq, frequency)
        result += f"频率误差: {error:.6f} %"
        self.result_textedit.setPlainText(result)

    '''
    measure_period
    使用time模块，计算开始计数、结束计数时间
    '''
    def measure_period(self, waveform):
        start_time = time.time()
        peaks, _ = find_peaks(waveform)
        valleys, _ = find_peaks(-waveform)
        zero_crossings = np.sort(np.concatenate([peaks, valleys]))

        periods = np.diff(zero_crossings)
        measured_period = np.mean(periods) / 960000  # 转换为秒
        measured_freq = 1 / (measured_period * 2)
        end_time = time.time()
        print("测量时间:", end_time - start_time, "秒")
        return measured_period, measured_freq

    '''
    calculate_error
    计算误差
    '''
    def calculate_error(self, measured_freq, true_freq):
        return ((measured_freq - true_freq) / true_freq) * 100

    '''
    plot_waveform
    绘制波形,根据input频率自适应调节，保持figure上10个周期左右
    '''
    def plot_waveform(self, waveform, waveform_type, frequency):
        duration = len(waveform) / 960000
        t = np.linspace(0, duration, len(waveform))

        plt.rcParams['mathtext.fontset'] = 'stix'
        plt.rcParams['font.sans-serif'] = ['SimSun']
        plt.rcParams['axes.unicode_minus'] = False

        plt.plot(t, waveform)
        plt.xlabel('时间 (秒)')
        plt.ylabel('幅值')
        plt.title('{} - 频率{} Hz'.format(waveform_type.capitalize(), frequency))
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling) # 合理显示QT框架
    app = QApplication(sys.argv)
    window = WaveformGenerator()
    window.show()
    sys.exit(app.exec_())
