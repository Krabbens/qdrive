from PyQt5.QtCore import QCoreApplication, QUrl, pyqtSignal, QObject
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtQml import qmlRegisterType, QQmlComponent
from Source.ThreadWrapper import ThreadWrapper as TW
from concurrent.futures import ThreadPoolExecutor as cf
import os

class Callback(TW):
    def __init__(self, program):
        super().__init__()
        self.program = program
        self.conn = program.connector
        self.mf = program.modelFactory
        self.engine = None
        self.threadId = 0

    @pyqtSlot()
    def exit(self):
        os._exit(0)

    @pyqtSlot(str)
    def open_directory_async(self, name):
        self.conn.toggle_loader()
        self.open_directory(name)

    def open_directory_worker(self, name):
        files = self.program.driveHandler.open_directory(name)
        return files
    
    def open_directory_callback(self, files):
        self.conn.toggle_loader()
        if "parentName" not in files[0]:
            self.conn.set_current_directory_text("All Files")
        else:
            self.conn.set_current_directory_text(files[0]["parentName"])
        self.mf.file_list.clear_items()
        self.mf.file_list.add_items(files)

    @pyqtSlot(str, str, str)
    def download_file_async(self, path, id, name):
        # here insert item delegate loader
        newPath = path.split('file:///')[1] + name
        self.download_file(newPath, id)

    def download_file_worker(self, path, id):
        def callback(progress, total):
            print("Progress: " + str(progress) + " Total: " + str(total))
        self.program.driveHandler.download_file(path, id, callback)
        return path
    
    def download_file_callback(self, path):
        # here remove item delegate loader
        print("Downloaded: " + path)

    
    @TW.future(target=open_directory_worker, callback=open_directory_callback)
    def open_directory(self, name): pass

    @TW.future(target=download_file_worker, callback=download_file_callback)
    def download_file(self, path, id): pass