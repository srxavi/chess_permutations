import unittest

from chess.processing import parmap


class TestProcessing(unittest.TestCase):

    def test_parmap(self):
        def func(a):
            return a
        input_params = [(1,)]
        result = parmap(func, input_params, 1)
        self.assertEquals([1], result)
