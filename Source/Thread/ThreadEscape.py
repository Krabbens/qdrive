from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtCore import QThread
from Source.Debug import Debug
from Source.Thread.SignalWrapper import SignalWrapper as SW

MAX_THREADS = 1000

class ThreadEscape(QObject):
    threadSignals = [SW() for i in range(MAX_THREADS)]

    def __init__(self):
        QObject.__init__(self)
        for i in range(MAX_THREADS):
            self.threadSignals[i].threadSignal.connect(self.dispatch)

    def dispatch(self, func, *args):
        func(self, *(args[0]))

    def escape_thread(func):
        def decorator(self, *args, **kwargs):
            id = int(QThread.currentThreadId()) % MAX_THREADS
            self.threadSignals[id].threadSignal.emit(func, args)
        return decorator