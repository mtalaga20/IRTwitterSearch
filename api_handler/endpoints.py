"""

"""

import os.path as osp
import sys; sys.path.append('.')

from icecream import ic

from flask import request, render_template
from functools import wraps

from typing import Callable, Any

from SEARCH_ENGINE_PKG import search


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


@register_endpoint('/query', 'post')
def query():
    content = request.json
    query: str = content['query']
    relevant_doc_ids: list[str] = content['relevant_doc_ids']
    results: list = search(query, relevant_doc_ids)  # return a ranked list of {doc_id, rank, relevant uris}
    return {'ranked_results': results}
