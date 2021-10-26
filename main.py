import sys
import main_menu
import main_graphs_1
import numpy as np
import plot_canvas as pc
from PyQt5 import QtWidgets, QtGui, QtCore


G = 9.8

def read_line(line):
    value = 0
    try:
        value = float(line)
        return value, True
    except Exception as error:
        print(str(error))
        return value, False


class Menu(QtWidgets.QMainWindow, main_menu.Ui_MainWindow_1):
    def __init__(self, connect):
        super().__init__()
        self.setupUi(self)  # Инициализация дизайна
        self.setWindowIcon(QtGui.QIcon('main_icon.jpg'))  # Иконка
        # Переменные
        self.mode = self.comboBox.currentText()
        self.coeff_resist = float(self.lE_coeff_resist.text())
        self.start_v = float(self.lE_start_v.text())
        self.angle = float(self.lE_angle.text())
        self.height = float(self.lE_height.text())
        # Создаем экземпляры классов графиков
        self.base_graph = Base()
        self.extra_graph = Extra()
        self.spec_graph = Spec()
        # Сигналы кнопок
        self.btn_image.clicked.connect(self.create_image)
        self.btn_spec_mode.clicked.connect(self.spec_mode)
        # Тик-так
        self.DataUpdateTimer = QtCore.QTimer()
        self.DataUpdateTimer.timeout.connect(self.update_parameters)
        self.DataUpdateTimer.start(1000)

    def create_image(self):
        self.base_graph.re_create_arrays(self.start_v, self.angle, self.height)
        connect.x, connect.y = self.base_graph.get_arrays()
        connect.flag += 1
        pass

    def spec_mode(self):
        # self.test()
        pass

    # def test(self):
    #     print("#1 {0}\n#2 {1}\n#3 {2}\n#4 {3}\n#5 {4}\n".format(self.mode, self.coeff_resist, self.start_v, self.angle, self.height))

    def update_parameters(self):
        # Обновляем параметры
        self.mode = self.comboBox.currentText()
        value = read_line(self.lE_coeff_resist.text())
        if value[1]:
            self.coeff_resist = value[0]
            connect.coeff_resist = value[0]
        else:
            self.lE_coeff_resist.setText('')
            self.lE_coeff_resist.setPlaceholderText('Error')
        value = read_line(self.lE_start_v.text())
        if value[1]:
            self.start_v = value[0]
            connect.start_v = value[0]
        else:
            self.lE_start_v.setText('')
            self.lE_start_v.setPlaceholderText('Error')
        value = read_line(self.lE_angle.text())
        if value[1]:
            self.angle = value[0]
            connect.angle = value[0]
        else:
            self.lE_angle.setText('')
            self.lE_angle.setPlaceholderText('Error')
        value = read_line(self.lE_height.text())
        if value[1]:
            self.height = value[0]
            connect.height = value[0]
        else:
            self.lE_height.setText('')
            self.lE_height.setPlaceholderText('Error')
        connect.x, connect.y = self.base_graph.get_arrays()
        pass


class Frames(QtWidgets.QMainWindow, main_graphs_1.Ui_MainWindow):
    def __init__(self, connect):
        super().__init__()
        self.setupUi(self)  # Инициализация дизайна
        self.setWindowIcon(QtGui.QIcon('main_icon.jpg'))  # Иконка
        # Переменные
        self.coeff_resist = 0
        self.start_v = 0
        self.angle = 0
        self.heigth = 0
        self.x = []
        self.y = []
        self.flag = 0
        self.previous = 0
        # Layouts
        self.frame_1_layout = pc.Layout(self.frame_1, self.x, self.y)
        self.frame_1.setLayout(self.frame_1_layout)
        # Тик-так
        self.DataUpdateTimer = QtCore.QTimer()
        self.DataUpdateTimer.timeout.connect(self.update_from_connect)
        self.DataUpdateTimer.start(1000)

    def update_from_connect(self):
        self.coeff_resist = connect.coeff_resist
        self.start_v = connect.coeff_resist
        self.angle = connect.angle
        self.heigth = connect.height
        self.x = connect.x
        self.y = connect.y
        self.flag = connect.flag
        print(self.flag)
        print(self.previous)
        if self.previous != self.flag:
            self.frame_1_layout.draw(self.x, self.y)
            self.frame_1.setLayout(self.frame_1_layout)
            self.previous = self.flag
        pass


class Connect:
    flag = 0
    coeff_resist = 0
    start_v = 0
    angle = 0
    height = 0
    x = []
    y = []
    def __init__(self):
        pass


class Base:
    def __init__(self, start_v=10, angle=45, height=20):
        self.start_v = start_v
        self.angle = angle
        self.height = height
        self.x, self.y = self.create_arrays(self.start_v, self.angle, self.height)

    def create_arrays(self, start_v, angle, height):
        # Высчитываем время полета
        b = np.sqrt(np.power(start_v, 2)*np.power(np.sin(angle), 2) + 2*G*height)
        time = (start_v*np.sin(angle) + b)/G
        t = np.linspace(0, time, 1000)
        x = np.zeros(len(t))
        y = np.zeros(len(t))
        i = 0
        for m in t:
            x_val = start_v*np.cos(angle)*m
            y_val = height + start_v*np.sin(angle)*m - (G*np.power(m, 2))/2
            x[i] = x_val
            y[i] = y_val
            i += 1
        # print(time)
        # print(t)
        # print(x)
        # print(y)
        return x, y

    def re_create_arrays(self, start_v, angle, height):
        self.x, self.y = self.create_arrays(start_v, angle, height)

    def get_arrays(self):
        return self.x, self.y


class Extra:
    pass


class Spec:
    pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # window = MainWindow()
    connect = Connect()
    frames = Frames(connect)
    frames.show()
    menu = Menu(connect)
    menu.show()
    # window.show()
    app.exec_()