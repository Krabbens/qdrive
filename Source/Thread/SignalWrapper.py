from PyQt5.QtCore import QThread, pyqtSignal, QObject

class SignalWrapper(QObject):
    threadSignal = pyqtSignal(object, object)

    def __init__(self):
        QObject.__init__(self)