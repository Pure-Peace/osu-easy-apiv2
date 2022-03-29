from typing import Dict, Literal, Optional
import requests
from osu_authorization import try_get_authorization_token


RequestType = Literal['get', 'post', 'head',
                      'options', 'put', 'patch', 'delete']


JSON_REQ_HEADER = {'Content-Type: application/json',
                   'Accept: application/json'}


class OsuApi:
    uri: str
    json_data: Optional[Dict] = None
    auth_header: Optional[Dict] = None

    def __init__(self, uri: str) -> None:
        self.uri = uri
        self.auth_header = {
            'Authorization': f'Bearer {try_get_authorization_token()["access_token"]}'}

    def send(self, request_type: RequestType = 'get') -> Dict:
        headers = self.auth_header
        if request_type == 'post':
            headers |= JSON_REQ_HEADER
        return requests.request(request_type, f'https://osu.ppy.sh/api/v2/{self.uri}', headers=headers, json=self.json_data).json()

    def get(self) -> Dict:
        self.send(request_type='get')

    def post(self) -> Dict:
        self.send(request_type='post')

    def add_queries(self, params: Dict, *queries) -> 'OsuApi':
        for q in queries:
            if params.get(q) is None:
                continue
            if '?' not in self.uri:
                self.uri += '?'
            if not self.uri.endswith(('&', '?',)):
                self.uri += f'&'
            if q == 'cursor':
                self.uri += params[q]
            else:
                self.uri += f'{q}={params[q]}'
        return self

    def add_json(self, params: Dict, *fields) -> 'OsuApi':
        json_data = {k: params.get(k) for k in fields}
        if self.json_data is None:
            self.json_data = json_data
        else:
            self.json_data |= json_data

        return self
