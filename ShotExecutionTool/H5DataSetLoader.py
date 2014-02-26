__author__ = 'Blake'

import numpy as np


class H5DataSetLoader(object):
    @staticmethod
    def load(group):
        value = group[()]
        if isinstance(value, np.ndarray):
            return list(value)
        else:
            return value
