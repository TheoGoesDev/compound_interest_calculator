from decimal import Decimal

import pytest

from main import calculate_compound_interest


def test_simple_compound_interest():
    """Test basic compound interest calculation without monthly additions"""
    result = calculate_compound_interest(
        principal=1000,
        rate=0.05,
        time=1,
        compounds_per_year=1
    )
    assert result == 1050.00

def test_monthly_compound_interest():
    """Test compound interest with monthly compounding"""
    result = calculate_compound_interest(
        principal=1000,
        rate=0.05,
        time=1,
        compounds_per_year=12
    )
    assert result > 1050.00  # Should be slightly higher than annual compounding

def test_monthly_additions():
    """Test compound interest with monthly additions"""
    result = calculate_compound_interest(
        principal=1000,
        rate=0.05,
        time=1,
        compounds_per_year=12,
        monthly_addition=100
    )
    assert result > 1000 + (100 * 12)  # Should be more than principal + additions

def test_zero_principal():
    """Test calculation with zero principal"""
    result = calculate_compound_interest(
        principal=0,
        rate=0.05,
        time=1,
        monthly_addition=100
    )
    assert result > 0  # Should accumulate monthly additions

def test_zero_rate():
    """Test calculation with zero interest rate"""
    result = calculate_compound_interest(
        principal=1000,
        rate=0,
        time=1,
        monthly_addition=100
    )
    assert result == 1000 + (100 * 12)  # Should equal principal + total additions

def test_negative_values():
    """Test that negative values raise ValueError"""
    with pytest.raises(ValueError):
        calculate_compound_interest(
            principal=-1000,
            rate=0.05,
            time=1
        )

def test_edge_cases():
    """Test edge cases with very small and large values"""
    result = calculate_compound_interest(
        principal=0.01,
        rate=0.001,
        time=0.1
    )
    assert result > 0

    result = calculate_compound_interest(
        principal=1_000_000,
        rate=0.20,
        time=30
    )
    assert result > 1_000_000