
from typing import List, Tuple
import sources.constants as constants

def rect_area(rect: Tuple[Tuple[int, int], Tuple[int, int]]) -> int:
    """
        [[xmin, ymin], [xmax, ymax]]
    """
    (xmin, ymin), (xmax, ymax) = rect
    return (xmax - xmin + 1) * (ymax - ymin + 1)

def intersection_over_reunion(rect1, rect2) -> float:
    """
    Returns the intersection over reunion
    """
    (x1min, y1min), (x1max, y1max) = rect1
    (x2min, y2min), (x2max, y2max) = rect2

    xmin = max(x1min, x2min)
    ymin = max(y1min, y2min)
    xmax = min(x1max, x2max)
    ymax = min(y1max, y2max)

    if xmin > xmax or ymin > ymax:
        return 0.
    
    intersection = rect_area(((xmin, ymin), (xmax, ymax)))
    reunion = rect_area(rect1) + rect_area(rect2) - intersection

    return intersection / reunion

def non_max_suppression(windows: List[Tuple[Tuple, float]]):
    """
    Removes all windows with a smaller precision.
    """
    good_windows = []
    
    windows.sort(key=lambda x: -x[-1])

    for window in windows:
        ok = True
        for good_window in good_windows:
            inter_over_reun = intersection_over_reunion(window[0], good_window[0])
            if inter_over_reun > constants.NON_MAX_SUPPRESSION_THRESHOLD:
                ok = False
                break

        if ok:
            good_windows.append(window)

    # TODO: Rescale windows depending on class
    return good_windows