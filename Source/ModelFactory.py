from Source.Thread.ThreadWrapper import ThreadWrapper
from Source.Models.DriveFileList import DriveFileList

class ModelFactory(ThreadWrapper):
    def __init__(self):
        super().__init__()
        self.file_list = DriveFileList()