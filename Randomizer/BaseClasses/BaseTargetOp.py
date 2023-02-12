from typing import IO


class BaseTargetOp(object):
    def __init__(self, file: IO, params = None):
        self.params = params
        self.file = file
