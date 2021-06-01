import time
import pyttsx3
from PyQt5.QtCore import QThread
from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread,
                          QThreadPool, pyqtSignal)
class Voice(QThread):
    def __init__(self,slovo):
        super().__init__()
        self.slovo=slovo
    def run(self):
        voice=pyttsx3.init()
        voice.say(self.slovo)
        voice.runAndWait

