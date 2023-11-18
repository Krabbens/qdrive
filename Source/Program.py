import os
from PyQt6.QtCore import QMetaObject, QUrl, pyqtSignal, pyqtSlot, QObject, Qt
from PyQt6.QtQml import QQmlApplicationEngine, QQmlComponent
from Source.Callback import Callback
from Source.Connector import Connector

class Program(QObject):
    def __init__(self, app):
        QObject.__init__(self)
        self.engine = None
        self.app = app
        self.fullPath = os.path.dirname(os.path.realpath(__file__))
        self.callback = Callback(self)
        self.connector = Connector(self)
        self.Initialize()
        if self.engine != None: self.Run()
        

    def Initialize(self):
        self.engine = QQmlApplicationEngine()
        ctx = self.engine.rootContext()
        ctx.setContextProperty('callback', self.callback)
        ctx.setContextProperty('connector', self.connector)
        self.engine.load("main.qml")
        self.connector.Init()

    def Run(self):
        pass