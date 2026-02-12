"""
MapleDiseaseValueHolder - Converted from Java source
Original: client/MapleDiseaseValueHolder.java
Package: client
"""

from typing import Optional, Any


class MapleDiseaseValueHolder:
    """
    Class MapleDiseaseValueHolder
    Implements: Serializable
    """

    serialVersionUID = 9179541993413738569

    def __init__(self, disease: Any, startTime: int, length: int):
        self.startTime = 0
        self.length = 0
        self.disease = None
        self.disease = disease
        self.startTime = startTime
        len(self) = length


