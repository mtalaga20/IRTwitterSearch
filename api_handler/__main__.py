"""

"""

# OS, system, paths
from dotenv import load_dotenv
import os
import os.path as osp, os
DIR_PATH = osp.dirname(osp.realpath(__file__))
import sys; sys.path.append(DIR_PATH)

# interface
import argparse

# debugging
from icecream import ic

# Environment vars

load_dotenv()

# library imports
from flask import Flask

DEPLOY = os.getenv("REACT_APP_DEPLOY")

if (DEPLOY == "false"):
    from flask_cors import CORS

# local imports
from endpoints import endpoints


def make_argparser() -> argparse.ArgumentParser:
    """Defines command line interface."""
    argparser = argparse.ArgumentParser(description='API endpoint server')
    argparser.add_argument('--host', default = 'localhost', help = 'server domain')
    argparser.add_argument('--port', type = int, default = 8000, help = 'server port')
    return argparser


def main():
    argparser = make_argparser()
    args = argparser.parse_args()
    host: str = args.host
    port: int = args.port

    app = Flask(
        __name__,
        # template_folder = osp.join(DIR_PATH, 'test_frontend', 'templates'),
        # static_folder = osp.join(DIR_PATH, 'test_frontend', 'static'),
    )

    # enables JSON with CORS
    if (DEPLOY == "false"):
        CORS(app)
        app.config['CORS_HEADERS'] = 'Content-Type'

    # register routes
    for (endpoint, request_type), callback in endpoints.items():
        app.route(endpoint, methods=(request_type,))(callback)

    app.run(debug = True, host = host, port = port)


if __name__ == '__main__':
    main()
