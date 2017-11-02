#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
from PyQt5 import QtCore
from ..cqcad import CQCADGui

def test_menu_navigation(qtbot, tmpdir):
    '''
    test to ensure basic find files functionality is working.
    '''
    window = CQCADGui()
    window.show()
    qtbot.addWidget(window)

    # Test the recent scripts/projects menu
    qtbot.mouseClick(window.recentMenu, QtCore.Qt.LeftButton)
    assert len(window.recentMenu.actions()) == 0

    # Test the examples menu
    qtbot.mouseClick(window.examplesMenu, QtCore.Qt.LeftButton)
    assert len(window.examplesMenu.actions()) == 0  # TODO: Update this when the CadQuery library is integrated
