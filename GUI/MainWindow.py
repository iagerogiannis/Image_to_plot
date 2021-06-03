from PyQt5.QtWidgets import QMainWindow
from GUI.Workspace import Workspace
from GUI.MainMenu import MainMenu


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setGeometry(200, 80, 600, 600)
        self.setWindowTitle("Image to Plot with Splines")

        self.mainMenu = MainMenu(self)
        self.plotPanel = Workspace(self)
        self.setCentralWidget(self.plotPanel)
        self.show()
