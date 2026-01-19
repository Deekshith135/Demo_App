# backend/sideview/aggregator.py
"""
Health Aggregation Utilities for Sideview
Provides aggregation functions for health status from multiple observations
"""

import logging
from typing import List, Dict, Any
from collections import Counter

logger = logging.getLogger(__name__)


def aggregate_health_robust(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Aggregate health status from multiple observations using robust voting.
    
    Args:
        data: List of observation dictionaries with 'status' or 'health' fields
        
    Returns:
        Dictionary with aggregated status and confidence
    """
    if not data:
        return {
            "status": "unknown",
            "confidence": 0.0,
            "total_observations": 0
        }
    
    # Extract statuses from data
    statuses = []
    confidences = []
    
    for item in data:
        # Try to get status from different possible fields
        status = item.get('status') or item.get('health') or item.get('prediction', {}).get('status')
        
        if status:
            # Handle nested status dictionaries
            if isinstance(status, dict):
                status_val = status.get('prediction') or status.get('status')
                conf = float(status.get('confidence', 0.0))
            else:
                status_val = status
                conf = float(item.get('confidence', 0.5))
            
            if status_val:
                statuses.append(str(status_val).lower())
                confidences.append(conf)
    
    if not statuses:
        return {
            "status": "unknown",
            "confidence": 0.0,
            "total_observations": len(data)
        }
    
    # Count occurrences and calculate weighted confidence
    status_counter = Counter(statuses)
    most_common_status, count = status_counter.most_common(1)[0]
    
    # Calculate average confidence for the most common status
    status_confidences = [
        conf for status, conf in zip(statuses, confidences)
        if status == most_common_status
    ]
    avg_confidence = sum(status_confidences) / len(status_confidences) if status_confidences else 0.0
    
    # Adjust confidence by consensus (higher consensus = higher confidence)
    consensus_factor = count / len(statuses)
    final_confidence = avg_confidence * (0.7 + 0.3 * consensus_factor)
    
    return {
        "status": most_common_status,
        "confidence": round(final_confidence, 3),
        "total_observations": len(data),
        "consensus": round(consensus_factor, 3),
        "status_distribution": dict(status_counter)
    }


def aggregate_by_part(data: List[Dict[str, Any]], part: str) -> Dict[str, Any]:
    """
    Aggregate health status for a specific tree part.
    
    Args:
        data: List of observation dictionaries
        part: Part name (e.g., 'stem', 'bud', 'leaves')
        
    Returns:
        Aggregated results for the specified part
    """
    # Filter data for the specific part
    part_data = [
        item for item in data
        if (item.get('part') or item.get('part_name', '')).lower() == part.lower()
    ]
    
    if not part_data:
        return {
            "part": part,
            "status": "no_data",
            "confidence": 0.0,
            "observations": 0
        }
    
    agg_result = aggregate_health_robust(part_data)
    agg_result['part'] = part
    agg_result['observations'] = len(part_data)
    
    return agg_result


def aggregate_tree_health(tree_data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    """
    Aggregate overall tree health from multiple parts.
    
    Args:
        tree_data: Dictionary mapping part names to lists of observations
        
    Returns:
        Overall tree health assessment
    """
    part_results = {}
    all_statuses = []
    
    for part, observations in tree_data.items():
        part_agg = aggregate_by_part(observations, part)
        part_results[part] = part_agg
        
        if part_agg['status'] not in ['no_data', 'unknown']:
            all_statuses.append(part_agg['status'])
    
    # Determine overall tree health
    if not all_statuses:
        overall_status = "unknown"
        overall_confidence = 0.0
    else:
        # Priority: critical > unhealthy > healthy
        if any('critical' in s or 'rot' in s or 'bleeding' in s for s in all_statuses):
            overall_status = "critical"
            overall_confidence = 0.8
        elif any('unhealthy' in s for s in all_statuses):
            overall_status = "unhealthy"
            overall_confidence = 0.7
        elif all('healthy' in s for s in all_statuses):
            overall_status = "healthy"
            overall_confidence = 0.9
        else:
            overall_status = "needs_inspection"
            overall_confidence = 0.5
    
    return {
        "overall_status": overall_status,
        "overall_confidence": overall_confidence,
        "parts": part_results,
        "total_parts_assessed": len(part_results)
    }
