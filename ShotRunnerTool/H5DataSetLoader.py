import numpy


def load(group):
    value = group[()]
    if isinstance(value, getattr(numpy, 'ndarray')):  # pylint reports this as an error otherwise
        return list(value)
    try:
        return numpy.asscalar(value)
    except:
        pass
    return value
