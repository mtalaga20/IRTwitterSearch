"""

"""

from bisect import bisect_left
import numpy as np
from icecream import ic


def find_nearest(container: list[int], target: int) -> int:
    """
    Assumes container is sorted, returns value in container that is closest to target.
    Return the smallest number if two entries are equidistant
    """
    pos = bisect_left(container, target)
    if pos == 0: return container[0]
    if pos == len(container): return container[-1]
    pre = container[pos - 1]
    post = container[pos]
    return post if post - target < target - pre else pre


def get_indices(index: dict, token: str, target_doc_id: str) -> list[str]:
    for doc_id, _, indices in index[token][1]:
        if doc_id == target_doc_id:
            return indices
    return []

def make_proximity_score_vector(
        index: dict,
        sorted_query_tokens: list[str],
        candidate_doc_ids: list[str]
    ) -> np.ndarray:
    vector = np.zeros(len(candidate_doc_ids))
    if len(sorted_query_tokens) == 1: return vector
    # TODO try to compute qt_count without going thru loops
    for i, doc_id in enumerate(candidate_doc_ids):
        total_dist = 0
        comparisons = 0
        qt_count = 0
        evaluated = set()
        for qt in sorted_query_tokens:
            if (qt_locs := get_indices(index, qt, doc_id)): qt_count += 1
            else: continue
            remaining = set(sorted_query_tokens) - {qt} - evaluated
            for compare_qt in remaining:
                if not (compare_qt_locs := get_indices(index, compare_qt, doc_id)): continue
                for qt_loc in qt_locs:
                    total_dist += np.log10(abs(qt_loc - find_nearest(compare_qt_locs, qt_loc)) + 1)  # NOTE cld remove log
                    comparisons += 1
            evaluated.add(qt)
        if qt_count > 1:
            mean_proximity = 1 / (total_dist / comparisons)
            qt_percent_present = qt_count / len(sorted_query_tokens)
            vector[i] = qt_percent_present * mean_proximity
        # else remains 0
    return vector