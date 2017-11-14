#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
import sys, os
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMenu
from ..cqcad import CQCADGui

@pytest.fixture(scope="session", autouse=True)
def do_something(request):
    # Make sure that these tests can import the cqcad modules properly
    encoding = sys.getfilesystemencoding()
    test_base_path = os.path.dirname(unicode(__file__, encoding))
    module_base_path = os.path.abspath(os.path.join(test_base_path, os.pardir))
    sys.path.insert(0, module_base_path)

def test_extensions_dropdown(qtbot, tmpdir):
    """
    Tests to ensure that the extensions dropdown on the toolbar works properly.

    :param qtbot: Bot for simulating user inputs
    :param tmpdir: Temporary directory
    :return: None
    """
    window = CQCADGui()
    window.show()
    qtbot.addWidget(window)

    # Make sure that the menu itself has the right items in it
    assert len(window.extsMenu.actions()) == 1
    assert window.extsMenu.actions()[0].iconText() == "Scripting"

    # Make sure that when the extensions dropdown items are clicked the right things happen
    if window.findChild(QMenu, "scriptMenu") is not None:
        assert window.extsMenu.actions()[0].isChecked() == True
        window.extsMenu.actions()[0].trigger()
        assert window.extsMenu.actions()[0].isChecked() == False
    else:
        assert window.extsMenu.actions()[0].isChecked() == False
        window.extsMenu.actions()[0].trigger()
        assert window.extsMenu.actions()[0].isChecked() == True

    # Make sure that the extensions menu is populated with items
    if window.findChild(QMenu, "scriptMenu") is None:
        # Make sure that the Scripting menu should be showing
        window.extsMenu.actions()[0].trigger()
    assert len(window.findChild(QMenu, "scriptMenu").actions()) == 3