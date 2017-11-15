from code import InteractiveConsole


class Console(InteractiveConsole):
    def __init__(self, parent):
        super(Console, self).__init__(parent)

        self.initUI()

    def initUI(self):
        pass

    def enter(self, source):
        source = self.preprocess(source)
        self.runcode(source)

    @staticmethod
    def preprocess(source): return source

    # TODO: Finish this http://pythoncentral.io/embed-interactive-python-interpreter-console/