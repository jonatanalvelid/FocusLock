# -*- coding: utf-8 -*-

# General imports
import os
import time

# Scientific python packages and software imports
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import Dock, DockArea

# Tempesta control imports
import control.focus as focus
import control.guitools as guitools

datapath = r"C:\\Users\\STEDred\Documents\defaultTempestaData"


class FileWarning(QtGui.QMessageBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TempestaFocusLockGUI(QtGui.QMainWindow):
    """Main GUI class. This class calls other modules in the control folder

    :param Scanner scanZ: object controlling a Piezoconcept Z-scanning inset
    """

    liveviewStarts = QtCore.pyqtSignal()
    liveviewEnds = QtCore.pyqtSignal()

    def __init__(self, scan_z, webcam_focus_lock, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.scan_z = scan_z

        self.filewarning = FileWarning()

        # Dock widget
        dockArea = DockArea()

        # Focus lock widget
        focusDock = Dock("Focus lock", size=(500, 500))
        self.focusWidget = focus.FocusWidget(self.scan_z, webcam_focus_lock)
        focusDock.addWidget(self.focusWidget)
        dockArea.addDock(focusDock, "left")

        self.setWindowTitle('Tempesta - Focus lock edition')
        self.cwidget = QtGui.QWidget()
        self.setCentralWidget(self.cwidget)

        # Widgets' layout
        layout = QtGui.QGridLayout()
        self.cwidget.setLayout(layout)
        layout.addWidget(dockArea, 0, 0, 1, 1)

    def closeEvent(self, *args, **kwargs):
        """closes the different devices. Resets the NiDaq card,
        turns off the lasers and cuts communication with the SLM"""
        try:
            self.lvthread.terminate()
        except:
            pass

        super().closeEvent(*args, **kwargs)


if __name__ == "main":
    pass
