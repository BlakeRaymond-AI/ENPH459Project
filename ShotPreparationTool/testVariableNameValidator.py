from unittest import TestCase
from ShotPreparationTool.VariableNameValidator import isValidVariableName


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
            self.assertFalse(isValidVariableName(name))
        for name in self.validNames:
            self.assertTrue(isValidVariableName(name))
