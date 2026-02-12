"""
Randomizer - Converted from Java source
Original: server/Randomizer.java
Package: server
"""

from random import Random
from typing import Optional, Any
import random


class Randomizer:
    """
    Class Randomizer
    """

    # Static initializer
    # rand = Random()


    @staticmethod
    def nextInt() -> int:
        return Randomizer.rand.nextInt()

    @staticmethod
    def nextInt_arg0(arg0: int) -> int:
        return Randomizer.rand.nextInt(arg0)

    def nextBytes(self, bytes: bytes) -> None:
        Randomizer.rand.nextBytes(bytes)

    def nextBoolean(self) -> bool:
        return Randomizer.rand.nextBoolean()

    def nextDouble(self) -> float:
        return Randomizer.rand.nextDouble()

    def nextFloat(self) -> float:
        return Randomizer.rand.nextFloat()

    def nextLong(self) -> int:
        return Randomizer.rand.nextLong()

    def rand(self, lbound: int, ubound: int) -> int:
        return (int)(Randomizer.rand.nextDouble() * (ubound - lbound + 1) + lbound)

