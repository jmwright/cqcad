#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
import sys, os
from PyQt5 import QtCore
from ..cqcad import CQCADGui

@pytest.fixture(scope="session", autouse=True)
def do_something(request):
    # Make sure that these tests can import the cqcad modules properly
    encoding = sys.getfilesystemencoding()
    test_base_path = os.path.dirname(unicode(__file__, encoding))
    module_base_path = os.path.abspath(os.path.join(test_base_path, os.pardir))
    sys.path.insert(0, module_base_path)

    # request.addfinalizer(finalizer_function)

def test_menu_navigation(qtbot, tmpdir):
    '''
    test to ensure basic menu navigation and operation is working
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

    # Test the dock and its visibility menu checkbox
    dockActChecked = window.dockAct.isChecked()
    assert(dockActChecked == window.dock.isVisible())
    window.dockAct.trigger()
    assert(window.dockAct.isChecked() is not dockActChecked)
    assert(window.dock.isVisible() is not dockActChecked)
