"""

"""

import os.path as osp

from icecream import ic

from flask import request, render_template
from functools import wraps

from typing import Callable, Any

from pathlib import Path
import sys
path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))
from searchEngine.search_interface import API_Query, load_data, relevant_user_tweets


DIR_PATH = osp.dirname(osp.realpath(__file__))

endpoints: dict[tuple[str, str], Callable[[], Any]] = {}

API_DF, API_INDEX, API_VS = load_data()

def register_endpoint(endpoint: str, request_type: str = 'GET') -> Callable:
    def _register_endpoint(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs) -> Any:
            return fn(*args, **kwargs)
        assert endpoint not in endpoints
        endpoints[endpoint, request_type.upper()] = wrapper
        return wrapper
    return _register_endpoint


@register_endpoint('/')
def home():
    return render_template('index.html')

@register_endpoint("/updated_query", "post")
def updated_query():
    content = request.json
    query: str = content['query']
    relevant_tweets = content["relevant_tweets"]
    irrelevant_tweets = content["irrelevant_tweets"]
    alpha = content["alpha"]
    beta = content["beta"]
    gamma = content["gamma"]
    query_v, _ = API_Query(query, API_DF, API_INDEX, API_VS)
    results: list = relevant_user_tweets(relevant_tweets, irrelevant_tweets, query_v, query, API_DF, API_INDEX, API_VS, alpha, beta, gamma)
    return {'ranked_results': results}


@register_endpoint('/query', 'post')
def query():
    content = request.json
    query: str = content['query']
    _, rel_tweets = API_Query(query, API_DF, API_INDEX, API_VS)
    return {'ranked_results': rel_tweets}
