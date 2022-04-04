class KeyboardLevelError(Exception):
    def __init__(self, text):
        self.text = text


class KeyboardGeneratorError(Exception):
    def __init__(self, text):
        self.text = text