"""

"""

from bisect import bisect_left
import numpy as np


def find_nearest(container: list[int], target: int) -> int:
    """
    Assumes container is sorted and returns closest value to target.
    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(container, target)
    if pos == 0: return container[0]
    if pos == len(container): return container[-1]
    pre = container[pos - 1]
    post = container[pos]
    return post if post - target < target - pre else pre


def make_proximity_score_vector(index: 'InvertedIndex', sorted_query_tokens: list[str], candidate_doc_names: list[str]):
    vector = np.empty(len(candidate_doc_names))
    for i, doc in enumerate(candidate_doc_names):
        total_dist = 1  # set at one to avoid divide by zero
        comparisons = 1  # set at one to avoid divide by zero
        qt_count = 0
        for qt in sorted_query_tokens:
            if (qt_locs := index[qt]['docs'][doc]['locs']): qt_count += 1
            remaining = set(sorted_query_tokens) - {qt}
            for compare_qt in remaining:
                if not (compare_qt_locs := index[compare_qt]['docs'][doc]['locs']): break
                for qt_loc in qt_locs:
                    total_dist += np.log10(abs(qt_loc - find_nearest(compare_qt_locs, qt_loc)))  # TODO shld add log here?
                    comparisons += 1
        mean_proximity = 1 / (total_dist / comparisons)
        qt_percent_present = qt_count / len(sorted_query_tokens)
        vector[i] = qt_percent_present * mean_proximity

    return vector