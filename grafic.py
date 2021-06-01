import sys
import parse
from parseSlovar import *
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt,QObject,pyqtSignal,QThread,pyqtSlot,QRunnable,QThreadPool
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget,QAction
from PyQt5.QtGui import QTextCursor
import pyttsx3
class Voice(QThread):
    def __init__(self,slovo):
        super().__init__()
        self.slovo=slovo
    def run(self):
        self.voice = pyttsx3.init()
        self.voice.say(self.slovo)
        self.voice.runAndWait()
class Main_Window(QDialog): # Главное окно
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Словарь")
        self.setGeometry(500, 250, 1150, 700)
        vbox=QVBoxLayout()
        self.tabWidget=QTabWidget()
        self.leks=Leks_slovar()
        self.slov=Slovar()
        self.table=Table()
        self.tabWidget.addTab(self.leks,"Лексический словарь")
        self.tabWidget.addTab(self.slov,"Словарь")
        self.tabWidget.addTab(self.table,'Мой словарь')
        vbox.addWidget(self.tabWidget)
        self.slov.textEdit.LeksSlovar.triggered.connect(self.smena0)# Кнопки для смены виджетов из словаря->лексическийс словарь
        self.leks.textBrowser.SlovSlov.triggered.connect(self.smena1)
        self.setLayout(vbox)
        self.show()
    def smena0(self):
        self.leks.textBrowser.slovo=self.slov.textEdit.slovo    # забор слова из обычного словаря в лексический
        self.tabWidget.setCurrentIndex(0)
        self.leks.NovoeSlovo()
    def smena1(self):
        self.slov.textEdit.slovo=self.leks.textBrowser.slovo
        self.tabWidget.setCurrentIndex(1)
        self.slov.NovoeSlovo()
    def smena2(self):
        self.tabWidget.setCurrentIndex(2)
        self.table.NovoeSlovo()
class TextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.slovo=str
        self.voice=pyttsx3.init()
        self.LeksSlovar=QAction()
        self.SlovSlov=QAction()
        self.searchSlovar = QAction("Найти в словаре", self)
        self.searchSlovar.triggered.connect(self.eventSlovar)
        self.searchSlovar.setShortcut('S')
        self.addAction(self.searchSlovar)
        self.searchLeks = QAction("Найти в лексическом словаре", self)
        self.searchLeks.triggered.connect(self.eventLeksSlovar)
        self.searchLeks.setShortcut('F')
        self.addAction(self.searchLeks)
    def contextMenuEvent(self,event):
        menu = self.createStandardContextMenu()
        menu.addAction(self.searchLeks)
        menu.addAction(self.searchSlovar)
        self.searchLeks.setEnabled(False)
        self.searchSlovar.setEnabled(False)
        if (self.slovoPodCursorom()):
            self.searchSlovar.setEnabled(True)
            self.searchLeks.setEnabled(True)
        menu.exec_(self.mapToGlobal(event.pos()))
    def slovoPodCursorom(self):
        cursor = self.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        return cursor.selectedText()
    def eventLeksSlovar(self):
        if(self.slovoPodCursorom()):
            self.slovo=self.slovoPodCursorom()
            self.LeksSlovar.trigger()
    def eventSlovar(self):
        if(self.slovoPodCursorom()):
            self.slovo = self.slovoPodCursorom()
            self.SlovSlov.trigger()
class Leks_slovar(QWidget): # вкладка лексического словаря
    def __init__(self):
        super().__init__()
        self.masSlov=[]
        self.t=True
        self.pos=0
        self.poisk=QLineEdit(self) # Ввод слова
        self.poisk.setPlaceholderText("Ввод слова")
        button_leks=QPushButton("Поиск") # Кнопка поиска
        button_leks.setShortcut('Alt+Enter')
        self.button_next=QPushButton("Next")
        self.button_prev=QPushButton("Prev")
        vbox=QVBoxLayout()
        hbox=QHBoxLayout()
        self.textBrowser = TextEdit()
        self.textBrowser.setReadOnly(True)
        # Добавление всех кнопок
        hbox.addWidget(self.button_prev)
        hbox.addWidget(self.button_next)
        hbox.addWidget(self.poisk)
        hbox.addWidget(button_leks)
        vbox.addLayout(hbox)
        vbox.addWidget(self.textBrowser)
        self.setLayout(vbox)
        #####
        # Логика кнопок
        self.textBrowser.LeksSlovar.triggered.connect(self.NovoeSlovo)
        self.button_next.pressed.connect(self.NextSlovo)
        self.button_next.setEnabled(False)
        self.button_prev.pressed.connect(self.PrevSlovo)
        self.button_prev.setEnabled(False)
        button_leks.setShortcut('Ctrl+S')
        button_leks.pressed.connect(self.Obrabotka)
        button_leks.setStyleSheet('background-color: red;border-style: outset;border-width: 2px;border-radius: 10px;border-color: beige;font: bold 14px;min-width: 10em;padding: 6px;')
        #######
        self.show()
    def NovoeSlovo(self):
        self.poisk.setText(self.textBrowser.slovo)
        self.Obrabotka()
    def Proverka(self):
        print("dasdas")
    def PrevSlovo(self):
        self.t=False
        self.pos -=1
        self.poisk.setText(self.masSlov[self.pos-1])
        self.Obrabotka()
    def NextSlovo(self):
        self.t=False
        self.pos+=1
        self.poisk.setText(self.masSlov[self.pos-1])
        self.Obrabotka()
    def Obrabotka(self):
        self.textBrowser.clear()
        slovo=self.poisk.text()
        thread = Voice(slovo)
        thread.start()
        if(self.t==True):
            self.masSlov=self.masSlov[0:self.pos]
            self.masSlov.append(slovo)
            self.pos+=1
        if(self.pos>1):
            self.button_prev.setEnabled(True)
        else:
            self.button_prev.setEnabled(False)
        if(self.pos!=len(self.masSlov)):
            self.button_next.setEnabled(True)
        else: self.button_next.setEnabled(False)
        self.t=True
        results=parse.parse(slovo)
        if(results=='Error'):
            self.masSlov.pop()
            self.textBrowser.append("Введенно неверное слово")
        else:
            kluchi=(list(results.keys()))
            for i in kluchi:
                chet = 1
                self.textBrowser.append(i)
                opredelenie=results[i]
                for j in opredelenie:
                    self.textBrowser.append('    '*5+str(chet)+')'+j)
                    chet+=1
