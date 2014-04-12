import keyword
import re


def isValidVariableName(candidate):
    return re.match("[_A-Za-z][_a-zA-Z0-9]*$", candidate) and not keyword.iskeyword(candidate)
