from PyQt5.QtCore import QCoreApplication, QUrl, pyqtSignal, QObject, QThread
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtQml import qmlRegisterType, QQmlComponent
from Source.Debug import Debug
from Source.Thread.ThreadWrapper import ThreadWrapper as TW
from Source.Drive.MonkeyPatch import *
from concurrent.futures import ThreadPoolExecutor as cf
import os
import json

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
        file = self.mf.file_list.get(index)
        self.download_file(file, index)

    def download_file_worker(self, file, index):
        earlier_progress = 0
        def callback(progress, total):
            self.conn.set_download_progress(index, round((earlier_progress + progress)/total, 2))
        if "parts" in file:
            name = file["name"]
            if os.path.exists("./Downloads/" + name):
                i = 1
                while os.path.exists("./Downloads/" + name):
                    name = file["name"].split(".")[0] + " (" + str(i) + ")." + file["name"].split(".")[1]
                    i += 1
            parts = sorted(file["parts"], key=lambda x: int(x[0]))
            for part in parts:
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
        return {"path" : name, "index" : index}
    
    def download_file_callback(self, return_val):
        self.conn.set_download_progress(return_val["index"], 1)
        Debug()("Downloaded file:", return_val["path"])


    @pyqtSlot(str)
    def upload_files_async(self, paths):
        for path in json.loads(paths):
            self.upload_files(path)

    def upload_files_worker(self, path):
        Debug()("Uploading file:", path)
        
        #self.program.driveHandler.upload_file(path)
        

    
    @TW.future(target=open_directory_worker, callback=open_directory_callback)
    def open_directory(self, name): pass

    @TW.future(target=download_file_worker, callback=download_file_callback)
    def download_file(self, file, index): pass

    @TW.future(target=upload_files_worker)
    def upload_files(self, path): pass