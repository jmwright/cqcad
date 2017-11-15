#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CQCad GUI entry point

Sets up the CQCad GUI for use - Pulls settings and populates menus.

License: LGPL 3.0
"""
import sys
from PyQt5.QtWidgets import QApplication
from CQCadWindow import CQCadWindow

def main():
    app = QApplication(sys.argv)
    cqcad = CQCadWindow()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()