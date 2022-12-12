import sys
from PyQt5.QtCore import Qt,pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import os
import Main


useStockfish = False

def changeUseStockFish(value):
    global useStockfish
    useStockfish = value == 2 

def clickedWhite():
    Main.start("w",useStockFish=useStockfish)

def clickedBlack():
    Main.start("b",useStockFish=useStockfish)


def window():
    app = QApplication([])
    app.setStyle('Fusion')
    palette = QPalette()
    #palette.setColor(QPalette.ButtonText, Qt.red)
    app.setPalette(palette)

    #General font
    absolute_path = os.path.dirname(__file__)
    relative_path = "./fonts/ka1.TTF"
    full_path = os.path.join(absolute_path, relative_path)
    QFontDatabase.addApplicationFont(full_path)

    #window
    win = QMainWindow()
    win.setGeometry(200,200,500,500)
    win.setFixedSize(500,500)
    win.setWindowTitle("ChessBot CV")
    win.setWindowIcon(QIcon('.\\Notebooks\\images\\logo.png'))

    #Prevent maximization
    win.setWindowFlags(win.windowFlags() | Qt.CustomizeWindowHint)
    win.setWindowFlags(win.windowFlags() & ~Qt.WindowMaximizeButtonHint)

    #Welcome
    label = QLabel(win)
    label.resize(350,40)
    label.setText("Bienvenido a ChessBot")
    label.setStyleSheet("font-size:16px;margin: 0 auto; border-radius:5px;background-color:white;border: 2px solid black;text-align:center")
    label.move(75,50)
    label.setFont(QFont("Karmatic Arcade",12))

    #Text
    label = QLabel(win)
    label.resize(340,35)
    label.setText("Elige tu color de pieza")
    label.setStyleSheet("font-size:15px;margin: 0 auto; border-radius:5px;background-color:white;border: 2px solid black;")
    label.move(80,100)
    label.setFont(QFont("Karmatic Arcade",12))

    negras = QPushButton(win)
    negras.setText("Negras")
    negras.move(150,200)
    negras.setStyleSheet("""
        QPushButton {
            background:white;
            border-radius:10px;
            border: 3px solid black
        }
        QPushButton:hover {
            background-color:#c7c7c7;
        }
    """)
    negras.resize(200,40)
    negras.setFont(QFont("Karmatic Arcade",12))
    negras.clicked.connect(clickedBlack)


    blancas = QPushButton(win)
    blancas.setText("Blancas")
    blancas.setFont(QFont("Karmatic Arcade",12))
    blancas.setStyleSheet("""
        QPushButton {
            background:white;
            border-radius:10px;
            border: 3px solid black
        }
        QPushButton:hover {
            background-color:#c7c7c7;
        }
    """)
    blancas.move(150,250)
    blancas.resize(200,40)
    blancas.clicked.connect(clickedWhite)

    

    checkbox = QCheckBox(win)
    checkbox.setText("Use Stockfish")
    checkbox.move(170,300)
    checkbox.resize(200,40)
    checkbox.setFont(QFont("Karmatic Arcade",10))
    checkbox.stateChanged.connect(changeUseStockFish)

   

    #image
    label = QLabel(win)
    pixmap = QPixmap('.\\Notebooks\\images\\logo.png')
    pixmap = pixmap.scaled(130, 130, Qt.KeepAspectRatio)
    label.setPixmap(pixmap)
    label.resize(500,500)
    label.move(180,150)
    label.lower()

    win.show()
    sys.exit(app.exec_())


window()