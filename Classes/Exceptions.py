class ClassDdIsNone(Exception):
    def __init__(self, text):
        self.txt = text


class UnknownCommand(Exception):
    def __init__(self, text):
        self.txt = text


class InvalidString(Exception):
    def __init__(self, text):
        self.txt = text


class RunFunctionError(Exception):
    def __init__(self, text):
        self.txt = text


class GetJsonError(Exception):
    def __init__(self, text):
        self.txt = text


class SetJsonError(Exception):
    def __init__(self, text):
        self.txt = text


class CorrectionJsonError(Exception):
    def __init__(self, text):
        self.txt = text
