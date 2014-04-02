import keyword
import re

__author__ = 'Blake'


class VariableNameValidator(object):

    def __init__(self):
        pass

    @staticmethod
    def isValidVariableName(candidate):
        return re.match(
            "[_A-Za-z][_a-zA-Z0-9]*$", candidate) and not keyword.iskeyword(candidate)
