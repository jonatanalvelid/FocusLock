# -*- coding: utf-8 -*-

"""
Created on Wed Sep  6 14:06:03 2017

@author: jonatan.alvelid

"""


# import math
# from pyvisa import constants

from lantz import Action, Feat
# from lantz.messagebased import MessageBasedDriver
from lantz.drivers.legacy.serial import SerialDriver
# from lantz import Q_


class PCZPiezo(SerialDriver):
    """Driver for the PiezoConcept Z-piezo.
    """

#    DEFAULTS = {'ASRL': {'write_termination': '\r',
#                         'read_termination': '\r',
#                         'baud_rate': 19200,
#                         'bytesize': 8,
#                         'parity': constants.Parity.none,
#                         'stop_bits': constants.StopBits.one,
#                         'encoding': 'ascii',
#                         }}

    # TODO: add this in PyVISA
    # flow control flags
    # RTSCTS = False
    # DSRDTR = False
    # XONXOFF = False

    ENCODING = 'ascii'

    RECV_TERMINATION = '\n'
    SEND_TERMINATION = '\n'

    BAUDRATE = 115200
    BYTESIZE = 8
    PARITY = 'none'
    STOPBITS = 1

    #: flow control flags
    RTSCTS = False
    DSRDTR = False
    XONXOFF = False

    def query(self, arg):
        return super().query(arg)

    @Feat(read_once=True)
    def idn(self):
        """Get information of system, such as name, number of axis,...
        maximum stroke etc. """
#        return self.query('INFOS')
        dummyquery = 'dummy zpiezo answer'
        return dummyquery
    def initialize(self):
        super().initialize()


    # Z-MOVEMENT

    @Feat(units='micrometer')
    def absZ(self):
        """ Absolute Z position. """
        return float(self.query('GET_X').split()[0])

    @absZ.setter
    def absZ(self, value):
        """ Absolute Z position movement, in um. """
        self.query('MOVEX ' + str(float(value)) + 'u')

    def relZ(self, value):
        """ Relative Z position movement, in um. """
        if float(value) < 0:
            self.query('MOVRX +' + str(float(value))[1:7] + 'u')
        if float(value) > 0:
            self.query('MOVRX -' + str(float(value))[0:6] + 'u')
        if abs(float(value)) > 0.5:
                print('Warning: Step bigger than 500 nm.')

    @Action(units='micrometer')
    def move_relZ(self, value):
        """ Relative Z position movement, in um. """
        if float(value) < 0:
            self.query('MOVRX +' + str(round(float(value), 3))[1:7] + 'u')
        if float(value) > 0:
            self.query('MOVRX -' + str(round(float(value), 3))[0:6] + 'u')
        if abs(float(value)) > 0.5:
                print('Warning: Step bigger than 500 nm.')

    @Action(units='micrometer', limits=(100,))
    def move_absZ(self, value):
        """ Absolute Z position movement, in um. """
        self.query('MOVEX ' + str(round(float(value), 3)) + 'u')

    # CONTROL/STATUS

    @Feat()
    def timeStep(self):
        """ Get the time between each points sent by the RAM of the USB
        interface to the nanopositioner. """
        return self.query('GTIME')

    @timeStep.setter
    def timeStep(self, value):
        """ Set the time between each points sent by the RAM of the USB
        interface to the nanopositioner, in ms. """
        self.query('STIME ' + str(int(value)) + 'm')

    def close(self):
        self.finalize()


if __name__ == '__main__':
    import argparse
#    import lantz.log

    parser = argparse.ArgumentParser(description='Test Kentech HRI')
    parser.add_argument('-i', '--interactive', action='store_true',
                        default=False, help='Show interactive GUI')
    parser.add_argument('-p', '--port', type=str, default='COMXX',
                        help='Serial port to connect to')

    args = parser.parse_args()
#    lantz.log.log_to_screen(lantz.log.DEBUG)
    with PCZPiezo('COM4') as inst:
        if args.interactive:
            from lantz.ui.qtwidgets import start_test_app
            start_test_app(inst)
        else:
            # Add your test code here
            print('Non interactive mode')