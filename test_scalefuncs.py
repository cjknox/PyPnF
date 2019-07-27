import unittest
from typing import List

import numpy as np
import pandas as pd

import datadefs
import scalefuncs


class TestChartScales(unittest.TestCase):
    def test_chart_scale_one_hundred(self):
        self.assertEqual(scalefuncs.chart_scale_one_hundred(), [float(x) for x in range(0, 101, 2)])

    def test_chart_scale_percent(self):
        min_max_ranges = ((0, 10), (20, 30), (100, 110))
        for min, max in min_max_ranges:
            for percent in range(1, 11):
                scale = scalefuncs.chart_scale_percent(min, max, percent, ndigits=2)
                percent_test = 1 + (percent / 100.0)
                for i in range(len(scale)-1):
                    self.assertAlmostEqual(scale[i + 1]/scale[i], percent_test, delta=0.02)

    def test_chart_scale_traditional(self):
        traditional = scalefuncs.chart_scale_traditional
        self.assertEqual(traditional(4, 6), [4.0, 4.25, 4.5, 4.75, 5.0, 5.5, 6.0])
        self.assertEqual(traditional(18, 21), [18.0, 18.5, 19.0, 19.5, 20.0, 21.0])
        self.assertEqual(traditional(97, 104), [97.0, 98.0, 99.0, 100.0, 102.0, 104.0])
        self.assertEqual(traditional(195, 205), [194.0, 196.0, 198.0, 200.0, 204.0, 208.0])
        self.assertEqual(traditional(390, 410), [388.0, 392.0, 396.0, 400.0, 408.0, 416.0])
        self.assertEqual(traditional(780, 820), [776.0, 784.0, 792.0, 800.0, 816.0, 832.0])
        self.assertEqual(traditional(1580, 1660), [1568.0, 1584.0, 1600.0, 1632.0, 1664.0])
    
    def test_chart_scale_fixed_boxsize(self):
        fixed_boxsize = scalefuncs.chart_scale_fixed_boxsize
        self.assertEqual(fixed_boxsize(min_value=10, max_value=100, box_size=20), [0, 20, 40, 60, 80, 100])
        self.assertEqual(fixed_boxsize(min_value=4, max_value=6, box_size=0.25), [4.0, 4.25, 4.5, 4.75, 5.0, 5.25, 5.5, 5.75, 6.0])
        self.assertEqual(fixed_boxsize(20, 25, 1), [20.0, 21.0, 22.0, 23.0, 24.0, 25.0])
        self.assertEqual(fixed_boxsize(20, 23, 0.5), [20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0])
        self.assertEqual(fixed_boxsize(200, 300, 20), [200.0, 220.0, 240.0, 260.0, 280.0, 300.0])

    def __chart_scale__repr_(chart_scale):
        pass
        """        if len(chart_scale) < 10:
                    return str(chart_scale)
                else:
                    return '%s ... %s' % (str(chart_scale[:3]), str(chart_scale[-3:]) )
        """


class Test_FirstColumnDirection(unittest.TestCase):
    path = 'test_data.csv'
    df = pd.read_csv(path, index_col='date', na_values='null')
    scale_one_hundred = scalefuncs.chart_scale_one_hundred()
    scale_percent = scalefuncs.chart_scale_percent(1, 100, percent=6, ndigits=2)
    scale_traditional = scalefuncs.chart_scale_traditional(1, 100)
    scale_fixed_boxsize = scalefuncs.chart_scale_fixed_boxsize(min_value=5, max_value=100, box_size=5)
    # x_traditional	x_percent	x_100	x_101	o_traditional	o_percent	o_100

    def test_x_column(self):
        direction = datadefs.Direction.X
        self.assertEqual(direction, scalefuncs.getFirstColumnDirection(self.df, 'x_traditional', self.scale_traditional))
    
    def test_o_column(self):
        direction = datadefs.Direction.O

    def test_undefined_column(self):
        direction = datadefs.Direction.Undefined

    """
    def getFirstColumnDirection(df: DataFrame, column_name: str, chart_scale: List[float]):
        pass
    """

class Test__tradGetBoxSize(unittest.TestCase):
    def test_boxSize(self):
        box_func = scalefuncs._tradGetBoxSize
        self.assertEqual(box_func(-1.00), 0.0)
        self.assertEqual(box_func(0.01), 0.25)
        self.assertEqual(box_func(4.99), 0.25)
        self.assertEqual(box_func(5.00), 0.5)
        self.assertEqual(box_func(19.99), 0.5)
        self.assertEqual(box_func(20.00), 1.0)
        self.assertEqual(box_func(99.99), 1.0)
        self.assertEqual(box_func(100.00), 2.0)
        self.assertEqual(box_func(199.99), 2.0)
        self.assertEqual(box_func(200.00), 4.0)
        self.assertEqual(box_func(399.99), 4.0)
        self.assertEqual(box_func(400.00), 8.0)
        self.assertEqual(box_func(799.99), 8.0)
        self.assertEqual(box_func(800.00), 16.0)
        self.assertEqual(box_func(1599.99), 16.0)
        self.assertEqual(box_func(1600), 32.0)


def _tradAnchorBoxValue(value: float) -> float:
    if value <= 0.0:
        return 0.0
    box_size = scalefuncs._tradGetBoxSize(value)
    return math.floor(value/box_size) * box_size


def myround(x, prec=2, base=0.05):
    return round(base * round(float(x)/base), prec)


# Returns the chart_scale index and box value for a given price
def getIdxBoxForValue(value: float, direction, chart_scale: List[float]):
    pass

def getBoxForValue(value: float, direction, chart_scale: List[float]):
    pass

def getBoxesBetweenValues(start_value: float, end_value: float, chart_scale: List[float]) -> List[float]:
    pass

def getBoxesInReversals(price: float, num_reversal_boxes: int, direction, chart_scale: List[float]) -> List[float]:
    pass    

def getNextBoxUp(value: float, chart_scale: List[float]):
    pass

def getNextBoxDn(value: float, chart_scale: List[float]):
    pass

def getReversalUp(value: float, chart_scale: List[float], num_reversal_boxes: int = 3):
    pass

def getReversalDn(value: float, chart_scale: List[float], num_reversal_boxes: int = 3):
    pass

if __name__ == '__main__':
        unittest.main()
