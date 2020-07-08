# -*- coding: utf-8 -*-

# General imports
import os
import time

# Scientific python packages and software imports
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import Dock, DockArea
from lantz import Q_

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

        """
        # Actions in menubar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')

        self.savePresetAction = QtGui.QAction('Save configuration...', self)
        self.savePresetAction.setShortcut('Ctrl+S')
        self.savePresetAction.setStatusTip('Save camera & recording settings')
        savePresetFunction = lambda: guitools.savePreset(self)
        self.savePresetAction.triggered.connect(savePresetFunction)
        fileMenu.addAction(self.savePresetAction)
        fileMenu.addSeparator()

        # Potentially remove all this?
        self.presetsMenu = QtGui.QComboBox()
        self.presetDir = datapath
        if not(os.path.isdir(self.presetDir)):
            self.presetDir = os.path.join(os.getcwd(), 'control\\Presets')
        for preset in os.listdir(self.presetDir):
            self.presetsMenu.addItem(preset)
        self.loadPresetButton = QtGui.QPushButton('Load preset')
        loadPresetFunction = lambda: guitools.loadPreset(self)
        self.loadPresetButton.pressed.connect(loadPresetFunction)
        """
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
