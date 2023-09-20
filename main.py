from PyQt5.QtWidgets import QApplication

from UI import MainWidget

if __name__ == '__main__':
    app = QApplication([])

    window = MainWidget('Задача о ферзях', (1000, 800))

    window.show()
    app.exec_()