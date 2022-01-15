import sys

from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLineEdit

class qbGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QB Scorekeeper")

        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self._createNames()

    def _createNames(self):
        self.names = QHBoxLayout()

        name1 = QLabel("Name 1")


        self.generalLayout.addLayout(self.names)

def main():
    app = QApplication(sys.argv)

    view = qbGui()
    view.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
