import os
from PyQt5.QtCore import QMetaObject, QUrl, pyqtSignal, pyqtSlot, QObject, Qt
from PyQt5.QtQml import QQmlApplicationEngine, QQmlComponent
from Source.Callback import Callback
from Source.Connector import Connector
from Source.Drive.DriveHandler import DriveHandler
from Source.ModelFactory import ModelFactory
from Source.ThreadWrapper import ThreadWrapper as TW

class Program(TW):
    def __init__(self, app):
        super().__init__()
        self.engine = None
        self.app = app
        self.fullPath = os.path.dirname(os.path.realpath(__file__))
        self.callback = Callback(self)
        self.connector = Connector(self)
        self.driveHandler = DriveHandler()
        self.modelFactory = ModelFactory()
        self.initialize()
        if self.engine != None: self.run()
        

    def initialize(self):
        self.engine = QQmlApplicationEngine()
        ctx = self.engine.rootContext()
        ctx.setContextProperty('callback', self.callback)
        ctx.setContextProperty('connector', self.connector)
        ctx.setContextProperty('fileList', self.modelFactory.file_list)
        self.engine.load("main.qml")
        self.connector.Init()

    def create_drive(self):
        self.driveHandler.create_instances()
        files = self.driveHandler.list_files()
        return files
        
    def fill_drive(self, files):
        self.modelFactory.file_list.add_items(files)

    def run(self):
        self.create_drive_async()
        


    @TW.future(target=create_drive, callback=fill_drive)
    def create_drive_async(self): pass