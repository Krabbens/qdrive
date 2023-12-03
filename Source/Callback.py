from PyQt5.QtCore import QCoreApplication, QUrl, pyqtSignal, QObject
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtQml import qmlRegisterType, QQmlComponent
from Source.Debug import Debug
from Source.ThreadWrapper import ThreadWrapper as TW
from Source.Drive.MonkeyPatch import *
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

    @pyqtSlot(int)
    def download_file_async(self, index):
        # here add item delegate loader
        Debug()("Index: ", index)
        file = self.mf.file_list.get(index)
        Debug()("File: ", file) 
        self.download_file(file, index)

    def download_file_worker(self, file, index):
        earlier_progress = 0
        def callback(progress, total):
            # TODO write signal to update progress bar
            print("Progress: " + str(round((earlier_progress + progress)/total, 2)*100) + "%")
            self.conn.set_gradient_in_delegate(index, round((earlier_progress + progress)/total, 2))
        if "parts" in file:
            Debug()("Parted file:", file)
            name = file["name"]
            if os.path.exists("./Downloads/" + name):
                i = 1
                while os.path.exists("./Downloads/" + name):
                    name = file["name"].split(".")[0] + " (" + str(i) + ")." + file["name"].split(".")[1]
                    i += 1
            parts = sorted(file["parts"], key=lambda x: int(x[0]))
            for part in parts:
                Debug()("Part:", part)
                size = self.program.driveHandler.download_file(name, part[1], int_size_from_str(file["size"]), callback)
                earlier_progress += size
        else:
            name = file["name"]
            if os.path.exists("./Downloads/" + name):
                i = 1
                while os.path.exists("./Downloads/" + name):
                    name = file["name"].split(".")[0] + " (" + str(i) + ")." + file["name"].split(".")[1]
                    i += 1

            self.program.driveHandler.download_file(name, file["id"], int_size_from_str(file["size"]), callback)
        return name
    
    def download_file_callback(self, path):
        # here remove item delegate loader
        print("Downloaded: " + path)

    
    @TW.future(target=open_directory_worker, callback=open_directory_callback)
    def open_directory(self, name): pass

    @TW.future(target=download_file_worker, callback=download_file_callback)
    def download_file(self, file, index): pass