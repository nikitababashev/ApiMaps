import requests
import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt
import os
from mapd import Ui_Form


WIDTH, HEIGHT = 600, 500


class MyWidget(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.delt = '0.005'
        self.setupUi(self)
        self.setWindowTitle('Карта')
        self.ready.clicked.connect(self.createmaps)

    def createmaps(self):
        coords = self.coords.text().split()
        map_api_server = 'http://static-maps.yandex.ru/1.x/'
        map_params = {
            'll': ','.join(coords),
            'spn': ','.join([self.delt, self.delt]),
            'l': 'map'
        }
        response = requests.get(map_api_server, params=map_params)

        if not response:
            print('Код ошибки:', response.status_code)
            sys.exit()

        self.map_file = 'map.png'
        with open(self.map_file, 'wb') as file:
            file.write(response.content)

        self.initUI()
        self.delta.setText(f'Масштаб: {self.delt[:5]}')

    def initUI(self):
        pixmap = QPixmap(self.map_file)
        self.map.setPixmap(pixmap)

    def closeEvent(self, event):
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp and float(self.delt) > 0.005:
            self.delt = str(float(self.delt) - 0.05)
            self.createmaps()
        if event.key() == Qt.Key_PageDown and float(self.delt) < 45:
            self.delt = str(float(self.delt) + 0.05)
            self.createmaps()


app = QApplication(sys.argv)
widget = MyWidget()
widget.show()
sys.exit(app.exec())
