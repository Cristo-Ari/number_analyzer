from PyQt5 import QtWidgets, QtCore  # Импортируем QtCore для использования Qt.Horizontal
from PyQt5.QtWidgets import QFileDialog, QVBoxLayout, QPushButton, QSlider, QLabel
import pyqtgraph as pg
import sys
import numpy as np
import time

class PiDigitAnimation(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        # Инициализация пользовательского интерфейса
        self.setWindowTitle("Анимация цифр числа Pi")
        self.layout = QVBoxLayout()
        
        # Кнопки управления
        self.play_pause_button = QPushButton('Пауза')
        self.play_pause_button.clicked.connect(self.toggle_animation)
        self.layout.addWidget(self.play_pause_button)
        
        self.reset_button = QPushButton('Сброс')
        self.reset_button.clicked.connect(self.reset_animation)
        self.layout.addWidget(self.reset_button)
        
        # Ползунок для регулировки скорости
        self.speed_label = QLabel('Скорость')
        self.layout.addWidget(self.speed_label)
        self.speed_slider = QSlider()
        self.speed_slider.setOrientation(QtCore.Qt.Horizontal)  # Исправлено на QtCore.Qt.Horizontal
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(1000)
        self.speed_slider.setValue(100)
        self.speed_slider.valueChanged.connect(self.update_speed)
        self.layout.addWidget(self.speed_slider)
        
        # График
        self.graph_widget = pg.PlotWidget()
        self.layout.addWidget(self.graph_widget)
        self.setLayout(self.layout)
        
        # Настройка графика
        self.bars = pg.BarGraphItem(x=np.arange(10), height=np.zeros(10), width=0.6, brush='b')
        self.graph_widget.addItem(self.bars)
        self.graph_widget.setYRange(0, 500)
        self.graph_widget.setTitle("Частота появления цифр")
        self.graph_widget.setLabel('left', 'Количество повторений')
        self.graph_widget.setLabel('bottom', 'Цифры')
        
        # Логические переменные
        self.animation_running = True
        self.speed = 100
        self.digit_counts = np.zeros(10)
        
        # Чтение файла
        self.file_path = self.open_file()
        self.digit_reader = self.read_digits_from_file(self.file_path)
        
        # Таймер для анимации
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(self.speed)
    
    def open_file(self):
        # Диалог выбора файла
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Выберите файл с числами", "", "Text files (*.txt)")
        return file_path

    def read_digits_from_file(self, file_path):
        # Чтение цифр из файла
        with open(file_path, 'r') as f:
            digits = f.read()
            for digit in digits:
                if digit.isdigit():
                    yield int(digit)

    def update_graph(self, digit):
        # Обновление графика
        self.digit_counts[digit] += 1
        self.bars.setOpts(height=self.digit_counts)
        self.graph_widget.setYRange(0, max(self.digit_counts) + 10)
    
    def animate(self):
        # Анимация
        if self.animation_running:
            try:
                digit = next(self.digit_reader)
                self.update_graph(digit)
            except StopIteration:
                self.timer.stop()

    def toggle_animation(self):
        # Пауза/Старт анимации
        if self.animation_running:
            self.animation_running = False
            self.play_pause_button.setText("Старт")
        else:
            self.animation_running = True
            self.play_pause_button.setText("Пауза")

    def reset_animation(self):
        # Сброс анимации
        self.digit_counts = np.zeros(10)
        self.digit_reader = self.read_digits_from_file(self.file_path)
        self.animation_running = True
        self.play_pause_button.setText("Пауза")
        self.timer.start(self.speed)
    
    def update_speed(self):
        # Обновление скорости анимации
        self.speed = self.speed_slider.value()
        self.timer.setInterval(self.speed)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = PiDigitAnimation()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
