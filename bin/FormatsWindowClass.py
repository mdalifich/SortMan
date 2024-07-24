import sys
import os
import glob
import os.path
import sqlite3
import shutil
import time

import bin.AORFormatsWindowClass
from bin.AORFormatsWindowClass import *


from PyQt5 import QtGui, QtCore
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QLabel, QScrollArea, QCheckBox, \
    QGridLayout, QHBoxLayout, QVBoxLayout, QMenuBar, QAction, QLineEdit


class SelectFormatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.CheckBoxes = []
        self.dialogue = dialugueWindow('Удалить')
        self.setGeometry(100, 100, 403, 208)
        self.setWindowTitle('Select Format')
        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        layoutH = QHBoxLayout()
        layoutV = QVBoxLayout()
        scroll = QScrollArea()
        self.widget = QWidget()
        layoutH.addWidget(scroll)
        self.widget.setLayout(self.grid)
        scroll.setWidget(self.widget)
        scroll.setWidgetResizable(True)
        layoutV.addLayout(layoutH)
        self.setLayout(layoutV)
        self.UpdateFormatBox()
        self.Menu = QMenuBar(self)
        self.FormatMenu = self.Menu.addMenu('Изменить')
        self.addForm = QAction('Добавить', self)
        self.delForm = QAction('Удалить', self)
        self.addForm.triggered.connect(self.addFormat)
        self.delForm.triggered.connect(self.deleteFormat)
        self.FormatMenu.addAction(self.addForm)
        self.FormatMenu.addAction(self.delForm)

    def deleteFormat(self):
        self.dialogue = dialugueWindow('Удалить')
        self.dialogue.show()
        self.close()

    def addFormat(self):
        self.dialogue = dialugueWindow('Добавить')
        self.dialogue.show()
        self.close()

    def OpenDataBase(self):
        self.DataBase = sqlite3.connect('bin/DataBase/BD.sqlite')
        self.curs = self.DataBase.cursor()

    def CloseDataBase(self):
        self.DataBase.commit()
        self.DataBase.close()

    def CheckFormatFromDataBase(self):
        self.OpenDataBase()
        self.LikeDataBase = 'SELECT Format FROM FormatFile'
        ret = self.curs.execute(self.LikeDataBase).fetchall()
        self.CloseDataBase()
        return ret

    def UpdateFormatBox(self):
        if len(self.CheckFormatFromDataBase()) > 0:
            x = 0
            y = 0
            for i in reversed(range(self.grid.count())):
                self.grid.itemAt(i).widget().setParent(None)
            for i in self.CheckFormatFromDataBase():
                mesh = QCheckBox(self)
                mesh.setText(i[0])
                self.OpenDataBase()
                self.LikeDataBase = f'SELECT Chek FROM FormatFile WHERE Format = "{i[0]}"'
                ret = self.curs.execute(self.LikeDataBase).fetchall()
                if ret[0][0] == 1:
                    mesh.setChecked(True)
                else:
                    mesh.setChecked(False)
                self.CloseDataBase()
                mesh.clicked.connect(self.checkedFormat)
                self.grid.addWidget(mesh, y, x)
                self.CheckBoxes.append(mesh)
                x += 1
                if x == 5:
                    y += 1
                    x = 0

    def checkedFormat(self):
        if self.sender().isChecked():
            self.OpenDataBase()
            chekBaseInfo = f'UPDATE FormatFile SET Chek = 1 WHERE Format = "{self.sender().text()}"'
            self.curs.execute(chekBaseInfo).fetchall()
            self.CloseDataBase()
        elif not self.sender().isChecked():
            self.OpenDataBase()
            chekBaseInfo = f'UPDATE FormatFile SET Chek = 0 WHERE Format = "{self.sender().text()}"'
            self.curs.execute(chekBaseInfo).fetchall()
            self.CloseDataBase()