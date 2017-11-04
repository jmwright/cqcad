#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Custom code editor for CQCad

License: LGPL 3.0
"""
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTextEdit

class CodeEdit(QTextEdit):
    def __init__(self):
        super(CodeEdit, self).__init__()

        self.initUI()

    def initUI(self):
        pass