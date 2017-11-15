from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMdiArea

__title__ = QCoreApplication.translate('cqcad', "Scripting Triple")

def execute(mdiArea):
    print(__title__ + " Layout Activated")