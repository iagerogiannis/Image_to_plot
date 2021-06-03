from PyQt5.QtWidgets import QMainWindow, QAction


class MainMenu:

    def __init__(self, parent: QMainWindow):
        super().__init__()
        self.parent = parent
        self.centralWindow = self.parent
        self.buildMenu()

    def buildMenu(self):

        mainMenu = self.parent.menuBar()

        fileMenu = mainMenu.addMenu("File")

        helpMenu = mainMenu.addMenu("Help")

        aboutAction = QAction("About", self.parent)
        aboutAction.setStatusTip("Shows information about the application")

        helpMenu.addAction(aboutAction)

        self.parent.statusBar()

