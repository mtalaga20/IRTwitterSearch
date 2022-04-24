"""

"""

import os.path as osp
import sys; sys.path.append('.')

from icecream import ic

from flask import request, render_template
from functools import wraps

from typing import Callable, Any

from main import Search, relevant_user_tweets, search


DIR_PATH = osp.dirname(osp.realpath(__file__))

endpoints: dict[tuple[str, str], Callable[[], Any]] = {}

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
    query_vector, cosSim = Search(query)
    results: list = relevant_user_tweets(relevant_tweets, query_vector)
    return {'ranked_results': ic(results)}


@register_endpoint('/query', 'post')
def query():
    content = request.json
    query: str = content['query']
    relevant_doc_ids = None
    results: list = search(query, relevant_doc_ids) 
    return {'ranked_results': ic(results)}
