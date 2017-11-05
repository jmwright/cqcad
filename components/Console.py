#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python console for CQCad

License: LGPL 3.0
"""
from code import InteractiveConsole


class Console(InteractiveConsole):
    def __init__(self):
        super(Console, self).__init__()

        self.initUI()

    def initUI(self):
        pass

    def enter(self, source):
        source = self.preprocess(source)
        self.runcode(source)

    @staticmethod
    def preprocess(source): return source

    # TODO: Finish this http://pythoncentral.io/embed-interactive-python-interpreter-console/