import datetime
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


from bin.HistoryWindowClass import *


from PyQt5 import QtGui, QtCore
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QLabel, QScrollArea, QCheckBox, \
    QGridLayout, QHBoxLayout, QVBoxLayout, QMenuBar, QAction, QLineEdit


class SortMain(QWidget):
    def __init__(self):
        super().__init__()
        self.Error = None
        self.DataBase = None
        self.curs = None
        self.WindFormat = None
        self.LikeDataBase = None
        try:
            with open('bin/DefaultPath.txt', mode='rt') as f:
                k = f.readlines()
                if len(k) == 1:
                    self.ToPath = k[0]
                else:
                    self.ToPath = "No directory"
        except FileNotFoundError:
            with open('bin/DefaultPath.txt', mode='at') as f:
                k = f.readlines()
                if len(k) != 0:
                    self.ToPath = k[0]
                else:
                    self.ToPath = "No directory"
        if self.ToPath == "No directory":
            with open('bin/DefaultPath.txt', mode='wt') as f:
                f.write('No directory')
        self.DB = None
        uic.loadUi('bin/Windows/SortWindow.ui', self)
        self.ToFile = None
        self.isAll = True
        self.initUi()

    def initUi(self):
        self.openHistory.clicked.connect(self.openHistoryfnc)
        self.SelectPath.clicked.connect(self.SelectP)
        self.SelectFileButton.clicked.connect(self.SelectFile)
        self.StartButton.clicked.connect(self.Sort)
        self.AllOrSelectButton.clicked.connect(self.AllOrSelect)
        self.SelectFormatButton.clicked.connect(self.CallFormat)
        self.SelectFileLineEdit_2.setText(self.ToPath)

    def openHistoryfnc(self):
        self.HistoryClass = HistoryWind()
        self.HistoryClass.show()

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

    def addFilesToDB(self, name, fromLoc, toLoc):
        self.OpenDataBase()
        date = str(datetime.datetime.now()).split('.')[0].split(':')[0]
        BaseInfo = f'INSERT INTO Files(FileName, NowLocation, FromLocation, SortedDate) VALUES ("{name}", '
        BaseInfo += f'"{toLoc}", "{fromLoc}", "{date}")'
        self.curs.execute(BaseInfo).fetchall()
        self.CloseDataBase()

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
        print(self.isAll)
        if self.isAll:
            self.AllOrSelectButton.setText('̲В̲с̲е̲ ̲"̲.̲"/ Выбрать форматы')
            self.SelectFormatButton.setEnabled(False)
        else:
            self.AllOrSelectButton.setText('Все "." / ̲В̲ы̲б̲р̲а̲т̲ь̲ ф̲о̲р̲м̲а̲т̲ы̲')
            self.SelectFormatButton.setEnabled(True)

    def CopyTo(self, data, file):
        if ' '.join(data) not in os.listdir(self.ToPath):
            os.mkdir(self.ToPath + '/' + ' '.join(data))
        shutil.copy(file, self.ToPath + '/' + ' '.join(data) + '/' + file.split('/')[-1])
        self.addFilesToDB(file.split('/')[-1], file, self.ToPath + '/' + ' '.join(data) + '/' + file.split('/')[-1])

    def MoveTo(self, data, file):
        if ' '.join(data) not in os.listdir(self.ToPath):
            os.mkdir(self.ToPath + '/' + ' '.join(data))
        shutil.move(file, self.ToPath + '/' + ' '.join(data) + '/' + file.split('/')[-1])
        self.addFilesToDB(file.split('/')[-1], file, self.ToPath + '/' + ' '.join(data) + '/' + file.split('/')[-1])

    def Sort(self):
        self.DB = 'bin/DataBase/BD.sqlite'
        os.walk(self.ToPath)
        if self.SelectFileLineEdit_2.text() == '':
            try:
                with open('bin/DefaultPath.txt', mode='rt') as f:
                    self.ToPath = f.readlines()[0]
            except IndexError:
                self.ResultLineEdit.setText('Некорректно введеный путь. Проверьте нижнее поле для ввода')
            except FileNotFoundError:
                with open('bin/DefaultPath.txt', mode='a') as f:
                    self.ResultLineEdit.setText('Пересоздан корневой файл. Запустите сортировку еще раз')
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
                                Day = time.ctime(os.path.getctime(file)).split()[:2]
                                Day = reversed(Day)
                                if self.TypeSort.currentText() == 'Год/Месяц/День/Час':
                                    data = [time.ctime(os.path.getctime(file)).split()[-1], '- год,',
                                            ' '.join(
                                                Day) + f'(день: {time.ctime(os.path.getctime(file)).split()[2]}) час:',
                                            time.ctime(os.path.getctime(file)).split()[3].split(':')[0]]
                                elif self.TypeSort.currentText() == 'Год/Месяц/День':
                                    data = [time.ctime(os.path.getctime(file)).split()[-1], '- год,',
                                            ' '.join(Day) + f'(день: {time.ctime(os.path.getctime(file)).split()[2]})']
                                elif self.TypeSort.currentText() == 'Год/Месяц':
                                    data = [time.ctime(os.path.getctime(file)).split()[-1], '- год,', Day[1]]
                                else:
                                    data = [time.ctime(os.path.getctime(file)).split()[-1]]
                                if self.isAll:
                                    self.CopyTo(data, file)
                                else:
                                    self.OpenDataBase()
                                    self.LikeDataBase = 'SELECT Format FROM FormatFile WHERE Chek = 1'
                                    LikeFormat2 = []
                                    for i in self.curs.execute(self.LikeDataBase).fetchall():
                                        LikeFormat2.append(i[0])
                                    if file.split('.')[1] in LikeFormat2:
                                        if ' '.join(data) not in os.listdir(self.ToPath):
                                            os.mkdir(self.ToPath + '/' + ' '.join(data))
                                        shutil.copy(file, self.ToPath + '/' + ' '.join(data) + '/' + file.split('/')[-1])
                                        self.addFilesToDB(file.split('/')[-1], file,
                                                          self.ToPath + '/' + ' '.join(data) + '/' + file.split('/')[-1])
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
                                Day = time.ctime(os.path.getctime(file)).split()[:2]
                                Day = reversed(Day)
                                if self.TypeSort.currentText() == 'Год/Месяц/День/Час':
                                    data = [time.ctime(os.path.getctime(file)).split()[-1], '- год,',
                                            ' '.join(
                                                Day) + f'(день: {time.ctime(os.path.getctime(file)).split()[2]}) час:',
                                            time.ctime(os.path.getctime(file)).split()[3].split(':')[0]]
                                elif self.TypeSort.currentText() == 'Год/Месяц/День':
                                    data = [time.ctime(os.path.getctime(file)).split()[-1], '- год,',
                                            ' '.join(Day) + f'(день: {time.ctime(os.path.getctime(file)).split()[2]})']
                                elif self.TypeSort.currentText() == 'Год/Месяц':
                                    data = [time.ctime(os.path.getctime(file)).split()[-1], '- год,', Day[1]]
                                else:
                                    data = [time.ctime(os.path.getctime(file)).split()[-1]]

                                if self.isAll:
                                    self.MoveTo(data, file)
                                else:
                                    self.OpenDataBase()
                                    self.LikeDataBase = 'SELECT Format FROM FormatFile WHERE Chek = 1'
                                    LikeFormat2 = []
                                    for i in self.curs.execute(self.LikeDataBase).fetchall():
                                        LikeFormat2.append(i[0])
                                    if file.split('.')[1] in LikeFormat2:
                                        if ' '.join(data) not in os.listdir(self.ToPath):
                                            os.mkdir(self.ToPath + '/' + ' '.join(data))
                                        shutil.move(file, self.ToPath + '/' + file.split('/')[-1])
                                        self.addFilesToDB(file.split('/')[-1], file,
                                                          self.ToPath + '/' + file.split('/')[-1])
                else:
                    self.Error = ErrorWindow(101)
                    self.Error.show()
            else:
                self.Error = ErrorWindow(102)
                self.Error.show()
        except FileNotFoundError:
            self.ResultLineEdit.setText('Неизвестная ошибка! Проверьте путь указанный в нижнем поле!')