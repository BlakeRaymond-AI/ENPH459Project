__author__ = 'Blake'


class FluentDictionary:
    def __init__(self, source):
        for key, value in source.items():
            if isinstance(value, dict):
                setattr(self, key, FluentDictionary(value))
            else:
                setattr(self, key, value)
