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


class SortMain(QWidget):
    def __init__(self):
        super().__init__()
        with open('bin/DefaultPath.txt', mode='rt') as f:
            self.ToPath = f.readlines()[0]
        self.DB = None
        uic.loadUi('bin/Windows/SortWindow.ui', self)
        self.ToFile = None
        self.isAll = True
        self.initUi()

    def initUi(self):
        self.SelectPath.clicked.connect(self.SelectP)
        self.SelectFileButton.clicked.connect(self.SelectFile)
        self.StartButton.clicked.connect(self.Sort)
        self.AllOrSelectButton.clicked.connect(self.AllOrSelect)
        self.SelectFormatButton.clicked.connect(self.CallFormat)
        self.SelectFileLineEdit_2.setText(self.ToPath)

    def SelectP(self):
        self.ToFile = QFileDialog.getExistingDirectory(self, 'Выбери папку', '')
        self.ToPath = self.ToFile
        with open('bin/DefaultPath.txt', mode='wt') as f:
            f.write(self.ToPath)
        self.SelectFileLineEdit_2.setText(self.ToPath)

    def CallFormat(self):
        self.WindFormat = SelectFormatWindow()
        self.WindFormat.show()

    def OpenDataBase(self):
        self.DataBase = sqlite3.connect('bin/DataBase/BD.sqlite')
        self.curs = self.DataBase.cursor()

    def CloseDataBase(self):
        self.DataBase.commit()
        self.DataBase.close()

    def LenghFormat(self):
        self.OpenDataBase()
        self.LikeDataBase = 'SELECT Format FROM FormatFile'
        ret = len(self.curs.execute(self.LikeDataBase).fetchall())
        self.CloseDataBase()
        return ret

    def SelectFile(self):
        self.ToFile = QFileDialog.getExistingDirectory(self, 'Выбери папку', '')
        self.SelectFileLineEdit.setText(self.ToFile)

    def AllOrSelect(self):
        self.isAll = not self.isAll
        if self.isAll:
            self.AllOrSelectButton.setText('̲В̲с̲е̲ ̲"̲.̲"/ Выбрать форматы')
            self.SelectFormatButton.setEnabled(False)
        else:
            self.AllOrSelectButton.setText('Все "." / ̲В̲ы̲б̲р̲а̲т̲ь̲ ф̲о̲р̲м̲а̲т̲ы̲')
            self.SelectFormatButton.setEnabled(True)

    def Sort(self):#/home/artur82/PycharmProjects/SortMan/Test/
        self.DB = 'bin/DataBase/BD.sqlite'
        os.walk(self.ToPath)
        if self.SelectFileLineEdit_2.text() == '':
            with open('bin/DefaultPath.txt', mode='rt') as f:
                self.ToPath = f.readlines()[0]
        else:
            self.ToPath = self.SelectFileLineEdit_2.text()
        try:
            if os.path.isfile(self.DB):
                if self.SelectFileLineEdit.text() != '':
                    if self.CopyFileBox.isChecked():
                        self.ResultLineEdit.setText('Успешно!')
                        files1 = os.listdir(self.ToFile)
                        for i in range(len(files1)):
                            files1[i] = self.ToFile + '/' + files1[i]
                        for file in files1:
                            if len(file.split('.')) == 1:
                                for i in os.listdir(file):
                                    files1.append(file + '/' + i)
                            else:
                                if self.isAll:
                                    if self.TypeSort.currentText() == 'Год/Месяц/День/Час':
                                        Day = time.ctime(os.path.getctime(file)).split()[:2]
                                        Day = reversed(Day)
                                        data = [time.ctime(os.path.getctime(file)).split()[-1],
                                                ' '.join(Day) + f'(числа: {time.ctime(os.path.getctime(file)).split()[2]})',
                                                time.ctime(os.path.getctime(file)).split()[3].split(':')[0]]
                                        if ' '.join(data) not in os.listdir(self.ToPath):
                                            os.mkdir(self.ToPath + '/' + ' '.join(data))
                                        shutil.copy(file, self.ToPath + '/' + ' '.join(data) + '/' + file.split('/')[-1])
                                    elif self.TypeSort.currentText() == 'Год/Месяц/День':
                                        Day = time.ctime(os.path.getctime(file)).split()[:2]
                                        Day = reversed(Day)
                                        data = [time.ctime(os.path.getctime(file)).split()[-1],
                                                ' '.join(Day) + f'(числа: {time.ctime(os.path.getctime(file)).split()[2]})']
                                        if ' '.join(data) not in os.listdir(self.ToPath):
                                            os.mkdir(self.ToPath + '/' + ' '.join(data))
                                        shutil.copy(file, self.ToPath + '/' + ' '.join(data) + '/' + file.split('/')[-1])
                                    elif self.TypeSort.currentText() == 'Год/Месяц':
                                        Day = time.ctime(os.path.getctime(file)).split()[:2]
                                        data = [time.ctime(os.path.getctime(file)).split()[-1], Day[1]]
                                        if ' '.join(data) not in os.listdir(self.ToPath):
                                            os.mkdir(self.ToPath + '/' + ' '.join(data))
                                        shutil.copy(file, self.ToPath + '/' + ' '.join(data) + '/' + file.split('/')[-1])
                                    else:
                                        data = [time.ctime(os.path.getctime(file)).split()[-1]]
                                        if ' '.join(data) not in os.listdir(self.ToPath):
                                            os.mkdir(self.ToPath + '/' + ' '.join(data))
                                        shutil.copy(file, self.ToPath + '/' + ' '.join(data) + '/' + file.split('/')[-1])
                                else:
                                    self.OpenDataBase()
                                    self.LikeDataBase = 'SELECT Format FROM FormatFile WHERE Chek = 1'
                                    LikeFormat2 = []
                                    for i in self.curs.execute(self.LikeDataBase).fetchall():
                                        LikeFormat2.append(i[0])
                                    if file.split('.')[1] in LikeFormat2:
                                        shutil.copy(file, self.ToPath + '/' + file.split('/')[-1])
                                    self.CloseDataBase()

                    elif self.RemakeFileBox.isChecked():
                        self.ResultLineEdit.setText('Успешно!')
                        files1 = os.listdir(self.ToFile)
                        for i in range(len(files1)):
                            files1[i] = self.ToFile + '/' + files1[i]
                        for file in files1:
                            if len(file.split('.')) == 1:
                                for i in os.listdir(file):
                                    files1.append(file + '/' + i)
                            else:
                                if self.isAll:
                                    if self.TypeSort.currentText() == 'Год/Месяц/День/Час':
                                        Day = time.ctime(os.path.getctime(file)).split()[:2]
                                        Day = reversed(Day)
                                        data = [time.ctime(os.path.getctime(file)).split()[-1],
                                                ' '.join(Day) + f'(числа: {time.ctime(os.path.getctime(file)).split()[2]})',
                                                time.ctime(os.path.getctime(file)).split()[3].split(':')[0]]
                                        if ' '.join(data) not in os.listdir(self.ToPath):
                                            os.mkdir(self.ToPath + '/' + ' '.join(data))
                                        shutil.move(file, self.ToPath + '/' + ' '.join(data) + '/' + file.split('/')[-1])
                                    elif self.TypeSort.currentText() == 'Год/Месяц/День':
                                        Day = time.ctime(os.path.getctime(file)).split()[:2]
                                        Day = reversed(Day)
                                        data = [time.ctime(os.path.getctime(file)).split()[-1],
                                                ' '.join(Day) + f'(числа: {time.ctime(os.path.getctime(file)).split()[2]})']
                                        if ' '.join(data) not in os.listdir(self.ToPath):
                                            os.mkdir(self.ToPath + '/' + ' '.join(data))
                                        shutil.move(file, self.ToPath + '/' + ' '.join(data) + '/' + file.split('/')[-1])
                                    elif self.TypeSort.currentText() == 'Год/Месяц':
                                        Day = time.ctime(os.path.getctime(file)).split()[:2]
                                        data = [time.ctime(os.path.getctime(file)).split()[-1], Day[1]]
                                        if ' '.join(data) not in os.listdir(self.ToPath):
                                            os.mkdir(self.ToPath + '/' + ' '.join(data))
                                        shutil.move(file, self.ToPath + '/' + ' '.join(data) + '/' + file.split('/')[-1])
                                    else:
                                        data = [time.ctime(os.path.getctime(file)).split()[-1]]
                                        if ' '.join(data) not in os.listdir(self.ToPath):
                                            os.mkdir(self.ToPath + '/' + ' '.join(data))
                                        shutil.move(file, self.ToPath + '/' + ' '.join(data) + '/' + file.split('/')[-1])
                                else:
                                    self.OpenDataBase()
                                    self.LikeDataBase = 'SELECT Format FROM FormatFile WHERE Chek = 1'
                                    LikeFormat2 = []
                                    for i in self.curs.execute(self.LikeDataBase).fetchall():
                                        LikeFormat2.append(i[0])
                                    if file.split('.')[1] in LikeFormat2:
                                        shutil.copy(file, self.ToPath + '/' + file.split('/')[-1])
                                    self.CloseDataBase()


                else:
                    self.Error = ErrorWindow(101)
                    self.Error.show()
            else:
                self.Error = ErrorWindow(102)
                self.Error.show()
        except FileNotFoundError:
            self.ResultLineEdit.setText('Неизвестная ошибка! Проверьте путь указанный в нижнем поле!')