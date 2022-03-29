from typing import Dict
import requests
from osu_authorization import try_get_authorization_token


access_token: str = try_get_authorization_token()['access_token']
request_header = {'Authorization': f'Bearer {access_token}'}


class OsuApi:
    uri: str
    params: Dict

    def __init__(self, uri: str, params: Dict) -> None:
        self.uri = uri
        self.params = params

    def send(self) -> Dict:
        return requests.get(f'https://osu.ppy.sh/api/v2/{self.uri}', headers=request_header).json()

    def add_queries(self, *queries) -> 'OsuApi':
        for q in queries:
            if self.params.get(q) is None:
                continue
            if '?' not in self.uri:
                self.uri += '?'
            if '&' in self.uri and not self.uri.endswith('&'):
                self.uri += f'&'
            self.uri += f'{q}={self.params[q]}'

        return self
