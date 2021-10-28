import sys
import main_menu
import main_graphs_1
import numpy as np
import plot_canvas as pc
from PyQt5 import QtWidgets, QtGui, QtCore


G = 9.80665

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
        connect.mode = self.comboBox.currentText()
        connect.coeff_resist = float(self.lE_coeff_resist.text())
        connect.start_v = float(self.lE_start_v.text())
        connect.angle = float(self.lE_angle.text())
        connect.height = float(self.lE_height.text())
        # Создаем экземпляры классов графиков
        connect.base_graph = Base()
        connect.extra_graph = Extra()
        connect.spec_graph = Spec()
        # Сигналы кнопок
        self.btn_image.clicked.connect(self.create_image)
        self.btn_spec_mode.clicked.connect(self.spec_mode)
        # Тик-так
        self.DataUpdateTimer = QtCore.QTimer()
        self.DataUpdateTimer.timeout.connect(self.update_parameters)
        self.DataUpdateTimer.start(1000)

    def create_image(self):
        connect.base_graph.re_create_arrays(connect.start_v, connect.angle, connect.height, connect.mode, connect.coeff_resist)
        connect.x, connect.y = connect.base_graph.get_arrays()
        connect.flag += 1
        # print("###frame###")
        # print("{0}\n{1}\n{2}\n{3}\n{4}".format(connect.coeff_resist, connect.start_v, connect.angle, connect.height, connect.mode))
        pass

    def spec_mode(self):
        # self.test()
        pass

    # def test(self):
    #     print("#1 {0}\n#2 {1}\n#3 {2}\n#4 {3}\n#5 {4}\n".format(self.mode, self.coeff_resist, self.start_v, self.angle, self.height))

    def update_parameters(self):
        # Обновляем параметры
        connect.mode = self.comboBox.currentText()
        value = read_line(self.lE_coeff_resist.text())
        if value[1]:
            connect.coeff_resist = value[0]
        else:
            self.lE_coeff_resist.setText('')
            self.lE_coeff_resist.setPlaceholderText('Error')
        value = read_line(self.lE_start_v.text())
        if value[1]:
            connect.start_v = value[0]
        else:
            self.lE_start_v.setText('')
            self.lE_start_v.setPlaceholderText('Error')
        value = read_line(self.lE_angle.text())
        if value[1]:
            connect.angle = value[0]
        else:
            self.lE_angle.setText('')
            self.lE_angle.setPlaceholderText('Error')
        value = read_line(self.lE_height.text())
        if value[1]:
            connect.height = value[0]
        else:
            self.lE_height.setText('')
            self.lE_height.setPlaceholderText('Error')
        pass


class Frames(QtWidgets.QMainWindow, main_graphs_1.Ui_MainWindow):
    def __init__(self, connect):
        super().__init__()
        self.setupUi(self)  # Инициализация дизайна
        self.setWindowIcon(QtGui.QIcon('main_icon.jpg'))  # Иконка
        # Переменные
        self.flag = 0
        self.previous = 0
        # Layouts
        self.frame_1_layout = pc.Layout(self.frame_1, connect.x, connect.y)
        self.frame_1.setLayout(self.frame_1_layout)
        # Тик-так
        self.DataUpdateTimer = QtCore.QTimer()
        self.DataUpdateTimer.timeout.connect(self.update_from_connect)
        self.DataUpdateTimer.start(1000)

    def update_from_connect(self):
        self.flag = connect.flag
        print(self.flag)
        print(self.previous)
        if self.previous != self.flag:
            self.frame_1_layout.draw(connect.x, connect.y)
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
    base_graph = None
    extra_graph = None
    spec_graph = None
    mode = ''

    def __init__(self):
        pass


