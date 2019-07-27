import unittest

import datadefs


class TestScale(unittest.TestCase):
    def test_ScaleType(self):
        scaletypes = datadefs.ScaleType
        expected = [datadefs.ScaleType.OneHundred, datadefs.ScaleType.Percent
                   ,datadefs.ScaleType.Traditional, datadefs.ScaleType.Undefined
                   ,datadefs.ScaleType.Fixed]
        for scale in scaletypes:
            self.assertIn(scale, expected)


class TestDirections(unittest.TestCase):
    def test_Direction(self):
        directions = datadefs.Direction
        expected = [datadefs.Direction.O, datadefs.Direction.Undefined, datadefs.Direction.X]
        for direction in directions:
            self.assertIn(direction, expected)


class TestTrends(unittest.TestCase):
    def test_Trend(self):
        trends = datadefs.Trend
        expected = [datadefs.Trend.Negative, datadefs.Trend.Positive, datadefs.Trend.Undefined]
        for trend in trends:
            self.assertIn(trend, expected)

#TODO: Column Tests

#TODO: Chart Tests 

if __name__ == '__main__':
        unittest.main()
