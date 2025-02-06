from gui.window import MainWindow
from PyQt5.QtWidgets import QApplication
import sys

""" UI prasības:
1. Tā lapiņa arī parādas blakus uz ekrāna.
2. Diagrammā:
2.1 Sarkanā krāsā [2, 5, 6, 8.]
2.2 Dzeltenā krāsā [1, 7, 9.]
2.3. Zaļā krāsa [3, 4.].

3. Printēšanas funkciju, kurā izprintē to diagrammu un apkopojumu.

Apkopojumā:
 * vienību skaits,
 * visus tos rezultātus,
 * brīva vieta komentāriem,
"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())