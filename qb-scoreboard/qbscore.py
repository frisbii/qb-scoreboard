import sys

from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,

    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFormLayout,

    QLineEdit,
    QPushButton,
    QLabel,
    QCheckBox,
    QStatusBar
)
from PyQt5.QtGui import QFont, QFontDatabase, QIcon

from playerWidget import player

PLAYER_COLOURS = {
    0: "hsl(218, 51%, x)",
    1: "hsl(97, 43%, x)",
    2: "hsl(45, 100%, x)",
    3: "hsl(24, 82%, x)"
}
""" placeholder
    0: "#DAE3F3",
    1: "#E2F0D9",
    2: "#fff2cc",
    3: "#fbe5d6"
"""

class qbGui(QMainWindow):
    """View portion of the scoring program"""
    def __init__(self):
        """View initializer"""
        super().__init__()
        # Sets main window properties
        self.setWindowTitle("QB Scorekeeper")
        self.setWindowIcon(QIcon("assets/icon.png"))

        # The central widget is assigned the general layout, formatting the other widgets inside the central one
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self._centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(self._centralWidget)

        # Sets margins and spacing to remove blank space around the widgets
        self.generalLayout.setContentsMargins(0, 0, 0, 0)
        self.generalLayout.setSpacing(0)
        #self._centralWidget.setAttribute(Qt.WA_StyledBackground, True)
        #self._centralWidget.setStyleSheet("background-color:yellow")

        # Creates each portion of the central widget
        # self._createMenu()
        self._createScoreboard()
        self.generalLayout.addStretch()
        self._createNavButtons()
        self._createStatusBar()

        self.setFixedWidth(350 * len(self.playerObjects))

    def _createMenu(self):
        """Creates the menu bar of the central window"""
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction('&Exit', self.close)

    def _createScoreboard(self):
        """Creates the scoreboard of the central window. Round numbers and player columns"""
        self.scoreboard = QHBoxLayout()
        self.scoreboard.setSpacing(0)

        # Creating the round number column
        self.rounds = QVBoxLayout()
        self.roundHeader = QLabel("Round")
        self.roundHeader.setStyleSheet("font-size:16px")
        self.rounds.addWidget(self.roundHeader)
        # self.scoreboard.addLayout(self.rounds, 1) !!! <<< round num column disabled for now

        # Creating the player columns
        self.playerObjects = {}
        playerNames = ["Maritte", "Safina", "Gilda", "Petronella"]
        for i, name in enumerate(playerNames):
            self.playerObjects[name] = player(name, i)
            self.scoreboard.addWidget(self.playerObjects[name], 3)

        # Adding the scoreboard to the general layout
        self.generalLayout.addLayout(self.scoreboard)

    def _createNavButtons(self):
        """Creates the navigation buttons at the bottom of the main window"""
        self.navButtons = QHBoxLayout()

        self.navObjects = {}
        for l in ["Back", "Continue"]:
            button = QPushButton(l)
            button.setFixedHeight(50)
            self.navObjects[l] = button
            self.navButtons.addWidget(button)

        self.generalLayout.addLayout(self.navButtons)

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("Tossup 1")
        self.setStatusBar(status)

class qbController:
    """Controller portion of the program"""
    def __init__(self, model, view):
        """Controller initializer"""
        self._view = view

        self._connectSignals()

    def _connectSignals(self):
        """Connect signals and slots"""
        # self.navObjects["Continue"].clicked.connect(self.playerObjects["Maritte"].resetScoring)
        for playerObj in self._view.playerObjects:
            continue

def main():
    # Create instance of QApplication
    app = QApplication(sys.argv)

    # Load in and set default font
    id = QFontDatabase.addApplicationFont("assets/Montserrat-Bold.ttf")

    # Show the GUI
    view = qbGui()
    view.show()
    # Create instances of the model and the controller
    qbController("", view=view)

    # Execute the program event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
