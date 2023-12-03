from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtCore import QThread
from Source.Debug import Debug
        

class ThreadEscape(QObject):
    threadSignal = pyqtSignal(object, object)

    def __init__(self):
        QObject.__init__(self)
        self.threadSignal.connect(self.dispatch)

    def dispatch(self, func, *args):
        func(self, *(args[0]))

    def escape_thread(func):
        def decorator(self, *args, **kwargs):
            self.threadSignal.emit(func, args)
        return decorator