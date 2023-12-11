import math
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


    @pyqtSlot(int)
    def open_directory_async(self, idx):
        self.conn.toggle_loader()
        Debug()("Opening directory index:", idx)
        name = self.mf.file_list.get(idx)["name"]
        Debug()("Opening directory:", name)
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
            self.conn.set_progress(index, round((earlier_progress + progress)/total, 2))
        if "parts" in file:
            name = file["name"]
            if os.path.exists("./Downloads/" + name):
                i = 1
                while os.path.exists("./Downloads/" + name):
                    name = ".".join(file["name"].split(".")[:-1]) + " (" + str(i) + ")." + file["name"].split(".")[-1]
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
                    name = ".".join(file["name"].split(".")[:-1]) + " (" + str(i) + ")." + file["name"].split(".")[-1]
                    i += 1

            self.program.driveHandler.download_file(name, file["id"], int_size_from_str(file["size"]), callback)
        return {"path" : name, "index" : index}
    
    def download_file_callback(self, return_val):
        self.conn.set_progress(return_val["index"], 1)
        Debug()("Downloaded file:", return_val["path"])


    @pyqtSlot(str)
    def upload_files_async(self, paths):
        for path in json.loads(paths):
            part_file = {
                "name": path.split("/")[-1],
                "type": "file",
                "icon": "\uf15b",
                "date": datetime.now().strftime("%a %b %y %H:%M"),
                "size": sizeof_fmt(os.path.getsize(path[8:])),
                "id": "",
                "parentId": self.program.driveHandler.get_id_of_current_directory(),
                "progress": 0,
                "parts": "[]",
                "clickable": False,
                "progressColor": "#445555FF"
            }
            self.mf.file_list.add_items([part_file])
            self.upload_files(path[8:], self.mf.file_list.rowCount()-1)

    def upload_files_worker(self, path, idx):
        num_of_accounts = len(self.program.driveHandler.accounts)
        actual_progress = 0
        def callback(progress, total):
            nonlocal actual_progress
            actual_progress += progress / num_of_accounts
            print(actual_progress/total)
            self.conn.set_progress(idx, round(actual_progress/total, 2))

        with open(path, "rb") as f:
            file_length = os.path.getsize(path)
            split_size = math.ceil(file_length / num_of_accounts)
            if split_size == 0: split_size = file_length
            i = 0
            while True:
                file_name = path.split("/")[-1] + ".gpart" + str(i+1)
                data = f.read(split_size)
                if not data: break
                self.program.driveHandler.upload_file_async(i, file_name, data, callback)
                i += 1

        Debug()("Uploading file:", path)
        
        #self.program.driveHandler.upload_file(path)
        

    
    @TW.future(target=open_directory_worker, callback=open_directory_callback)
    def open_directory(self, name): pass

    @TW.future(target=download_file_worker, callback=download_file_callback)
    def download_file(self, file, index): pass

    @TW.future(target=upload_files_worker)
    def upload_files(self, path): pass