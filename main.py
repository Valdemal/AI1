from PyQt5.QtWidgets import QApplication

from UI import MainWidget

DEFAULT_QUEENS_COUNT = 3
DEFAULT_TEMPERATURE = 80

if __name__ == '__main__':
    app = QApplication([])

    window = MainWidget('Задача о ферзях', (1000, 800), DEFAULT_QUEENS_COUNT, DEFAULT_TEMPERATURE)

    window.show()
    app.exec_()
