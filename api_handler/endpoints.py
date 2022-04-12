"""

"""

import os.path as osp

from icecream import ic

from flask import request, render_template
from functools import wraps
import random

from typing import Callable, Any


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
    terms = query.split()
    # TODO make actual call for usefult data here
    results = ' '.join(terms) if random.choice((True, False)) else ' '.join(reversed(terms))
    return {'ranked_results': results}
