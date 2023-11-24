from PyQt5.QtCore import *

class ThreadCallback(QThread):
    threadSignal = pyqtSignal(object)
    quitSignal = pyqtSignal(object)

    def __init__(self, args: list, id: int) -> None:
        QThread.__init__(self)
        self.func = args[0]
        self.id = id
        if len(args) > 1:
            self.args = args[1]
        else:
            self.args = []

    def run(self):
        self.Run()

    def Run(self):
        if self.args != []:
            self.func(self.args, self.threadSignal)
        else:
            self.func(self.threadSignal)
        self.quitSignal.emit(self.id)