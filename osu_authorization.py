import os
import signal
import json
from time import time
from typing import Dict, List, Literal, Union
import webbrowser
from flask import Flask, request
from threading import Thread
from multiprocessing import Process
import requests

TokenKeys = Literal['token_type', 'expires_in',
                    'access_token', 'refresh_token', 'request_time']
OauthToken = Dict[TokenKeys, Union[str, int]]


class OauthClientConfig:
    code_file: str
    client_id: int
    client_secret: str
    redirect_port: int
    redirect_path: str
    scopes: List[str]

    def __init__(self, cfg_file: str):
        with open(cfg_file) as f:
            c = json.loads(f.read())
            self.code_file = c['code_file']
            self.client_id = c['client_id']
            self.client_secret = c['client_secret']
            self.redirect_port = c['redirect_port']
            self.redirect_path = c['redirect_path']
            self.scopes = c['scopes']


cfg = OauthClientConfig('config.json')


def redirect_uri():
    return f'http://localhost:{cfg.redirect_port}{cfg.redirect_path}'


def authorize_uri():
    return f'https://osu.ppy.sh/oauth/authorize?client_id={cfg.client_id}&redirect_uri={redirect_uri()}&response_type=code&scope={r"%20".join(cfg.scopes)}'


def open_authorize():
    webbrowser.open(authorize_uri())


def run_app():
    app = Flask(__name__)

    def shutdown_app(delay: int):
        import time
        time.sleep(delay)
        os.kill(os.getpid(), signal.SIGINT)

    def save_code(code: str):
        with open(cfg.code_file, 'w', encoding='utf-8') as f:
            f.write(code)

    @app.route(cfg.redirect_path)
    def callback():
        if (code := request.args.get('code')) is None:
            print('Could not get authorize code')
            os.kill(os.getpid(), signal.SIGINT)

        save_code(code)
        Thread(target=shutdown_app, args=(1,)).start()
        return 'success authorization, please close this page'

    app.run(port=cfg.redirect_port, debug=False, use_reloader=False)


def get_authorization_code() -> str:
    get_authorization_code_by_oauth()
    return try_get_authorization_code()


def try_get_authorization_code(refresh=False) -> str:
    if not refresh and os.path.isfile(cfg.code_file):
        with open(cfg.code_file) as f:
            if len(code := f.read()) > 10:
                return code

    return get_authorization_code()


def get_authorization_code_by_oauth():
    app_process = Process(target=run_app)
    app_process.start()
    open_authorize()
    app_process.join()


def get_authorization_token(code: str) -> OauthToken:
    print('requesting auth token..')
    token: OauthToken = requests.post('https://osu.ppy.sh/oauth/token', headers={
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }, json={
        'client_id': cfg.client_id,
        'client_secret': cfg.client_secret,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri()
    }).json()

    if token.get('hint') in ['Authorization code has expired', 'Authorization code has been revoked']:
        print('refreshing authorization token...')
        return get_authorization_token(try_get_authorization_code(refresh=True))

    if token.get('error') is not None:
        print('fatal: ', token)
        raise Exception('Failed to get authorization token')

    os.remove(cfg.code_file)
    token['request_time'] = int(time())
    with open('osu_token.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(token, indent=4))
    return token


def try_get_authorization_token(refresh=False) -> OauthToken:
    if refresh:
        return get_authorization_token(try_get_authorization_code(refresh=True))

    if os.path.isfile('osu_token.json'):
        with open('osu_token.json') as f:
            token: OauthToken = json.loads(f.read())
            if int(time()) - token['expires_in'] <= token['request_time']:
                return token

    return get_authorization_token(try_get_authorization_code())


if __name__ == '__main__':
    token = try_get_authorization_token()
    print(token)
