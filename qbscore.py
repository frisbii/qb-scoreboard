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
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont, QFontDatabase

PLAYER_COLOURS = {
    1: "#DAE3F3",
    2: "#E2F0D9",
    3: "#fff2cc",
    4: "#fbe5d6"
}

class qbGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QB Scorekeeper")

        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)

        #self._centralWidget.setAttribute(Qt.WA_StyledBackground, True)
        #self._centralWidget.setStyleSheet("background-color:yellow")

        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self._createScoreboard()
        self.generalLayout.addStretch()
        self._createButtons()

    def _createScoreboard(self):
        self.scoreboard = QHBoxLayout()

        # Creating the round number column
        self.rounds = QVBoxLayout()
        roundHeader = QLabel("Rnd #")
        roundHeader.setStyleSheet("font-size:16px")
        self.rounds.addWidget(roundHeader)
        self.scoreboard.addLayout(self.rounds, 1)

        # Creating the player columns
        playerNames = ["Maritte", "Safina", "Gilda", "Petronella"]
        for name in playerNames:
            self.scoreboard.addWidget(player(name), 3)

        # Adding the scoreboard to the general layout
        self.generalLayout.addLayout(self.scoreboard)

    def _createButtons(self):
        self.buttons = QHBoxLayout()
        self.btnBack = QPushButton("Back")
        self.btnBack.setFixedHeight(50)
        self.btnContinue = QPushButton("Continue")
        self.btnContinue.setFixedHeight(50)
        self.buttons.addWidget(self.btnBack)
        self.buttons.addWidget(self.btnContinue)

        self.generalLayout.addLayout(self.buttons)

class player(QWidget):
    def __init__(self, name):
        super().__init__()
        #self.setAttribute(Qt.WA_StyledBackground, True)
        #self.setStyleSheet("background-color:red")
        self.objectName = name
        self.playerLayout = QVBoxLayout()

        self._createLabel()

        self.setLayout(self.playerLayout)

    def _createLabel(self):
        self.nameHeader = QLabel(self.objectName)
        self.nameHeader.setStyleSheet("background-color:#DAE3F3; font-weight:bold; font-size:30px")
        self.playerLayout.addWidget(self.nameHeader)

def main():
    # Create instance of QApplication
    app = QApplication(sys.argv)

    # Load in and set default font
    id = QFontDatabase.addApplicationFont("fonts/Montserrat-Bold.ttf")
    app.setStyleSheet("QLabel { font-family:Montserrat; font-size:16px }")

    # Show the GUI
    view = qbGui()
    view.show()

    # Execute the program event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
