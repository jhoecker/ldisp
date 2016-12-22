#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import os
import signal
import sys

from PyQt5 import QtWidgets
from ldisp import lMainWindow

## version flag (python 2 or 3)
py_version = sys.version_info[0]          

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', dest='verbose',
                        action='store_true', help='Enables debug output.')
    parser.add_argument('-f', '--nofork', dest='foreground',
                        action='store_true', help='Foreground: Do not fork at startup')
    parser.add_argument('lfile', nargs='?')
    args = parser.parse_args()

    loglevel = logging.DEBUG if args.verbose else logging.WARNING
    logging.basicConfig(format='%(levelname)s: %(message)s',
                        level=loglevel)

    if args.verbose:
        args.foreground = True

    return showMainWindow(args.lfile, foreground=args.foreground)

    
def showMainWindow(fname, foreground=False):
    
    if not foreground:
        # Close stdout and stderr to avoid polluting the terminal
        os.close(1)
        os.close(2)

        if os.fork() > 0:
            return

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtWidgets.QApplication(sys.argv)
    
    window = lMainWindow.ldispMain(fname)
    
    window.show()
    return app.exec_()

if __name__ == '__main__':
    main()
