"""
Tests for signal processing math.
"""

import pytest
from teacher_api.signals.core_math import (
    calculate_stats,
    detect_deviation,
    moving_average,
    detect_trend,
    normalize_values,
)


class TestSignalMath:
    """Test signal processing functions."""

    def test_calculate_stats(self):
        """Should calculate correct statistics."""
        values = [1.0, 2.0, 3.0, 4.0, 5.0]
        stats = calculate_stats(values)
        
        assert stats.mean == 3.0
        assert stats.median == 3.0
        assert stats.min_value == 1.0
        assert stats.max_value == 5.0
        assert stats.sample_size == 5

    def test_calculate_stats_empty_list(self):
        """Should raise error for empty list."""
        with pytest.raises(ValueError, match="empty"):
            calculate_stats([])

    def test_detect_deviation_significant(self):
        """Should detect significant deviations."""
        baseline = [10.0, 10.0, 10.0, 10.0, 10.0]
        current = 20.0  # 2+ std devs away
        
        is_sig, z_score = detect_deviation(current, baseline, threshold_std_devs=2.0)
        
        assert is_sig is True
        assert z_score > 2.0

    def test_detect_deviation_not_significant(self):
        """Should not flag minor deviations."""
        baseline = [10.0, 11.0, 9.0, 10.5, 9.5]
        current = 10.2
        
        is_sig, z_score = detect_deviation(current, baseline, threshold_std_devs=2.0)
        
        assert is_sig is False

    def test_moving_average(self):
        """Should calculate moving average correctly."""
        values = [1.0, 2.0, 3.0, 4.0, 5.0]
        ma = moving_average(values, window_size=3)
        
        expected = [2.0, 3.0, 4.0]  # (1+2+3)/3, (2+3+4)/3, (3+4+5)/3
        assert ma == expected

    def test_moving_average_insufficient_data(self):
        """Should return empty for insufficient data."""
        values = [1.0, 2.0]
        ma = moving_average(values, window_size=3)
        
        assert ma == []

    def test_detect_trend_increasing(self):
        """Should detect increasing trends."""
        values = [1.0, 2.0, 3.0, 4.0, 5.0]
        trend = detect_trend(values)
        
        assert trend == "increasing"

    def test_detect_trend_decreasing(self):
        """Should detect decreasing trends."""
        values = [5.0, 4.0, 3.0, 2.0, 1.0]
        trend = detect_trend(values)
        
        assert trend == "decreasing"

    def test_detect_trend_stable(self):
        """Should detect stable patterns."""
        values = [3.0, 2.9, 3.1, 3.0, 2.95]
        trend = detect_trend(values)
        
        assert trend == "stable"

    def test_normalize_values(self):
        """Should normalize to target range."""
        values = [0.0, 50.0, 100.0]
        normalized = normalize_values(values, target_range=(0, 1))
        
        assert normalized[0] == 0.0
        assert normalized[1] == 0.5
        assert normalized[2] == 1.0

    def test_normalize_constant_values(self):
        """Should handle constant values."""
        values = [5.0, 5.0, 5.0]
        normalized = normalize_values(values, target_range=(0, 1))
        
        # Should return midpoint of target range
        assert all(v == 0.5 for v in normalized)
