import sys
import os
import glob
import os.path
import sqlite3
import shutil
import time

import bin.FormatsWindowClass
from bin.FormatsWindowClass import *

import bin.ErrorWindowClass
from bin.ErrorWindowClass import *


from PyQt5 import QtGui, QtCore
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QLabel, QScrollArea, QCheckBox, \
    QGridLayout, QHBoxLayout, QVBoxLayout, QMenuBar, QAction, QLineEdit


class HistoryWind(QWidget):
    def __init__(self):
        super().__init__()
        self.curs = None
        self.DataBase = None
        self.LikeDataBase = None
        uic.loadUi('bin/Windows/HistoryWindow.ui', self)
        self.initUI()

    def initUI(self):
        self.SbrossButton.clicked.connect(self.sbross)
        self.filtrButton.clicked.connect(self.filtr)
        self.historyTexBox.setText(self.getText())

    def filtr(self):
        time = self.TimeEdit.dateTime()
        dat = time.date()
        tm = time.time().hour()
        res = f'{dat.year()}-{dat.month()}-{dat.day()} {tm}'
        print(res)
        self.historyTexBox.setText(self.getText(comand=res))

    def sbross(self):
        self.historyTexBox.setText(self.getText())

    def getText(self, comand=''):
        res = ''
        result = ''
        if comand == '':
            self.OpenDataBase()
            self.LikeDataBase = 'SELECT * FROM Files'
            res = self.curs.execute(self.LikeDataBase).fetchall()
            self.CloseDataBase()
        else:
            self.OpenDataBase()
            self.LikeDataBase = f'SELECT * FROM Files WHERE SortedDate = "{comand}"'
            res = self.curs.execute(self.LikeDataBase).fetchall()
            self.CloseDataBase()
        for i in res:
            result += '\n=================================\n'
            result += f'Название: {i[1]}\n\nВходной путь: {i[3]}\n\nВыходной путь: {i[2]}\n\nДата сортировки: {i[4]} часов'
        return result

    def OpenDataBase(self):
        self.DataBase = sqlite3.connect('bin/DataBase/BD.sqlite')
        self.curs = self.DataBase.cursor()

    def CloseDataBase(self):
        self.DataBase.commit()
        self.DataBase.close()