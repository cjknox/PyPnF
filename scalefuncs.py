"""
    Functions used for setting chart scales and 
    getting the box a value falls within.
"""
import math  # type: ignore
from typing import List

from pandas import DataFrame  # type: ignore

import datadefs


def chart_scale_one_hundred() -> List[float]:
    '''Returns the scale for a zero to 100 percent chart'''
    return [float(x) for x in range(0, 101, 2)]


def chart_scale_percent(min_value: float=1.0, max_value: float=100.0, percent: float=6.5, ndigits: int=2) -> List[float]:
    if min_value <= 0.0 or max_value <= 0.0:
        return []
    percentInc = percent/100.0 + 1.0
    nextPoint = min_value
    chart_scale = [round(float(min_value), ndigits)]
    while nextPoint <= max_value:
        nextPoint *= percentInc
        chart_scale.append(round(float(nextPoint), ndigits))
    return chart_scale


def chart_scale_traditional(min_value: float=1.0, max_value: float=100.0) -> List[float]:
    '''Returns the scale for the traditional chart.'''
    nextPoint = _getBoxAnchorValue(min_value)
    chart_scale = [nextPoint]
    while nextPoint < max_value:
        nextPoint = _getBoxAnchorValue(nextPoint + _tradGetBoxSize(nextPoint))
        chart_scale.append(nextPoint)
    return chart_scale


def chart_scale_fixed_boxsize(min_value: float = 1.0, max_value: float = 100.0, box_size=1) -> List[float]:
    '''Returns the scale with a fixed box size'''
    nextPoint = _getBoxAnchorValue(min_value, box_size)
    chart_scale = [nextPoint]
    while nextPoint < max_value:
        nextPoint += box_size
        chart_scale.append(nextPoint)
    return chart_scale
 

def __chart_scale__repr_(chart_scale):
    if len(chart_scale) < 10:
        return str(chart_scale)
    else:
        return '%s ... %s' % (str(chart_scale[:3]), str(chart_scale[-3:]) )


def getFirstColumnDirection(df: DataFrame, column_name: str, chart_scale: List[float]):
    start_value = df[column_name][0]
    next_box_up = getNextBoxUp(start_value, chart_scale)
    next_box_dn = getNextBoxDn(start_value, chart_scale)
    rev_box_up = getReversalUp(start_value, chart_scale)
    rev_box_dn = getReversalDn(start_value, chart_scale)
    next_box_dir = datadefs.Direction.Undefined
    rev_box_dir = datadefs.Direction.Undefined

    for date, price in df[column_name].iteritems():
        #TODO this will need to be fixed to handle X and O for getIdxBoxForValue and getting box values for each (X O)
        _, box_value = getIdxBoxForValue(price, datadefs.Direction.Undefined, chart_scale)
        if box_value >= rev_box_up:
            rev_box_dir = datadefs.Direction.X
            break   # a reversal direction is stronger
        elif box_value <= rev_box_dn:
            rev_box_dir = datadefs.Direction.O
            break
        elif box_value >= next_box_up:
            if next_box_dir == datadefs.Direction.Undefined:
                #only set this for the first trigger
                next_box_dir= datadefs.Direction.X
        elif box_value <= next_box_dn:
            if next_box_dir == datadefs.Direction.Undefined:
                #only set this for the first trigger
                next_box_dir = datadefs.Direction.O
        else:
            pass
            # no defined Direction
    if rev_box_dir != datadefs.Direction.Undefined:
        return rev_box_dir
    else:
        return next_box_dir


def _tradGetBoxSize(value: float) -> float:
    if value < 0:
        return 0.0
    if value < 5:    # 0 < 5 is 0.25
        return 0.25
    if value < 20:   # 5 < 20 is 0.50
        return 0.5
    if value < 100:  # 20 < 100 is 1
        return 1.0
    if value < 200:  # 100 < 200 is 2
        return 2.0
    if value < 400:  # 200 < 400 is 4
        return 4.0
    if value < 800:  # 400 < 800 is 8
        return 8.0
    if value < 1600:  # 800 < 1600 is 16
        return 16.0
    return 32.0  # 1600 and above is 32


