import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, \
    QTableWidget, QTableWidgetItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import time
import os
from memory_profiler import profile

"""
使用标准差规则检测异常值
参数：
data: 待检测异常值的数据
threshold: 异常值的阈值，通常为标准差的倍数，默认为2
返回：
outliers: 异常值的索引列表、mean、data数组大小、标准差
"""
def detect_outliers(data, threshold=2):
    mean = np.mean(data)
    std = np.std(data)
    outliers = []
    for i, value in enumerate(data):
        if abs(value - mean) > threshold * std:
            outliers.append(i)
    return outliers, mean, len(data), std

"""
UI设计模块，定义 MyGUI 类
initUI(): 创建窗口、按钮、文本框、图表等界面元素
generate_simulated_data(): 生成模拟数据
detect_outliers_and_plot(): 检测异常值并绘制图表
reset_data_and_redetect_outliers(): 重置数据并重新检测异常值
"""
class MyGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('温度传感器异常值检测')
        self.setGeometry(300, 300, 800, 800)

        self.btn_detect = QPushButton('开始检测/Measure', self)
        self.btn_detect.setStyleSheet("background-color: lightblue")
        self.btn_detect.setFixedSize(200, 100)
        self.btn_detect.clicked.connect(self.detect_outliers_and_plot)

        self.btn_retest = QPushButton('重新检测/Restart', self)
        self.btn_retest.setStyleSheet("background-color: lightgreen")
        self.btn_retest.setFixedSize(200, 100)
        self.btn_retest.clicked.connect(self.reset_data_and_redetect_outliers)

        self.btn_exit = QPushButton('退出/Exit', self)
        self.btn_exit.setStyleSheet("background-color: lightcoral")
        self.btn_exit.setFixedSize(200, 100)
        self.btn_exit.clicked.connect(self.close)

        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(self.btn_detect)
        hbox_layout.addWidget(self.btn_retest)
        hbox_layout.addWidget(self.btn_exit)

        self.text_info = QTextEdit()
        self.text_info.setReadOnly(True)

        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 5))
        self.canvas = FigureCanvas(self.fig)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["索引", "温度 (℃)"])

        self.layout = QVBoxLayout()
        self.layout.addLayout(hbox_layout)
        self.layout.addWidget(self.canvas)

        self.stats_layout = QHBoxLayout()
        self.stats_layout.addWidget(self.table)
        self.stats_layout.addWidget(self.text_info)

        self.layout.addLayout(self.stats_layout)

        self.setLayout(self.layout)

    """
        温度传感器模拟产生异常值
        data：25±1
        error_values：25±15，num_errors随机
    """
    def generate_simulated_data(self, num_samples=100, num_errors=3):
        seed = np.random.randint(1000000)  # Generate a new seed each time
        np.random.seed(seed)
        data = np.random.normal(loc=25, scale=1, size=num_samples)  # 正常测量值序列
        error_indices = np.random.choice(num_samples, num_errors, replace=False)
        error_values = np.random.normal(loc=25, scale=15, size=num_errors)  # 异常值25±15
        data_with_errors = np.copy(data)
        data_with_errors[error_indices] = error_values
        return data_with_errors

    def reset_data(self):
        self.data = self.generate_simulated_data()

    """
    检测异常值并绘制图像
    绘制数据直方图
    绘制统计学箱线图
    """
    def detect_outliers_and_plot(self):
        self.data = self.generate_simulated_data()
        data = self.data

        outliers, mean, data_count, std = detect_outliers(data)

        outlier_indices = ', '.join(map(str, outliers))
        stats_info = f'温度传感器统计信息：\n数据个数：{data_count}\n平均值：{mean:.2f}\n标准差：{std:.2f}\n异常值数量：{len(outliers)}\n异常值索引：{outlier_indices}'
        self.text_info.setPlainText(stats_info)

        self.ax1.clear()
        self.ax1.hist(data, bins=20, alpha=0.5, color='skyblue')
        self.ax1.set_title('数据分布直方图')
        self.ax1.set_ylabel('频次Frequency')
        self.ax1.set_xlabel('温度t/℃')

        self.ax2.clear()
        self.ax2.boxplot(data, showfliers=False)

        plt.rcParams['mathtext.fontset'] = 'stix'  # 公式字体风格
        plt.rcParams['font.sans-serif'] = ['SimSun']  # 指定非衬线字体
        plt.rcParams['axes.unicode_minus'] = False  # 解决图像中的负号'-'显示为方块的问题

        # 添加标准差分界线
        mean_line = np.mean(data)
        std_line = np.std(data)
        self.ax2.axhline(mean_line, color='green', linestyle='--', label='Mean')
        #self.ax2.axhline(mean_line + std_line, color='orange', linestyle='--', label='+1 Std Dev')
        #self.ax2.axhline(mean_line - std_line, color='orange', linestyle='--', label='-1 Std Dev')
        self.ax2.axhline(mean_line + 2 * std_line, color='red', linestyle='--', label='+2 Std Dev')
        self.ax2.axhline(mean_line - 2 * std_line, color='red', linestyle='--', label='-2 Std Dev')
        #self.ax2.axhline(mean_line + 3 * std_line, color='purple', linestyle='--', label='+3 Std Dev')
        #self.ax2.axhline(mean_line - 3 * std_line, color='purple', linestyle='--', label='-3 Std Dev')

        # 将异常值标记为红点ro
        self.red_points = []
        for outlier in outliers:
            red_point = self.ax2.plot(1, data[outlier], 'ro', picker=5)[0]  # 设置picker属性为5
            self.red_points.append((red_point, outlier))  # 保存红点对象和索引

        self.ax2.set_title('箱线图')
        self.ax2.set_xlabel('Data')
        self.ax2.set_ylabel('Value')

        self.ax2.legend(loc='upper right')  # 将图例放置到右上角
        self.canvas.draw()

        self.table.setRowCount(0)
        for i, value in enumerate(data):
            self.table.insertRow(self.table.rowCount())
            item_index = QTableWidgetItem(str(i))
            item_value = QTableWidgetItem(f'{value:.2f}')
            if i in outliers:
                item_index.setForeground(QtGui.QColor('red'))
                item_value.setForeground(QtGui.QColor('red'))
            self.table.setItem(self.table.rowCount() - 1, 0, item_index)
            self.table.setItem(self.table.rowCount() - 1, 1, item_value)

    def on_pick(self, event):
        if isinstance(event.artist, plt.Line2D):
            red_point, index = event.artist, int(event.artist.get_xdata()[0])
            self.text_info.setPlainText(f'索引：{index}\n温度值：{self.data[index]:.2f}')

    def reset_data_and_redetect_outliers(self):
        self.reset_data()
        self.detect_outliers_and_plot()

class PerformanceTest:
    def __init__(self, function_to_test):
        self.function_to_test = function_to_test

    def time_test(self):
        start_time = time.time()
        self.function_to_test()  # 运行你的检测异常值和绘制图表函数
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"程序运行时间：{elapsed_time} 秒")

    @profile
    def memory_test(self):
        self.function_to_test()  # 运行你的检测异常值和绘制图表函数
        print("函数运行结束")

    def performance_test(self):
        print("运行时间测试：")
        self.time_test()
        print("\n内存占用测试：")
        self.memory_test()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = MyGUI()
    gui.show()

    # 连接pick_event事件
    gui.canvas.mpl_connect('pick_event', gui.on_pick)

    gui.performance_test = PerformanceTest(gui.detect_outliers_and_plot)
    gui.performance_test.performance_test()

    sys.exit(app.exec_())
