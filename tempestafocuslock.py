# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui

def main():

    from control import control
    import control.instruments as instruments

    app = QtGui.QApplication([])

    scan_z = instruments.ScanZ('COM5')

    print(scan_z.idn)

    webcam_focus_lock = instruments.CameraTIS(0, 0, 0, 0)

    win = control.TempestaFocusLockGUI(scan_z, webcam_focus_lock)
    win.show()
    app.exec_()

def analysisApp():

    from analysis import analysis

    app = QtGui.QApplication([])

    win = analysis.AnalysisWidget()
    win.show()

    app.exec_()

