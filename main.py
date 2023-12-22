# -*- coding: utf-8 -*-
import sys

from PySide6.QtWidgets import QApplication
from src import Game

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    sys.exit(app.exec())
