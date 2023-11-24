from PyQt5.QtWidgets import *
from PyQt5.QtQml import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QGuiApplication
import sys, os
from Source.Program import Program


def main():
    app = QGuiApplication(sys.argv)
    os.environ["QT_QUICK_CONTROLS_STYLE"] = "Material"
    p = Program(app)
 
    sys.exit(app.exec())

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)