class Base:
    def __init__(self, start_v=10, angle=60, height=20, mode='Без силы трения', coeff_resist=0.9):
        self.start_v = start_v
        self.angle = angle
        self.height = height
        self.mode = mode
        self.x, self.y = self.create_arrays(self.start_v, self.angle, self.height, mode, coeff_resist)

    def create_arrays(self, start_v, angle, height, mode, coeff_resist):
        # Высчитываем примерное время полета
        b = np.sqrt(np.power(start_v, 2)*np.power(np.sin(np.deg2rad(angle)), 2) + 2*G*height)
        print(start_v, np.sin(np.deg2rad(angle)), b, G)
        time = (start_v*np.sin(np.deg2rad(angle)) + b)/G
        print('time: {0}'.format(time))
        if mode == 'Без силы трения':
            return self.simple_arrays(time, start_v, angle, height)
        else:
            return self.hard_arrays(time, start_v, angle, height, coeff_resist)

    def simple_arrays(self, time, start_v, angle, height):
        t = np.linspace(0, time, 1000)
        x = np.zeros(len(t))
        y = np.zeros(len(t))
        i = 0
        for m in t:
            x_val = start_v * np.cos(np.deg2rad(angle)) * m
            y_val = height + start_v * np.sin(np.deg2rad(angle)) * m - (G * np.power(m, 2)) / 2
            x[i] = x_val
            y[i] = y_val
            i += 1
        period = time / 1000
        print('end {0}'.format(y[-1]))
        if y[999] == 0:
            return x, y
        else:
            m = time + 1 * period
            y_temp = height + start_v * np.sin(np.deg2rad(angle)) * m - (G * np.power(m, 2)) / 2
            if y_temp < 0:
                return x, y
            else:
                i = 1
                y_val = t[999]
                while y_val > 0:
                    m = time + i * period
                    x_val = start_v * np.cos(np.deg2rad(angle)) * m
                    y_val = height + start_v * np.sin(np.deg2rad(angle)) * m - (G * np.power(m, 2)) / 2
                    x = np.append(x, x_val)
                    y = np.append(y, y_val)
                    # print(len(y))
                    i += 1
                # print(len(y))
                # print('end {0}'.format(y[-1]))
                return x, y

    def hard_arrays(self, time, start_v, angle, height, coeff_resist):
        t = np.linspace(0, time, 1000)
        x = np.zeros(len(t))
        y = np.zeros(len(t))
        i = 0
        for m in t:
            b = 1 - np.exp(-((coeff_resist*m)/0.1))
            c = 0.1/coeff_resist
            x_val = start_v * np.cos(np.deg2rad(angle)) * c * b
            y_val = height + c * ((start_v * np.sin(np.deg2rad(angle)) + ((0.1*G)/coeff_resist)) * b - G*m)
            x[i] = x_val
            y[i] = y_val
            i += 1
        period = time / 1000
        print('end {0}'.format(y[-1]))
        if y[999] == 0:
            return x, y
        else:
            m = time + 1 * period
            y_temp = height + (0.1/coeff_resist) * ((start_v * np.sin(np.deg2rad(angle)) + ((0.1*G)/coeff_resist)) * (1 - np.exp(-((coeff_resist*m)/0.1))) - G*m)
            if y_temp < 0:
                return x, y
            else:
                i = 1
                y_val = t[999]
                while y_val > 0:
                    m = time + i * period
                    b = 1 - np.exp(-((coeff_resist * m) / 0.1))
                    c = 0.1 / coeff_resist
                    x_val = start_v * np.cos(np.deg2rad(angle)) * c * b
                    y_val = height + c * ((start_v * np.sin(np.deg2rad(angle)) + ((0.1*G)/coeff_resist)) * b - G*m)
                    x = np.append(x, x_val)
                    y = np.append(y, y_val)
                    # print(len(y))
                    i += 1
                # print(len(y))
                # print('end {0}'.format(y[-1]))
                return x, y

    def re_create_arrays(self, start_v, angle, height, mode, coeff_resist):
        self.x, self.y = self.create_arrays(start_v, angle, height, mode, coeff_resist)

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