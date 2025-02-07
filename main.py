from gui.window import MainWindow
from PyQt5.QtWidgets import QApplication
import sys

""" UI prasības:

1. Diagrammā:
  * Sarkanā krāsā [2, 5, 6, 8.];
  * Dzeltenā krāsā [1, 7, 9.];
  * Zaļā krāsa [3, 4.].

2. Printēšanas funkciju, kurā izprintē to diagrammu un apkopojumu.
2.1 Apkopojumā:
   * vienību skaits;
   * visus tos rezultātus;
   * brīva vieta komentāriem.

"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())