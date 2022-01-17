import sys

from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QButtonGroup,

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

STAT_CATEGORIES = ["TUC", "TUN", "TUA", "BC", "PPTU", "TS"]

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
        self._createPlayerspace()
        self.generalLayout.addStretch()
        self._createNavButtons()
        self._createStatusBar()

        self.setFixedWidth(350 * len(self.playerObjects))

    def _createMenu(self):
        """Creates the menu bar of the central window"""
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction('&Exit', self.close)

    def _createPlayerspace(self):
        """Creates the playerspace; a horizontal set of playerwidgets"""
        self.playerspace = QHBoxLayout()
        self.playerspace.setSpacing(0)

        # Creating the player columns
        self.playerObjects = {}
        playerNames = ["Maritte", "Safina", "Gilda"]
        for i, name in enumerate(playerNames):
            self.playerObjects[name] = player(name, i)
            self.playerspace.addWidget(self.playerObjects[name], 3)

        # Adding the scoreboard to the general layout
        self.generalLayout.addLayout(self.playerspace)

    def _createNavButtons(self):
        """Creates the navigation buttons at the bottom of the main window"""
        self.navLayout = QHBoxLayout()

        self.navButtons = {}
        for l in ["Back", "Continue"]:
            button = QPushButton(l)
            button.setFixedHeight(50)
            self.navButtons[l] = button
            self.navLayout.addWidget(button)

        self.generalLayout.addLayout(self.navLayout)

    def _createStatusBar(self):
        self.status = QStatusBar()
        self.status.showMessage("Waiting to start...")
        self.setStatusBar(self.status)

    def setTossup(self, n):
        self.status.showMessage(f"Tossup {str(n)}")

class qbController:
    """Controller portion of the program"""
    def __init__(self, model, view):
        """Controller initializer"""
        self._model = model
        self._view = view

        self._connectSignals()

    def _tossupEvent(self, playerObj, button):
        if playerObj.scorecard[self._model.tossup][0] == int(playerObj.tossupButtons.id(button)):
            self._deselectAllButtons(playerObj.tossupButtons)
            playerObj.scorecard[self._model.tossup][0] = 0
        else:
            playerObj.scorecard[self._model.tossup][0] = int(playerObj.tossupButtons.id(button))
        self._updateStats(playerObj)

    def _bonusEvent(self, playerObj, check):
        playerObj.scorecard[self._model.tossup][1][int(playerObj.bonusButtons.id(check)) - 1] = 10 if check.isChecked() else 0
        self._updateStats(playerObj)

    def _updateStats(self, playerObj):
        for stat in STAT_CATEGORIES:
            value = self._model.evaluateStat(playerObj.scorecard, stat)
            playerObj.setStatsText(stat, value)

    def _setupNewRound(self):
        if self._model.tossup == self._model.latest:
            self._model.newRound(self._view.playerObjects)
        else:
            self._model.tossup += 1
        self._view.setTossup(self._model.tossup)
        for _, playerObj in self._view.playerObjects.items():
            self._updateStats(playerObj)
        self._loadScoringStates()

    def _setupBackRound(self):
        self._model.tossup -= 1
        self._view.setTossup(self._model.tossup)
        for _, playerObj in self._view.playerObjects.items():
            self._updateStats(playerObj)
        self._loadScoringStates()

    def _deselectAllButtons(self, buttonGroup, exclusive=1):
        # Very clunky workaround to unselect button if it is already pressed
        # AFAIK, quirk of the AbstractButton exclusive property
        buttonGroup.setExclusive(False)
        for button in buttonGroup.buttons():
            button.setChecked(False)
        if exclusive:
            buttonGroup.setExclusive(True)

    def _loadScoringStates(self):
        t = self._model.tossup
        for _, playerObj in self._view.playerObjects.items():
            self._deselectAllButtons(playerObj.tossupButtons)
            if playerObj.scorecard[t][0] != 0:
                playerObj.tossupButtons.button(playerObj.scorecard[t][0]).setChecked(True)

            self._deselectAllButtons(playerObj.bonusButtons, 0)
            for i, score in enumerate(playerObj.scorecard[t][1]):
                if score == 10:
                    playerObj.bonusButtons.button(i + 1).setChecked(True)

    def _connectSignals(self):
        """Connect signals and slots"""
        # self.navObjects["Continue"].clicked.connect(self.playerObjects["Maritte"].resetScoring)
        for _, playerObj in self._view.playerObjects.items():
            for button in playerObj.tossupButtons.buttons():
                button.clicked.connect(partial(self._tossupEvent, playerObj, button))
            for check in playerObj.bonusButtons.buttons():
                check.clicked.connect(partial(self._bonusEvent, playerObj, check))
        self._view.navButtons["Continue"].clicked.connect(self._setupNewRound)
        self._view.navButtons["Back"].clicked.connect(self._setupBackRound)


class qbModel:
    def __init__(self):
        self.tossup = 0
        self.latest = 0

    def newRound(self, playerObjs):
        self.tossup += 1
        self.latest += 1
        for _, playerobj in playerObjs.items():
            playerobj.scorecard[self.tossup] = [0, [0, 0, 0]]

    def evaluateStat(self, scorecard, stat):
        v = 0
        for i in range(1, self.tossup + 1):
            row = scorecard[i]
            match stat:
                case "TUC":
                    if row[0] > 0:
                        v += 1
                case "TUN":
                    if row[0] < 0:
                        v += 1
                case "TUA":
                    v = (v * (i-1) + row[0]) / i
                case "BC":
                    v += row[1].count(10)
                case "PPTU":
                    v = (v * (i-1) + row[0] + sum(row[1])) / i
                case "TS":
                    v += row[0] + sum(row[1])
        return round(v, 1)

def main():
    # Create instance of QApplication
    app = QApplication(sys.argv)

    # Load in and set default font
    id = QFontDatabase.addApplicationFont("assets/Montserrat-Bold.ttf")

    # Show the GUI
    view = qbGui()
    view.show()
    # Create instances of the model and the controller
    model = qbModel()
    qbController(model=model, view=view)

    # Execute the program event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
