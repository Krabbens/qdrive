from PyQt5 import QtCore
from PyQt5.QtCore import QThread
from Source.Debug import Debug
from Source.ThreadEscape import ThreadEscape as TE

class Connector(TE):
    def __init__(self, program, parent=None):
        super().__init__()
        self.program = program

    def init(self):
        self.root = self.program.engine.rootObjects()[0]

    def toggle_loader(self):
        self.root.toggleLoader()

    def set_current_directory_text(self, text):
        self.root.setCurrentDirectoryText(text)

    @TE.escape_thread
    def set_gradient_in_delegate(self, index, color):
        Debug()(QThread.currentThread(), int(QThread.currentThreadId()))
        self.root.setGradientInDelegate(index, color)