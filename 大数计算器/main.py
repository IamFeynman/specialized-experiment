import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QColorDialog, QStyleFactory
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette, QBrush, QFont, QIcon, QPixmap, QPen
from cal import Cal_Core
from qframelesswindow import FramelessWindow, StandardTitleBar, AcrylicWindow
import Ui_task1
import base64

class calculator(AcrylicWindow, FramelessWindow):
    def __init__(self):
        self.last_expression = []
        self.result = []
        self.expression = ''
        super().__init__()
        
        self.ui = Ui_task1.Ui_Calculator()
        self.ui.setupUi(self)
        
        self.setTitleBar(StandardTitleBar(self))
        self.titleBar.raise_()
        self.titleBar.titleLabel.setStyleSheet("""
            QLabel{
                background: transparent;
                font: 13px 'Segoe UI';
                padding: 0 4px;
                color: white
            }
        """)
        self.titleBar.maxBtn.setNormalColor(QColor(255, 255, 255))
        self.titleBar.maxBtn.setHoverBackgroundColor(QColor(52, 49, 48))
        self.titleBar.closeBtn.setNormalColor(QColor(255, 255, 255))
        self.titleBar.minBtn.setNormalColor(QColor(255, 255, 255))
        self.titleBar.minBtn.setHoverBackgroundColor(QColor(52, 49, 48))

        # 创建计算器核心实例
        self.cal_core = Cal_Core()

        self.PURPLE = QColor(170, 170, 255)
        self.RED = QColor("#d83737")
        self.GREEN = QColor("#65d807")

        self.Eggtime = 0

    def Button_Press(self):
        sender_button_text = self.sender().text()
        if sender_button_text in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '+', '-', '*', '/', '<-', 'C', 'CE', 'clean_stack']:
            self.Button_Num_Press(sender_button_text)
        if sender_button_text == '=':
            self.Button_Num_Press(sender_button_text)
            if self.result == 'ERROR':
                self.ui.label_3.setText(str(self.result))
                self.ui.label_4.setText(str(self.expression))
            else:
                self.Change_LED_Color(3, self.PURPLE)
                if self.result == 0:
                    self.Change_LED_Color(2, self.GREEN)
                    self.Change_LED_Color(1, self.RED)
                elif self.result % 2 == 0:
                    self.Change_LED_Color(2, self.GREEN)
                elif self.result % 2 == 1:
                    self.Change_LED_Color(1, self.RED)
                
                self.ui.label_3.setText(str(self.result))
                self.ui.label_4.setText(str(self.expression))
                if self.result == 20040428:
                    self.Eggtime += 1
                    if self.Eggtime > 2:
                        self.Eggtime = 0
                        self.ui.label_4.setText(str('HAPPY'))
                        self.ui.label_3.setText(str('BIRTHDAY'))
                    else:
                        for bit in str(self.result):
                            self.Button_Num_Press(bit)
                else:
                    for bit in str(self.result):
                            self.Button_Num_Press(bit)

        if sender_button_text != 'C' and sender_button_text != 'CE':
            self.pressC = False
            self.ui.pushButton_20.setText('C')
        else:
            self.ui.label_3.setText('')
            self.Change_LED_Color(3, self.PURPLE)
            self.ui.pushButton_20.setText('CE')
            try:
                if self.pressC:
                    self.ui.label_4.setText('')
                self.pressC = True
            except:
                pass

        if sender_button_text == '1/x':
            if self.result == None:
                self.Button_Num_Press('=')
            if self.result == 0 or self.result == 'ERROR':
                self.ui.label_3.setText('ERROR')
                self.ui.label_4.setText('1/('+str(self.expression)+')')
                self.cal_core.cal_by_operation('clean_stack')
            else:
                show_result = Cal_Core.limit_result(Cal_Core,1.0 / self.result)
                self.ui.label_3.setText(str(show_result))
                self.ui.label_4.setText('1/('+str(self.expression)+')')
                self.cal_core.cal_by_operation('clean_stack')
                for bit in str(show_result):
                    self.Button_Num_Press(bit)

        if sender_button_text == '+/-':
            if self.result == None:
                self.Button_Num_Press('=')
            if self.result == None or self.result == 'ERROR':
                self.ui.label_3.setText('ERROR')
                self.ui.label_4.setText('-('+str(self.expression)+')')
                self.cal_core.cal_by_operation('clean_stack')
            else:
                show_result = Cal_Core.limit_result(Cal_Core, -self.result)
                self.ui.label_3.setText(str(show_result))
                self.ui.label_4.setText('-('+str(self.expression)+')')
                self.cal_core.cal_by_operation('clean_stack')
                for bit in str(show_result):
                    self.Button_Num_Press(bit)

    def Button_Num_Press(self, button_text):
        self.expression, self.result = self.cal_core.cal_by_operation(
            button_text)
        expression_string = ''.join(self.expression)
        self.ui.label_3.setText(str(expression_string))

    def Change_LED_Color(self, num, color):
        if num == 1 or num == 3:
            self.ui.label.setStyleSheet("color: white;\n"
                                        "border-radius: 20px;\n"
                                        "border: 2px groove gray;\n"
                                        "border-style: outset;\n"
                                        "background-color: " + color.name())
        if num == 2 or num == 3:
            self.ui.label_2.setStyleSheet("color: white;\n"
                                          "border-radius: 20px;\n"
                                          "border: 2px groove gray;\n"
                                          "border-style: outset;\n"
                                          "background-color: " + color.name())
    
    def keyPressEvent(self, event):
        return
        key = event.key()
        if Qt.Key_A <= key <= Qt.Key_Z:
            if event.modifiers() & Qt.ShiftModifier:  # Shift 键被按下
                self.statusBar().showMessage('"Shift+%s" pressed' % chr(key), 500)
            elif event.modifiers() & Qt.ControlModifier:  # Ctrl 键被按下
                self.statusBar().showMessage('"Control+%s" pressed' % chr(key), 500)
            elif event.modifiers() & Qt.AltModifier:  # Alt 键被按下
                self.statusBar().showMessage('"Alt+%s" pressed' % chr(key), 500)
            else:
                self.statusBar().showMessage('"%s" pressed' % chr(key), 500)

        elif key == Qt.Key_Home:
            self.statusBar().showMessage('"Home" pressed', 500)
        elif key == Qt.Key_End:
            self.statusBar().showMessage('"End" pressed', 500)
        elif key == Qt.Key_PageUp:
            self.statusBar().showMessage('"PageUp" pressed', 500)
        elif key == Qt.Key_PageDown:
            self.statusBar().showMessage('"PageDown" pressed', 500)
        else:  # 其它未设定的情况
            calculator.keyPressEvent(self, event)  # 留给基类处理


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = calculator()

    bitdata = b'iVBORw0KGgoAAAANSUhEUgAAAMgAAADICAYAAACtWK6eAAAACXBIWXMAAAsTAAALEwEAmpwYAAAE7mlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNy4xLWMwMDAgNzkuOWNjYzRkZSwgMjAyMi8wMy8xNC0xMToyNjoxOSAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iIHhtbG5zOnBob3Rvc2hvcD0iaHR0cDovL25zLmFkb2JlLmNvbS9waG90b3Nob3AvMS4wLyIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0RXZ0PSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VFdmVudCMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIDIzLjMgKFdpbmRvd3MpIiB4bXA6Q3JlYXRlRGF0ZT0iMjAyNC0wMy0zMFQxNzoyOTowMiswODowMCIgeG1wOk1vZGlmeURhdGU9IjIwMjQtMDQtMTJUMTM6NTA6MDgrMDg6MDAiIHhtcDpNZXRhZGF0YURhdGU9IjIwMjQtMDQtMTJUMTM6NTA6MDgrMDg6MDAiIGRjOmZvcm1hdD0iaW1hZ2UvcG5nIiBwaG90b3Nob3A6Q29sb3JNb2RlPSIzIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjQxMzllYzQ1LWJhZTQtOTg0MC05ZWFkLWU2NDQyNjBhNzZlYyIgeG1wTU06RG9jdW1lbnRJRD0i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'
    icon_img = base64.b64decode(bitdata)
    icon_pixmap = QPixmap()
    icon_pixmap.loadFromData(icon_img)
    # main_window.setWindowFlag(Qt.FramelessWindowHint)
    
    icon = QIcon(icon_pixmap)
    main_window.setWindowIcon(icon)
    main_window.setWindowOpacity(1)
    main_window.setWindowTitle("专业实验I-计算器")
    main_window.setFixedSize(main_window.width(), main_window.height())
    main_window.setWindowFlags(Qt.WindowCloseButtonHint)
    main_window.show()
    sys.exit(app.exec_())
