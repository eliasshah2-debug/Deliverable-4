"""
fraction.py - Task 2, Deliverable 4 (INF201)

A Fraction class representing a rational number numerator/denominator.

Invariants (always true for every Fraction object):
    * numerator and denominator are ints
    * denominator > 0  (the sign is always carried by the numerator)
    * the fraction is stored in lowest terms, e.g. Fraction(2, 4) -> 1/2
"""

from math import gcd


class Fraction:
    """A fraction numerator/denominator with integer parts and denominator > 0."""

    def __init__(self, numerator: int, denominator: int = 1):
        # bool is a subclass of int in Python, so exclude it explicitly
        for name, val in (("numerator", numerator), ("denominator", denominator)):
            if not isinstance(val, int) or isinstance(val, bool):
                raise TypeError(f"{name} must be an int, got {type(val).__name__}")

        if denominator <= 0:
            raise ValueError("denominator must be strictly positive (> 0)")

        # Reduce to lowest terms so that equal fractions look the same
        common = gcd(numerator, denominator)
        self._numerator = numerator // common
        self._denominator = denominator // common

    # ------------------------------------------------------------------
    # Read-only attributes
    # ------------------------------------------------------------------
    @property
    def numerator(self) -> int:
        return self._numerator

    @property
    def denominator(self) -> int:
        return self._denominator

    # ------------------------------------------------------------------
    # Helper
    # ------------------------------------------------------------------
    @staticmethod
    def _convert(other):
        """Turn an int into a Fraction; return None for unsupported types."""
        if isinstance(other, Fraction):
            return other
        if isinstance(other, int) and not isinstance(other, bool):
            return Fraction(other, 1)
        return None

    # ------------------------------------------------------------------
    # Comparisons
    # a/b ? c/d  <=>  a*d ? c*b   (valid because b > 0 and d > 0)
    # ------------------------------------------------------------------
    def __eq__(self, other):
        other = self._convert(other)
        if other is None:
            return NotImplemented
        # Both are in lowest terms, so equal values have equal parts
        return (self.numerator == other.numerator
                and self.denominator == other.denominator)

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return NotImplemented
        return not result

    def __lt__(self, other):
        other = self._convert(other)
        if other is None:
            return NotImplemented
        return self.numerator * other.denominator < other.numerator * self.denominator

    def __le__(self, other):
        other = self._convert(other)
        if other is None:
            return NotImplemented
        return self.numerator * other.denominator <= other.numerator * self.denominator

    def __gt__(self, other):
        other = self._convert(other)
        if other is None:
            return NotImplemented
        return self.numerator * other.denominator > other.numerator * self.denominator

    def __ge__(self, other):
        other = self._convert(other)
        if other is None:
            return NotImplemented
        return self.numerator * other.denominator >= other.numerator * self.denominator

    # Equal fractions must have equal hashes since we define __eq__
    def __hash__(self):
        return hash((self.numerator, self.denominator))

    # ------------------------------------------------------------------
    # Arithmetic
    # ------------------------------------------------------------------
    def __add__(self, other):
        other = self._convert(other)
        if other is None:
            return NotImplemented
        return Fraction(self.numerator * other.denominator + other.numerator * self.denominator,
                        self.denominator * other.denominator)

    def __radd__(self, other):          # e.g. 1 + Fraction(1, 2)
        return self.__add__(other)

    def __sub__(self, other):
        other = self._convert(other)
        if other is None:
            return NotImplemented
        return Fraction(self.numerator * other.denominator - other.numerator * self.denominator,
                        self.denominator * other.denominator)

    def __rsub__(self, other):          # e.g. 1 - Fraction(1, 2)
        other = self._convert(other)
        if other is None:
            return NotImplemented
        return other.__sub__(self)

    def __mul__(self, other):
        other = self._convert(other)
        if other is None:
            return NotImplemented
        return Fraction(self.numerator * other.numerator,
                        self.denominator * other.denominator)

    def __rmul__(self, other):          # e.g. 2 * Fraction(1, 3)
        return self.__mul__(other)

    def __truediv__(self, other):
        other = self._convert(other)
        if other is None:
            return NotImplemented
        if other.numerator == 0:
            raise ZeroDivisionError("division by a zero fraction")
        num = self.numerator * other.denominator
        den = self.denominator * other.numerator
        # Move a negative sign from the denominator up to the numerator
        if den < 0:
            num, den = -num, -den
        return Fraction(num, den)

    def __neg__(self):
        return Fraction(-self.numerator, self.denominator)

    def __abs__(self):
        return Fraction(abs(self.numerator), self.denominator)

    # ------------------------------------------------------------------
    # Conversions and string representations
    # ------------------------------------------------------------------
    def __float__(self):
        return self.numerator / self.denominator

    def __repr__(self):
        return f"Fraction({self.numerator}, {self.denominator})"

    def __str__(self):
        if self.denominator == 1:
            return str(self.numerator)
        return f"{self.numerator}/{self.denominator}"
