"""
Core mathematical functions for signal processing.

Pure math - no domain interpretation at this layer.
"""

from typing import List, Tuple, Optional
import statistics
from dataclasses import dataclass


@dataclass
class SignalStats:
    """Statistical summary of a signal."""
    
    mean: float
    median: float
    std_dev: float
    min_value: float
    max_value: float
    sample_size: int


def calculate_stats(values: List[float]) -> SignalStats:
    """
    Calculate basic statistics for a signal.
    
    Args:
        values: List of numeric values
        
    Returns:
        Statistical summary
        
    Raises:
        ValueError: If values list is empty
    """
    if not values:
        raise ValueError("Cannot calculate stats for empty list")
    
    return SignalStats(
        mean=statistics.mean(values),
        median=statistics.median(values),
        std_dev=statistics.stdev(values) if len(values) > 1 else 0.0,
        min_value=min(values),
        max_value=max(values),
        sample_size=len(values),
    )


def detect_deviation(
    current_value: float,
    baseline_values: List[float],
    threshold_std_devs: float = 2.0,
) -> Tuple[bool, float]:
    """
    Detect if current value deviates significantly from baseline.
    
    Args:
        current_value: Value to check
        baseline_values: Historical baseline
        threshold_std_devs: Number of standard deviations for significance
        
    Returns:
        Tuple of (is_significant, z_score)
    """
    if len(baseline_values) < 2:
        return False, 0.0
    
    baseline_mean = statistics.mean(baseline_values)
    baseline_std = statistics.stdev(baseline_values)
    
    if baseline_std == 0:
        return current_value != baseline_mean, 0.0
    
    z_score = (current_value - baseline_mean) / baseline_std
    is_significant = abs(z_score) >= threshold_std_devs
    
    return is_significant, z_score


def moving_average(values: List[float], window_size: int) -> List[float]:
    """
    Calculate moving average with specified window.
    
    Args:
        values: Time series values
        window_size: Size of moving window
        
    Returns:
        List of moving averages
    """
    if len(values) < window_size:
        return []
    
    result = []
    for i in range(len(values) - window_size + 1):
        window = values[i:i + window_size]
        result.append(statistics.mean(window))
    
    return result


def detect_trend(values: List[float], min_length: int = 3) -> Optional[str]:
    """
    Detect if values show a consistent trend.
    
    Args:
        values: Time series values
        min_length: Minimum length for trend detection
        
    Returns:
        "increasing", "decreasing", "stable", or None
    """
    if len(values) < min_length:
        return None
    
    # Simple trend detection using differences
    differences = [values[i+1] - values[i] for i in range(len(values) - 1)]
    
    if not differences:
        return "stable"
    
    positive_count = sum(1 for d in differences if d > 0)
    negative_count = sum(1 for d in differences if d < 0)
    
    threshold = len(differences) * 0.7  # 70% threshold
    
    if positive_count >= threshold:
        return "increasing"
    elif negative_count >= threshold:
        return "decreasing"
    else:
        return "stable"


def calculate_percentile(values: List[float], percentile: float) -> float:
    """
    Calculate percentile of values.
    
    Args:
        values: List of values
        percentile: Percentile to calculate (0-100)
        
    Returns:
        Value at percentile
    """
    if not values:
        raise ValueError("Cannot calculate percentile for empty list")
    
    if not 0 <= percentile <= 100:
        raise ValueError("Percentile must be between 0 and 100")
    
    sorted_values = sorted(values)
    index = (percentile / 100) * (len(sorted_values) - 1)
    
    if index.is_integer():
        return sorted_values[int(index)]
    else:
        lower = sorted_values[int(index)]
        upper = sorted_values[int(index) + 1]
        fraction = index - int(index)
        return lower + fraction * (upper - lower)


def normalize_values(values: List[float], target_range: Tuple[float, float] = (0, 1)) -> List[float]:
    """
    Normalize values to target range.
    
    Args:
        values: Values to normalize
        target_range: Desired output range (min, max)
        
    Returns:
        Normalized values
    """
    if not values:
        return []
    
    min_val = min(values)
    max_val = max(values)
    
    if min_val == max_val:
        # All values the same, return midpoint of target range
        midpoint = (target_range[0] + target_range[1]) / 2
        return [midpoint] * len(values)
    
    target_min, target_max = target_range
    target_span = target_max - target_min
    
    normalized = []
    for value in values:
        # Scale to 0-1
        scaled = (value - min_val) / (max_val - min_val)
        # Scale to target range
        result = target_min + scaled * target_span
        normalized.append(result)
    
    return normalized
