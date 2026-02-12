"""
CollectionUtil - Converted from Java source
Original: tools/CollectionUtil.java
Package: tools
"""

from typing import List
from typing import Optional, Any


class CollectionUtil:
    """
    Class CollectionUtil
    """

    def __init__(self):
        pass
        pass


    def copyFirst(self, list: list, count: int) -> Any:
        ret = [] < count) ? list : count)
        i = 0
        for elem in list:
            ret.add(elem)
            if i++ > count:
                break
        return ret

