"""
test_fraction.py - pytest tests for the Fraction class (Task 2, Deliverable 4)

Run with:  pytest -v test_fraction.py
"""

import pytest

from fraction import Fraction


# ----------------------------------------------------------------------
# Initialisation
# ----------------------------------------------------------------------
class TestInit:
    def test_basic(self):
        f = Fraction(3, 4)
        assert f.numerator == 3
        assert f.denominator == 4

    def test_default_denominator(self):
        f = Fraction(5)
        assert (f.numerator, f.denominator) == (5, 1)

    def test_reduced_to_lowest_terms(self):
        f = Fraction(6, 8)
        assert (f.numerator, f.denominator) == (3, 4)

    def test_negative_numerator(self):
        f = Fraction(-2, 4)
        assert (f.numerator, f.denominator) == (-1, 2)

    def test_zero(self):
        f = Fraction(0, 5)
        assert (f.numerator, f.denominator) == (0, 1)

    @pytest.mark.parametrize("den", [0, -1, -7])
    def test_denominator_not_positive_raises(self, den):
        with pytest.raises(ValueError):
            Fraction(1, den)

    @pytest.mark.parametrize("num, den", [(1.5, 2), (1, 2.0), ("1", 2), (1, None), (True, 2)])
    def test_non_integer_raises(self, num, den):
        with pytest.raises(TypeError):
            Fraction(num, den)

    def test_read_only(self):
        f = Fraction(1, 2)
        with pytest.raises(AttributeError):
            f.numerator = 5
        with pytest.raises(AttributeError):
            f.denominator = 5


# ----------------------------------------------------------------------
# Comparisons
# ----------------------------------------------------------------------
class TestComparisons:
    def test_eq(self):
        assert Fraction(1, 2) == Fraction(2, 4)
        assert Fraction(2, 1) == 2
        assert not (Fraction(1, 2) == Fraction(1, 3))

    def test_ne(self):
        assert Fraction(1, 2) != Fraction(1, 3)
        assert not (Fraction(1, 2) != Fraction(3, 6))

    def test_lt(self):
        assert Fraction(1, 3) < Fraction(1, 2)
        assert Fraction(-1, 2) < Fraction(1, 3)
        assert not (Fraction(1, 2) < Fraction(1, 2))

    def test_le(self):
        assert Fraction(1, 3) <= Fraction(1, 2)
        assert Fraction(1, 2) <= Fraction(2, 4)
        assert not (Fraction(2, 3) <= Fraction(1, 2))

    def test_gt(self):
        assert Fraction(3, 4) > Fraction(2, 3)
        assert Fraction(3, 2) > 1
        assert not (Fraction(1, 2) > Fraction(1, 2))

    def test_ge(self):
        assert Fraction(3, 4) >= Fraction(2, 3)
        assert Fraction(1, 2) >= Fraction(2, 4)
        assert not (Fraction(1, 3) >= Fraction(1, 2))

    def test_compare_with_non_fraction(self):
        # __eq__ returns NotImplemented, so Python falls back to False
        assert (Fraction(1, 2) == "1/2") is False
        assert (Fraction(1, 2) != "1/2") is True
        assert Fraction(1, 2).__eq__("1/2") is NotImplemented
        assert Fraction(1, 2).__lt__(0.5) is NotImplemented
        # Ordering with an unsupported type raises TypeError
        with pytest.raises(TypeError):
            Fraction(1, 2) < "a"

    def test_hash_consistent_with_eq(self):
        assert hash(Fraction(1, 2)) == hash(Fraction(2, 4))
        assert len({Fraction(1, 2), Fraction(2, 4), Fraction(3, 6)}) == 1


# ----------------------------------------------------------------------
# Arithmetic
# ----------------------------------------------------------------------
class TestArithmetic:
    def test_add(self):
        assert Fraction(1, 2) + Fraction(1, 3) == Fraction(5, 6)
        assert Fraction(1, 2) + 1 == Fraction(3, 2)
        assert 1 + Fraction(1, 2) == Fraction(3, 2)

    def test_sub(self):
        assert Fraction(1, 2) - Fraction(1, 3) == Fraction(1, 6)
        assert Fraction(1, 3) - Fraction(1, 2) == Fraction(-1, 6)
        assert 1 - Fraction(1, 4) == Fraction(3, 4)

    def test_mul(self):
        assert Fraction(2, 3) * Fraction(3, 4) == Fraction(1, 2)
        assert Fraction(1, 3) * 3 == 1
        assert 2 * Fraction(1, 4) == Fraction(1, 2)

    def test_truediv(self):
        assert Fraction(1, 2) / Fraction(1, 4) == 2
        assert Fraction(1, 2) / Fraction(-1, 4) == Fraction(-2, 1)
        assert Fraction(3, 4) / 3 == Fraction(1, 4)

    def test_div_result_has_positive_denominator(self):
        result = Fraction(1, 2) / Fraction(-3, 5)
        assert result.denominator > 0
        assert result == Fraction(-5, 6)

    def test_div_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            Fraction(1, 2) / Fraction(0, 1)

    def test_neg_and_abs(self):
        assert -Fraction(1, 2) == Fraction(-1, 2)
        assert abs(Fraction(-3, 4)) == Fraction(3, 4)

    def test_unsupported_operand(self):
        with pytest.raises(TypeError):
            Fraction(1, 2) + "a"


# ----------------------------------------------------------------------
# Conversions and formatting
# ----------------------------------------------------------------------
class TestFormatting:
    def test_float(self):
        assert float(Fraction(1, 4)) == pytest.approx(0.25)
        assert float(Fraction(-1, 3)) == pytest.approx(-0.333333333)

    def test_repr(self):
        assert repr(Fraction(2, 4)) == "Fraction(1, 2)"

    def test_str(self):
        assert str(Fraction(3, 4)) == "3/4"
        assert str(Fraction(-3, 4)) == "-3/4"
        assert str(Fraction(4, 2)) == "2"
