from PyQt5 import QtCore, QtGui, QtWidgets

LEVEL_MODE_EXAMPLE_STRING = '''
Statistics
LEVEL FILE ...
...

Table of ranges: Types
Types  No. of Files
71       1

Table of ranges: Groups
Groups  No. of Files
42         1

...
...
...
'''

EDITOR_MODE_EXAMPLE_STRING = '''
Statistics
0 words
0 sentences
0 words per sentences
'''


class ProgressBar(QtWidgets.QProgressBar):
    def __init__(self, parent=None, value=None, color=None):
        super().__init__(parent)

        self.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVertical_Mask)

        if value is not None:
            self.setValue(value)

        if color is not None:
            self.setStyleSheet(
                'QProgressBar::chunk {background-color: ' + color + '}')


class LevelTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initGrids()
        self.initForms()
        self.initTextBrowser()

        self.vbox = QtWidgets.QVBoxLayout(self)
        self.vbox.addLayout(self.grids)
        self.vbox.addSpacing(50)
        self.vbox.addLayout(self.forms)
        self.vbox.addWidget(self.textBrowser)

    @property
    def editor(self):
        return self.parent().parent().parent()

    def initGrids(self):
        self.grids = QtWidgets.QGridLayout()

        # Token Coverage
        self.tokenCoverageLabel = QtWidgets.QLabel('Token Coverage')
        self.tokenCoverageProgBar = ProgressBar(self, 0, '#278da9')
        self.grids.addWidget(self.tokenCoverageLabel, 0, 0, 1, 4)
        self.grids.addWidget(self.tokenCoverageProgBar, 1, 0, 1, 4)

        # Level Coverage
        self.levelCoverageLabel = QtWidgets.QLabel('Level Coverage')

        self.levelNoneButton = QtWidgets.QPushButton()
        self.levelNoneButton.setFlat(True)
        self.levelNoneButton.setText('Non-level')
        self.levelNoneProgBar = ProgressBar(
            self, 0, self.editor.formatManager.LEVEL_FORMAT_COLORS[None])

        self.level1Button = QtWidgets.QPushButton()
        self.level1Button.setFlat(True)
        self.level1Button.setText('Level 1')
        self.level1ProgBar = ProgressBar(
            self, 0, self.editor.formatManager.LEVEL_FORMAT_COLORS[1])

        self.level2Button = QtWidgets.QPushButton()
        self.level2Button.setFlat(True)
        self.level2Button.setText('Level 2')
        self.level2ProgBar = ProgressBar(
            self, 0, self.editor.formatManager.LEVEL_FORMAT_COLORS[2])

        self.level3Button = QtWidgets.QPushButton()
        self.level3Button.setFlat(True)
        self.level3Button.setText('Level 3')
        self.level3ProgBar = ProgressBar(
            self, 0, self.editor.formatManager.LEVEL_FORMAT_COLORS[3])

        # Checkboxes
        self.levelNoneCheckbox = QtWidgets.QCheckBox()
        self.level1Checkbox = QtWidgets.QCheckBox()
        self.level2Checkbox = QtWidgets.QCheckBox()
        self.level3Checkbox = QtWidgets.QCheckBox()

        for checkbox in (self.levelNoneCheckbox, self.level1Checkbox,
                         self.level2Checkbox, self.level3Checkbox):
            checkbox.clicked.connect(self.editor.refreshView)

        self.levelCoverages = [
            [self.levelNoneCheckbox, self.levelNoneButton, self.levelNoneProgBar],
            [self.level1Checkbox, self.level1Button, self.level1ProgBar],
            [self.level2Checkbox, self.level2Button, self.level2ProgBar],
            [self.level3Checkbox, self.level3Button, self.level3ProgBar],
        ]
        self.grids.addWidget(self.levelCoverageLabel, 2, 0, 1, 4)

        for i, levelCoverage in enumerate(self.levelCoverages):
            row = 3 + i
            self.grids.addWidget(levelCoverage[0], row, 0, 1, 1)
            self.grids.addWidget(levelCoverage[1], row, 1, 1, 1)
            self.grids.addWidget(levelCoverage[2], row, 2, 1, 2)

    def initForms(self):
        self.forms = QtWidgets.QFormLayout()

        self.statisticsLabel = QtWidgets.QLabel('Statistics')
        self.forms.addRow(self.statisticsLabel)
        self.forms.addRow(QtWidgets.QCheckBox(),
                          QtWidgets.QLabel('Word Types'))
        self.forms.addRow(QtWidgets.QCheckBox(),
                          QtWidgets.QLabel('Word Groups (Families)'))
        self.forms.addRow(QtWidgets.QCheckBox(),
                          QtWidgets.QLabel('Include Complete Frequency List'))

    def initTextBrowser(self):
        self.textBrowser = QtWidgets.QTextBrowser()
        self.textBrowser.setText(LEVEL_MODE_EXAMPLE_STRING)


class EditorTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initErrorGrids()
        self.initErrorList()
        self.initCoverageGrids()
        self.initTextBrowser()

        self.vbox = QtWidgets.QVBoxLayout(self)
        self.vbox.addLayout(self.errorGrids)
        self.vbox.addWidget(self.errorList)
        self.vbox.addSpacing(50)
        self.vbox.addLayout(self.coverageGrids)
        self.vbox.addWidget(self.textBrowser)

    @property
    def editor(self):
        return self.parent().parent().parent()

    def initErrorGrids(self):
        self.errorGrids = QtWidgets.QGridLayout()

        self.errorTypes = [
            [QtWidgets.QLabel('Concision'), 3, 'darkred'],
            [QtWidgets.QLabel('Clarity'), 5, 'darkblue'],
            [QtWidgets.QLabel('Logic'), 3, 'darkgreen']
        ]
        for i, errorType in enumerate(self.errorTypes):
            self.errorGrids.addWidget(errorType[0], 0, i)
            self.errorGrids.addWidget(
                QtWidgets.QPushButton(
                    styleSheet='font-weight: 900; font-size: 20px;'
                               'border: 5px solid ' + errorType[2],
                    text=str(errorType[1]),
                    minimumHeight=50
                ), 1, i)

    def initErrorList(self):
        self.errorList = QtWidgets.QListWidget(self)
        self.errorList.addItem('Error1')
        self.errorList.addItem('Error2')
        self.errorList.addItem('Error3')
        self.errorList.addItem('Error4')

    def initCoverageGrids(self):
        self.firstFreqCheckbox = QtWidgets.QCheckBox()
        self.firstFreqLabel = QtWidgets.QLabel()
        self.firstFreqProgBar = ProgressBar(self, 0, '#363d5c')
        self.secondFreqCheckbox = QtWidgets.QCheckBox()
        self.secondFreqLabel = QtWidgets.QLabel()
        self.secondFreqProgBar = ProgressBar(self, 0, '#87a840')
        self.thirdFreqCheckbox = QtWidgets.QCheckBox()
        self.thirdFreqLabel = QtWidgets.QLabel()
        self.thirdFreqProgBar = ProgressBar(self, 0, '#ddc328')

        for checkbox in (self.firstFreqCheckbox, self.secondFreqCheckbox,
                         self.thirdFreqCheckbox):
            checkbox.clicked.connect(self.editor.refreshView)

        self.coverageGrids = QtWidgets.QGridLayout()
        self.coverageLabel = QtWidgets.QLabel('Coverages')
        self.coverages = [
            [self.firstFreqCheckbox, self.firstFreqLabel, self.firstFreqProgBar],
            [self.secondFreqCheckbox, self.secondFreqLabel, self.secondFreqProgBar],
            [self.thirdFreqCheckbox, self.thirdFreqLabel, self.thirdFreqProgBar]
        ]
        self.coverageGrids.addWidget(self.coverageLabel, 0, 0, 1, 4)
        for i, coverage in enumerate(self.coverages):
            row = i + 1
            self.coverageGrids.addWidget(coverage[0], row, 0, 1, 1)
            self.coverageGrids.addWidget(coverage[1], row, 1, 1, 1)
            self.coverageGrids.addWidget(coverage[2], row, 2, 1, 2)

    def initTextBrowser(self):
        self.textBrowser = QtWidgets.QTextBrowser()
        self.textBrowser.setText(EDITOR_MODE_EXAMPLE_STRING)
