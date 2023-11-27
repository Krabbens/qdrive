from PyQt5 import QtCore, QtWidgets, QtQml

class Connector(QtCore.QObject):
    def __init__(self, program, parent=None):
        super(Connector, self).__init__(parent)
        self.program = program

    def init(self):
        self.root = self.program.engine.rootObjects()[0]

    def toggle_loader(self):
        self.root.toggleLoader()

    def set_current_directory_text(self, text):
        self.root.setCurrentDirectoryText(text)