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
        self.setFixedWidth(1400)

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
        roundHeader = QLabel("Round")
        roundHeader.setStyleSheet("font-size:16px")
        self.rounds.addWidget(roundHeader)
        # self.scoreboard.addLayout(self.rounds, 1) !!! <<< round num column disabled for now

        # Creating the player columns
        playerNames = ["Maritte", "Safina", "Gilda", "Petronella"]
        for i, name in enumerate(playerNames):
            # Adds a new player widget to the scoreboard for every passed player
            self.scoreboard.addWidget(player(name, i), 3)

        # Adding the scoreboard to the general layout
        self.generalLayout.addLayout(self.scoreboard)

    def _createNavButtons(self):
        """Creates the navigation buttons at the bottom of the main window"""
        self.buttons = QHBoxLayout()

        for l in ["Back", "Continue"]:
            button = QPushButton(l)
            button.setFixedHeight(50)
            self.buttons.addWidget(button)

        self.generalLayout.addLayout(self.buttons)

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("Round 1")
        self.setStatusBar(status)

class player(QWidget):
    """Defines the player columns of the scoreboard"""
    def __init__(self, name, number):
        """Player widget initialization"""
        super().__init__()
        # Gives the player widget object a name and number
        self.objectName = name
        self.playerNumber = number

        # Sets a background colour for the player widget
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f"player {{ background-color:{PLAYER_COLOURS[self.playerNumber].replace('x', '85%')} }}")

        self.playerLayout = QVBoxLayout()
        # Sets the margins around the player widget
        self.playerLayout.setContentsMargins(5,5,5,5) # L T R B

        # Creates each part of the player widget: player label, player stats, scoring buttons
        self._createLabel()
        self._createStats()
        self._createScoring()

        self.setLayout(self.playerLayout)

    def _createLabel(self):
        """Creates the label object at the top of the player widget"""
        self.nameHeader = QLabel(self.objectName)
        self.nameHeader.setStyleSheet("font-family:Montserrat; font-weight:bold; font-size:30px")
        self.nameHeader.setAlignment(Qt.AlignCenter)
        self.playerLayout.addWidget(self.nameHeader)

    def _createStats(self):
        """Creates the stats widget in the middle of the player widget"""
        self.stats_w = QWidget(self)
        # Sets the colour to be slightly brighter than the rest of the widget
        self.stats_w.setStyleSheet(f"""background-color:{PLAYER_COLOURS[self.playerNumber].replace('x', '95%')};
            font-family:Cascadia Mono; font-weight:200""")
        self.stats = QHBoxLayout()

        # Creates the two columns of stats using the QForm layout
        self.col1Stats = QFormLayout()
        self.col2Stats = QFormLayout()
        for i, col in enumerate([["TUC", "TN", "TUA"], ["BC", "BA", "TS"]]):
            for l in col:
                stat = QLineEdit()
                stat.objectName = l
                stat.setAlignment(Qt.AlignCenter)
                stat.setReadOnly(True)
                if i == 0:
                    self.col1Stats.addRow(l, stat)
                else:
                    self.col2Stats.addRow(l, stat)

        self.stats.addLayout(self.col1Stats)
        self.stats.addLayout(self.col2Stats)
        self.stats_w.setLayout(self.stats)
        self.playerLayout.addWidget(self.stats_w)

    def _createScoring(self):
        """Creates the scoring buttons and checkboxes"""
        self.scoring = QHBoxLayout()

        # Creates a button for each point value of a tossup
        for p in ["-5", "10", "15"]:
            button = QPushButton(p)
            button.objectName = p
            button.setCheckable(True)
            # Sets negs to be red if selected and correct points to be green
            if p == "-5":
                button.setStyleSheet("QPushButton:checked{background-color:#f55442; border:1px solid; border-radius:6px; padding: 6px}")
            else:
                button.setStyleSheet("QPushButton:checked{background-color:#54f542; border:1px solid; border-radius:6px; padding: 6px}")
            self.scoring.addWidget(button)

        # Creates a checkbox for each bonus question
        for i in ["1", "2", "3"]:
            check = QCheckBox()
            check.objectName = i
            self.scoring.addWidget(check)

        self.playerLayout.addLayout(self.scoring)

def main():
    # Create instance of QApplication
    app = QApplication(sys.argv)

    # Load in and set default font
    id = QFontDatabase.addApplicationFont("assets/Montserrat-Bold.ttf")

    # Show the GUI
    view = qbGui()
    view.show()

    # Execute the program event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
