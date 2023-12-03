import os
from PyQt5.QtCore import QMetaObject, QUrl, pyqtSignal, pyqtSlot, QObject, Qt, QThread
from PyQt5.QtQml import QQmlApplicationEngine, QQmlComponent
from Source.Callback import Callback
from Source.Connector import Connector
from Source.Drive.DriveHandler import DriveHandler
from Source.ModelFactory import ModelFactory
from Source.Thread.ThreadWrapper import ThreadWrapper as TW
from Source.Debug import Debug

class Program(TW):
    def __init__(self, app):
        super().__init__()
        self.engine = None
        self.app = app
        Debug.main_thread_id = int(QThread.currentThreadId())
        self.fullPath = os.path.dirname(os.path.realpath(__file__))
        self.connector = Connector(self)
        self.modelFactory = ModelFactory()
        self.callback = Callback(self)
        self.driveHandler = DriveHandler()
        self.initialize()
        if self.engine != None: self.run()
        

    def initialize(self):
        Debug()(QThread.currentThread(), int(QThread.currentThreadId()))
        self.engine = QQmlApplicationEngine()
        ctx = self.engine.rootContext()
        ctx.setContextProperty('callback', self.callback)
        ctx.setContextProperty('connector', self.connector)
        ctx.setContextProperty('fileList', self.modelFactory.file_list)
        self.engine.load("main.qml")
        self.connector.init()

    def create_drive(self):
        self.driveHandler.create_instances()
        files = self.driveHandler.list_files()
        
        return files
        
    def fill_drive(self, files):
        self.connector.toggle_loader()
        self.modelFactory.file_list.add_items(files) 

    def run(self):
        self.connector.toggle_loader()
        self.create_drive_async()
        


    @TW.future(target=create_drive, callback=fill_drive)
    def create_drive_async(self): pass