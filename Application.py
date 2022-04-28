from ControlPanel import ControlPanel
from PySide6.QtWidgets import QApplication

class Application(QApplication):
    def __init__(self):
        super(Application, self).__init__()

        self.controlpanel = ControlPanel()

        self.exec()


if __name__ == "__main__":
    Application()