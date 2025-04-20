from typing import List

def calculate_metrics(predictions: List[List[str]], ground_truth: List[List[str]], k: int = 3):
    """
    Calculate Mean Recall@K and MAP@K
    
    Args:
        predictions: List of lists, where each inner list contains the predicted assessment IDs
        ground_truth: List of lists, where each inner list contains the ground truth assessment IDs
        k: The K value for the metrics
    
    Returns:
        mean_recall_k: Mean Recall@K
        map_k: Mean Average Precision@K
    """
    recalls = []
    aps = []
    
    for pred, truth in zip(predictions, ground_truth):
        # Calculate Recall@K
        if not truth:  # Skip if no ground truth
            continue
        
        # Get top K predictions
        pred_k = pred[:k]
        
        # Calculate recall
        relevant_count = len(set(pred_k).intersection(set(truth)))
        recall = relevant_count / len(truth) if truth else 0
        recalls.append(recall)
        
        # Calculate AP@K
        ap = 0
        relevant_count = 0
        
        for i, p in enumerate(pred_k):
            if p in truth:
                relevant_count += 1
                precision_at_i = relevant_count / (i + 1)
                ap += precision_at_i
        
        if len(truth) > 0:
            ap /= min(k, len(truth))
            aps.append(ap)
    
    # Calculate Mean Recall@K and MAP@K
    mean_recall_k = sum(recalls) / len(recalls) if recalls else 0
    map_k = sum(aps) / len(aps) if aps else 0
    
    return mean_recall_k, map_k