class Slovar(QWidget):
    def __init__(self):
        super().__init__()
        self.poiskSlova=QLineEdit()
        self.textEdit=TextEdit()
        self.textEdit.setReadOnly(True)
        self.textEdit.SlovSlov.triggered.connect(self.NovoeSlovo)
        button=QPushButton("Поиск")
        hbox=QHBoxLayout()
        vbox=QVBoxLayout()
        hbox.addWidget(self.poiskSlova)
        hbox.addWidget(button)
        vbox.addLayout(hbox)
        vbox.addWidget(self.textEdit)
        button.pressed.connect(self.vivodSlovar)
        self.setLayout(vbox)
        self.show()
    def NovoeSlovo(self):
        self.poiskSlova.setText(self.textEdit.slovo)
        self.vivodSlovar()
    def vivodSlovar(self):
        self.textEdit.clear()
        slovo=parseSlovar(self.poiskSlova.text())
        voice=pyttsx3.init()
        voice.say(self.poiskSlova.text())
        voice.runAndWait()
        if('dopolnenie' in slovo):
            temp=slovo['dopolnenie']
            for i in temp:
                self.textEdit.append(i)
        self.textEdit.append('Перевод: ' + slovo['perevod'])
        self.textEdit.append("Example: ")
        if(slovo['kolvo']>5):
            slovo['kolvo']=5
        for i in range(0,slovo['kolvo']):
            self.textEdit.append(slovo['example_en'][i])
            self.textEdit.append(slovo['example_ru'][i])
class Table(QWidget):
    def __init__(self):
        super().__init__()
        self.poiskSlova = QLineEdit()
        self.table=QTableWidget()
        self.slova=[]
        self.kolvo=0
        button = QPushButton("Поиск")
        button1=QPushButton('Pricol')
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        hbox.addWidget(self.poiskSlova)
        hbox.addWidget(button)
        hbox.addWidget(button1)
        vbox.addLayout(hbox)
        vbox.addWidget(self.table)
        self.setLayout(vbox)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Word","Transcription","Translation","Example"])
        self.ZagruzkaSlov()
        button.pressed.connect(self.NovoeSlovo)
        button1.pressed.connect(self.DeleteSlovo)
        #header = self.table.horizontalHeader()
        #header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        #header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        #header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        #header.setSectionResizeMode(3, QHeaderView.Stretch)
        self.show()
    def DeleteSlovo(self):
        t=self.table.selectedRanges()
        t=t[0].bottomRow()
        self.kolvo-=1
        self.slova.pop(t)
        self.table.removeRow(t)
        file=open("from.txt",'w')
        for i in self.slova:
            file.write(i+"\n")
        file.close
    def vvodNovogoSlova(self,slovo):
        self.table.setRowCount(self.kolvo+1)
        results = parseSlovar(slovo)
        self.table.setItem(self.kolvo, 0, QTableWidgetItem(slovo))
        self.table.setItem(self.kolvo, 1, QTableWidgetItem(results['transcription']))
        self.table.setItem(self.kolvo, 2, QTableWidgetItem(results['perevod']))
        if (results["example_en"]):
            self.table.setItem(self.kolvo, 3, QTableWidgetItem(results["example_en"][0] + '\n' + results["example_ru"][0]))
        self.kolvo += 1
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
    def NovoeSlovo(self):
        if(parseSlovar(self.poiskSlova.text())):
            with open('from.txt','a') as newWorld:
                newWorld.write('\n'+self.poiskSlova.text())
                self.vvodNovogoSlova(self.poiskSlova.text())
                self.slova.append(self.poiskSlova.text())
        else: self.poiskSlova.setText("Неверно введено слово")
    def ZagruzkaSlov(self):
        with open('from.txt','r') as slovaIzFile:
            for i in slovaIzFile:
                i=i.replace('\n','')
                self.vvodNovogoSlova(i)
                self.slova.append(i)
        print(self.slova)
app=QApplication(sys.argv)
window=Main_Window()
sys.exit(app.exec_())