import os


class QssHelper:
    def __init__(self):
        pass

    @staticmethod
    def ReadQss(style):
        with open(style, 'r') as f:
            return f.read()