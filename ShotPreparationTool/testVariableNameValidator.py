from unittest import TestCase

from VariableNameValidator import VariableNameValidator


__author__ = 'Blake'


class TestVariableNameValidator(TestCase):
    invalidNames = [
        'Name with spaces',
        'Name.with.periods',
        'Name-with-dashes',
        '0NameThatStartsWithNumber',
        'NameWithIllegalCharacters!$%^'
        'continue'
    ]

    validNames = [
        'lowercase',
        'UPPERCASE',
        'camelCase',
        'PascalCase'
    ]

    def test_isValidVariableName(self):
        for name in self.invalidNames:
            self.assertFalse(VariableNameValidator.isValidVariableName(name))
        for name in self.validNames:
            self.assertTrue(VariableNameValidator.isValidVariableName(name))
