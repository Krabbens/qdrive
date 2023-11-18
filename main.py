from PyQt6.QtWidgets import *
from PyQt6.QtQml import *
from PyQt6.QtCore import *
from PyQt6.QtGui import QGuiApplication
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