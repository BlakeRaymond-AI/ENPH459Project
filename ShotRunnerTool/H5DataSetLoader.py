import numpy


def load(group):
    value = group[()]
    if isinstance(value, getattr(numpy, 'ndarray')):  # pylint reports this as an error otherwise
        return list(value)
    else:
        return value
