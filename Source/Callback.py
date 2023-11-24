from PyQt5.QtCore import QCoreApplication, QUrl, pyqtSignal, QObject
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtQml import qmlRegisterType, QQmlComponent
from Source.Thread import Thread
from concurrent.futures import ThreadPoolExecutor as cf
import os

class Callback(QObject):
    def __init__(self, program):
        QObject.__init__(self)
        self.program = program
        self.engine = None
        self.threads = []
        self.threadId = 0

    def ManageThread(self, id):
        for pair in self.threads:
            if pair[0] == id:
                pair[1].terminate()
                self.threads.remove(pair)
                break

    @pyqtSlot()
    def Exit(self):
        os._exit(0)