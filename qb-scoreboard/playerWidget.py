from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,

    QLineEdit,
    QPushButton,
    QLabel,
    QCheckBox,
    QButtonGroup
)

PLAYER_COLOURS = {
    0: "hsl(218, 51%, x)",
    1: "hsl(97, 43%, x)",
    2: "hsl(45, 100%, x)",
    3: "hsl(24, 82%, x)",
    4: "hsl(170, 0%, x)",
    5: "hsl(280, 70%, x)"
}
""" placeholder
    0: "#DAE3F3",
    1: "#E2F0D9",
    2: "#fff2cc",
    3: "#fbe5d6"
"""

class player(QWidget):
    """Defines the player columns of the scoreboard"""
    def __init__(self, name, num):
        """Player widget initialization"""
        super().__init__()
        # Gives the player widget object a name and number
        self.objectName = name
        self.playerNumber = num
        self.scorecard = {}

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
        self.statsObjects = {}
        self.col1Stats = QFormLayout()
        self.col2Stats = QFormLayout()
        for i, col in enumerate([["TUC", "TUN", "TUA"], ["BC", "PPTU", "TS"]]):
            for statName in col:
                statDisp = QLineEdit()
                self.statsObjects[statName] = statDisp
                statDisp.setAlignment(Qt.AlignCenter)
                statDisp.setReadOnly(True)
                if i == 0:
                    self.col1Stats.addRow(statName, statDisp)
                else:
                    self.col2Stats.addRow(statName, statDisp)

        self.stats.addLayout(self.col1Stats)
        self.stats.addLayout(self.col2Stats)
        self.stats_w.setLayout(self.stats)
        self.playerLayout.addWidget(self.stats_w)

    def _createScoring(self):
        """Creates the scoring buttons and checkboxes"""
        self.scoring = QHBoxLayout()

        # Creates a button for each point value of a tossup
        self.tossupButtons = QButtonGroup()
        for p in ["-5", "10", "15"]:
            button = QPushButton(p)
            button.setCheckable(True)
            # Sets negs to be red if selected and correct points to be green
            if p == "-5":
                button.setStyleSheet("QPushButton:checked{background-color:#f55442; border:1px solid; border-radius:6px; padding: 6px}")
            else:
                button.setStyleSheet("QPushButton:checked{background-color:#54f542; border:1px solid; border-radius:6px; padding: 6px}")
            self.tossupButtons.addButton(button, int(p))
            self.scoring.addWidget(button)

        # Creates a checkbox for each bonus question
        self.bonusButtons = QButtonGroup()
        self.bonusButtons.setExclusive(False)
        for i in ["1", "2", "3"]:
            check = QCheckBox()
            self.bonusButtons.addButton(check, int(i))
            self.scoring.addWidget(check)

        self.playerLayout.addLayout(self.scoring)

    def setStatsText(self, stat, value):
        self.statsObjects[stat].setText(str(value))

    def resetScoring(self):
        for label in self.scoringObjects:
            self.scoringObjects[label].setChecked(False)