def _getBoxAnchorValue(value: float, box_size: float = None) -> float:
    if value <= 0.0:
        return 0.0
    if not box_size:
        box_size = _tradGetBoxSize(value)
    if box_size <= 0.0:
        raise ValueError("box_size cannot be zero or negative.")
    return math.floor(value/box_size) * box_size


def myround(x, prec=2, base=0.05):
    return round(base * round(float(x)/base), prec)


# Returns the chart_scale index and box value for a given price
def getIdxBoxForValue(value: float, direction, chart_scale: List[float]):
    if value < min(chart_scale):
        raise LookupError("Value less than lowest scale value")
    if value > max(chart_scale):
        raise LookupError("Value greater than highest scale value")
    if direction == datadefs.Direction.X or direction == datadefs.Direction.Undefined:
        for index, item in enumerate(chart_scale):
            if index == len(chart_scale) - 1 and value == item:
                return index, item
            if value >= item and value < chart_scale[index + 1]:
                return index, item

    elif direction == datadefs.Direction.O:
        for index, item in enumerate(chart_scale):
            if value <= item:
                return index, item
        return index, item  #Is this correct?
    else:
        raise ValueError("The column direction {1} isn't handled in scalefuncs.getIdxBoxForValue".format(direction))
    raise LookupError("The value wasn't placed in the scale.")

def getBoxForValue(value: float, direction, chart_scale: List[float]) -> float:
    _, box = getIdxBoxForValue(value, direction, chart_scale)
    return box

def getBoxesBetweenValues(start_value: float, end_value: float, direction, chart_scale: List[float]) -> List[float]:
    lo_val = start_value if start_value <= end_value else end_value
    hi_val = end_value if start_value <= end_value else start_value
    lo_idx, lo_box = getIdxBoxForValue(lo_val, direction, chart_scale)
    hi_idx, hi_box = getIdxBoxForValue(hi_val, direction, chart_scale)
    boxes = []
    for idx in range(lo_idx, hi_idx + 1):
        boxes.append(chart_scale[idx])
    return boxes

def getBoxesInReversals(price: float, num_reversal_boxes: int, direction, chart_scale: List[float]) -> List[float]:
    idx, box = getIdxBoxForValue(price, direction, chart_scale)
    if direction == datadefs.Direction.X:
        idx = min(idx + 1, len(chart_scale))
        idx_rev = (idx - (num_reversal_boxes))# direction reversed up; fill in lower boxes
        return chart_scale[idx_rev:idx]
    elif direction == datadefs.Direction.O:
        idx_rev = idx + (num_reversal_boxes) # direction reversed down; fill in higher boxes
        return chart_scale[idx:idx_rev]
    else:
        raise ValueError('Cannot fill in reversal boxes for %s.') % direction
    

def getNextBoxUp(value: float, chart_scale: List[float]):
    index, item = getIdxBoxForValue(value, datadefs.Direction.X, chart_scale)
    num_boxes = len(chart_scale)
    if index < num_boxes:
        return chart_scale[index + 1]
    else:
        return chart_scale[num_boxes]  # does this correctly handle when value is in highest box?


def getNextBoxDn(value: float, chart_scale: List[float]):
    index, item = getIdxBoxForValue(value, datadefs.Direction.O, chart_scale)
    if index > 0:
        return chart_scale[index - 1]
    else:
        return chart_scale[0]  # does this correctly handle when value is in lowest box?


def getReversalUp(value: float, chart_scale: List[float], num_reversal_boxes: int = 3):
    index, item = getIdxBoxForValue(value, datadefs.Direction.O, chart_scale)
    if index <= len(chart_scale) - num_reversal_boxes:
        return chart_scale[index + num_reversal_boxes]
    else:
        return chart_scale[len(chart_scale)]  # does this correctly handle when reversal box is off scale?


def getReversalDn(value: float, chart_scale: List[float], num_reversal_boxes: int = 3):
    index, item = getIdxBoxForValue(value, datadefs.Direction.X, chart_scale)
    if index >= num_reversal_boxes:
        return chart_scale[index - num_reversal_boxes]
    else:
        return chart_scale[0]  # does this correctly handle when reversal box is off scale?
