"""
    Definitions of basic data types used in PyPnF.
"""

from enum import Enum, unique
from typing import List

import numpy as np  # type: ignore
import pandas as pd  # type: ignore

import scalefuncs


@unique
class ScaleType(Enum):
    OneHundred = '100 Percent'
    Percent = 'Percent'
    Traditional = 'Traditional'
    Fixed = 'Fixed Box Size'
    Undefined = 'Undefined'


@unique
class Direction(Enum):
    X = 'X'
    O = 'O'
    Undefined = '-'


@unique
class Trend(Enum):
    Positive = '+'
    Negative = '-'
    Undefined = 'U'


# Column
class Column(object):

    def __init__(self, start_date, start_value: float, direction: Direction, 
                 num_reversal_boxes: int, chart_scale: List[float]) -> None:
        self.start_date = start_date
#        self.start_value = start_value
        self.direction = direction
        self.num_reversal_boxes = num_reversal_boxes
        self.chart_scale = chart_scale
        if self.direction == Direction.X:
            self.next_box = scalefuncs.getNextBoxUp(start_value, self.chart_scale)
            self.reversal_box = scalefuncs.getReversalDn(start_value, self.chart_scale, self.num_reversal_boxes)
        elif self.direction == Direction.O:
            self.next_box = scalefuncs.getNextBoxDn(start_value, self.chart_scale)
            self.reversal_box = scalefuncs.getReversalUp(start_value, self.chart_scale, self.num_reversal_boxes)
        else:
            raise ValueError('Column cannot be created for direction {0}.'.format(self.direction))
        self.end_date = start_date
        self.boxes = [scalefuncs.getBoxForValue(start_value, self.direction, self.chart_scale)]

    def __repr__(self):
        return 'Start Date:\t%s\nStart Value:\t%s\nSNext Box:\t%s\nReversal Box:\t%s\nDirection:\t%s' % (
                self.start_date, self.start_value, self.next_box, self.reversal_box, self.direction)

    def print_boxes(self, num_to_show: int = 10):
        if len(self.boxes) <= num_to_show:
            return self.boxes
        else:
            return self.boxes[:int(num_to_show/2.0)] + ['...{' + str(len(self.boxes) - num_to_show) + '}...'] + self.boxes[-int(num_to_show/2.0 + 0.9):]

# Chart
class Chart(object):

    def __init__(self, start_date, num_reversal_boxes = 3):
        self.scale_type = ScaleType.Undefined
        self.scale = []
        self.columns = []
        self.start_date = start_date
        self.end_date = start_date
        self.num_reversal_boxes = num_reversal_boxes

    def set_chart_scale_one_hundred(self):
        if self.scale_type != ScaleType.Undefined:
            raise RuntimeError('This chart has already been setup.')
        self.scale_type = ScaleType.OneHundred
        self.scale = scalefuncs.chart_scale_one_hundred()

    def set_chart_scale_percent(self, min_value: float=1.0, max_value: float=100.0,
                            percent: float=6.5, ndigits: int=2):
        if self.scale_type != ScaleType.Undefined:
            raise RuntimeError('This chart has already been setup.')
        self.scale_type = ScaleType.Percent
        self.scale = scalefuncs.chart_scale_percent(min_value, max_value, percent, ndigits)

    def set_chart_scale_traditional(self, min_value: float=1.0,
                                max_value: float=100.0,
                                boxSize=None):
        if self.scale_type != ScaleType.Undefined:
            raise RuntimeError('This chart has already been setup.')
        self.scale_type = ScaleType.Traditional
        self.scale = scalefuncs.chart_scale_traditional(min_value, max_value)

    def set_chart_scale_fixed_box_size(self, min_value: float = 1.0, max_value: float = 100.0, box_size=1):
        if self.scale_type != ScaleType.Undefined:
            raise RuntimeError('This chart has already been setup.')
        self.scale_type = ScaleType.Fixed
        self.scale = scalefuncs.chart_scale_fixed_boxsize(min_value, max_value, box_size)

    def append_column(self, column: Column):
        if self.scale_type == ScaleType.Undefined:
            raise RuntimeError('The box scale has not been defined for this chart; unable to add a column.')
        self.columns.append(column)

    def get_dataframe(self):
        df = pd.DataFrame(index=self.scale)
        for column in self.columns:
            df[column.start_date] = pd.Series(column.direction.name, index=column.boxes)
        df[''] = pd.Series(self.scale, index=self.scale)
        df.replace(np.nan, '', inplace=True)
        return df.sort_index(ascending=False)
