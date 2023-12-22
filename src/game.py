import random

from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QPalette,
    QFont
)
from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QMessageBox
)

from config import (
    ROW, COL, NUM_MAP_COLOR
)


class Game(QWidget):  #

    def __init__(self):
        super().__init__()

        self.isLose = False
        self.isMove = False
        self.succeed = False
        self.palettes = []
        self.labels = []
        self.UI()

    def UI(self):
        self.setWindowTitle('2048')
        self.setGeometry(0, 0, 400, 400)

        layout = QGridLayout()
        layout.setSpacing(5)
        self.setLayout(layout)

        for i in range(ROW ** 2):
            label = QLabel('0', self)
            label.setAlignment(Qt.AlignCenter)
            label.setFixedWidth(80)
            label.setFixedHeight(80)
            label.setFont(QFont("Arial", 25, QFont.Bold))
            layout.addWidget(label, i // ROW, i % ROW)
            self.labels.append(label)

            pe = QPalette()
            pe.setColor(QPalette.WindowText, NUM_MAP_COLOR['0']['font'])
            label.setAutoFillBackground(True)
            pe.setColor(QPalette.Window, NUM_MAP_COLOR['0']['background'])
            label.setPalette(pe)
            self.palettes.append(pe)

        self.randomSetLabels(3)

        self.show()

    def reset(self):
        for i in range(ROW * COL):
            self.setTextAndColor(i, '0', setIsMove=False)
        self.randomSetLabels(3)

    def keyPressEvent(self, e):
        key_to_move = {
            Qt.Key_Up: 'up',
            Qt.Key_Down: 'down',
            Qt.Key_Left: 'left',
            Qt.Key_Right: 'right',
            Qt.Key_R: 'reset'
        }
        move = key_to_move.get(e.key())
        if move in ('up', 'down', 'left', 'right'):
            self.gridMove(move)
        elif move == 'reset':
            self.reset()

    def gridMove(self, direction):
        self.removeEmptyLabel(direction)
        self.mergeSameLabel(direction)
        if self.isLose:
            self.gameOver()
        if self.succeed:
            self.gameSuccess()
        if self.isMove:
            self.isMove = False
            self.randomSetLabels(1)

    def removeEmptyLabel(self, direction):
        self.isLose = True
        if direction == 'right':
            for i in range(ROW):
                row_point = []
                for j in range(COL - 1, -1, -1):
                    if self.labels[i * ROW + j].text() != '0':
                        row_point.append(self.labels[i * ROW + j].text())
                    else:
                        self.isLose = False
                j = COL - 1
                for text in row_point:
                    self.setTextAndColor(i * ROW + j, text)
                    j -= 1
                while j != -1:
                    self.setTextAndColor(i * ROW + j, '0')
                    j -= 1
        elif direction == 'left':
            for i in range(ROW):
                row_point = []
                for j in range(COL):
                    if self.labels[i * ROW + j].text() != '0':
                        row_point.append(self.labels[i * ROW + j].text())
                    else:
                        self.isLose = False
                j = 0
                for text in row_point:
                    self.setTextAndColor(i * ROW + j, text)
                    j += 1
                while j != COL:
                    self.setTextAndColor(i * ROW + j, '0')
                    j += 1
        elif direction == 'up':
            for j in range(COL):
                row_point = []
                for i in range(ROW):
                    if self.labels[i * ROW + j].text() != '0':
                        row_point.append(self.labels[i * ROW + j].text())
                    else:
                        self.isLose = False
                i = 0
                for text in row_point:
                    self.setTextAndColor(i * ROW + j, text)
                    i += 1
                while i != ROW:
                    self.setTextAndColor(i * ROW + j, '0')
                    i += 1
        elif direction == 'down':
            for j in range(COL):
                col_point = []
                for i in range(ROW - 1, -1, -1):
                    if self.labels[i * ROW + j].text() != '0':
                        col_point.append(self.labels[i * ROW + j].text())
                    else:
                        self.isLose = False
                i = ROW - 1
                for text in col_point:
                    self.setTextAndColor(i * ROW + j, text)
                    i -= 1
                while i != -1:
                    self.setTextAndColor(i * ROW + j, '0')
                    i -= 1

    def mergeSameLabel(self, direction):
        if direction == 'right':
            for j in range(ROW):
                for i in range(COL - 1, 0, -1):
                    right_label = self.labels[j * ROW + i]
                    left_label = self.labels[j * ROW + i - 1]
                    if right_label.text() == left_label.text():
                        num = int(right_label.text())
                        self.finishedMerge(j * ROW + i, num * 2)
                        self.setTextAndColor(j * ROW + i, str(num * 2))
                        for k in range(i - 1, 0, -1):
                            self.setTextAndColor(j * ROW + k, self.labels[j * ROW + k - 1].text())
                        self.setTextAndColor(j * ROW + 0, '0')
                        break
        elif direction == 'left':
            for j in range(ROW):
                for i in range(COL - 1):
                    right_label = self.labels[j * ROW + i + 1]
                    left_label = self.labels[j * ROW + i]
                    if right_label.text() == left_label.text():
                        num = int(left_label.text())
                        self.finishedMerge(j * ROW + i, num * 2)
                        self.setTextAndColor(j * ROW + i, str(num * 2))
                        for k in range(i + 1, COL - 1):
                            self.setTextAndColor(j * ROW + k, self.labels[j * ROW + k + 1].text())
                        self.setTextAndColor(j * ROW + COL - 1, '0')
                        break
        elif direction == 'down':
            for i in range(COL):
                for j in range(ROW - 1, 0, -1):
                    up_label = self.labels[(j - 1) * ROW + i]
                    down_label = self.labels[j * ROW + i]
                    if up_label.text() == down_label.text():
                        num = int(down_label.text())
                        self.finishedMerge(j * ROW + i, num * 2)
                        self.setTextAndColor(j * ROW + i, str(num * 2))
                        for k in range(j - 1, 0, -1):
                            self.setTextAndColor(k * ROW + i, self.labels[(k - 1) * ROW + i].text())
                        self.setTextAndColor(0 * ROW + i, '0')
                        break
        elif direction == 'up':
            for i in range(COL):
                for j in range(ROW - 1):
                    up_label = self.labels[j * ROW + i]
                    down_label = self.labels[(j + 1) * ROW + i]
                    if up_label.text() == down_label.text():
                        num = int(up_label.text())
                        self.finishedMerge(j * ROW + i, num * 2)
                        self.setTextAndColor(j * ROW + i, str(num * 2))
                        for k in range(j + 1, ROW - 1):
                            self.labels[k * ROW + i].setText(self.labels[(k + 1) * ROW + i].text())
                            self.setTextAndColor(k * ROW + i, self.labels[(k + 1) * ROW + i].text())
                        self.setTextAndColor((COL - 1) * ROW + i, '0')
                        break

    def randomSetLabels(self, nums):
        empty_grids = self.getEmptyGrid()
        num_str = '222448'
        for _ in range(nums):
            num = random.choice(num_str)
            label_index = random.choice(empty_grids)
            self.setTextAndColor(label_index, num, setIsMove=False)

    def getEmptyGrid(self):
        results = [index for index, labels in enumerate(self.labels) if labels.text() == '0']
        return results

    def setTextAndColor(self, index, num, setIsMove=True):
        if setIsMove:
            pre_text = self.labels[index].text()
            if pre_text != num:
                self.isMove = True

        self.labels[index].setText(num)
        self.palettes[index].setColor(QPalette.WindowText, NUM_MAP_COLOR[num]['font'])
        self.palettes[index].setColor(QPalette.Window, NUM_MAP_COLOR[num]['background'])
        self.labels[index].setPalette(self.palettes[index])

    def finishedMerge(self, index, num):
        if num == 2048:
            self.succeed = True
        self.isLose = False

    def gameOver(self):
        button = QMessageBox.question(self, "Игра окончена",
                                      "Ходов больше нет! Хотите начать заново?",
                                      QMessageBox.Ok |
                                      QMessageBox.Ok)
        if button == QMessageBox.Ok:
            self.reset()

    def gameSuccess(self):
        button = QMessageBox.question(self, "Поздравляем",
                                      "Вы собрали 2048! Хотите начать заново?",
                                      QMessageBox.Ok |
                                      QMessageBox.Ok)
        if button == QMessageBox.Ok:
            self.reset()
