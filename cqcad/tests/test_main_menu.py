#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
import sys, os
from PyQt5 import QtCore

# encoding = sys.getfilesystemencoding()
# test_base_path = os.path.dirname(__file__)
# module_base_path = os.path.abspath(os.path.join(test_base_path, os.pardir))
# sys.path.insert(0, module_base_path)

from cqcad.CQCadWindow import CQCadWindow

def test_menu_navigation(qtbot, tmpdir):
    '''
    test to ensure basic menu navigation and operation is working
    '''
    window = CQCadWindow()
    window.show()
    qtbot.addWidget(window)

    # Test the recent scripts/projects menu
    qtbot.mouseClick(window.recentMenu, QtCore.Qt.LeftButton)
    assert len(window.recentMenu.actions()) == 0

    # Test the examples menu
    qtbot.mouseClick(window.examplesMenu, QtCore.Qt.LeftButton)
    assert len(window.examplesMenu.actions()) == 0  # TODO: Update this when the CadQuery library is integrated

    # Test the dock and its visibility menu checkbox
    dockActChecked = window.dockAct.isChecked()
    assert(dockActChecked == window.dock.isVisible())
    window.dockAct.trigger()
    assert(window.dockAct.isChecked() is not dockActChecked)
    assert(window.dock.isVisible() is not dockActChecked)
