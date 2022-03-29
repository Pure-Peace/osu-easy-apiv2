from typing import Dict, Literal, Optional
import requests
from osu_authorization import try_get_authorization_token


RequestType = Literal['get', 'post', 'head',
                      'options', 'put', 'patch', 'delete']


ACCESS_TOKEN: str = try_get_authorization_token()['access_token']

AUTH_HEADER = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
JSON_REQ_HEADER = {'Content-Type: application/json',
                   'Accept: application/json'}


class OsuApi:
    uri: str
    json_data: Optional[Dict] = None

    def __init__(self, uri: str) -> None:
        self.uri = uri

    def send(self, request_type: RequestType = 'get') -> Dict:
        headers = AUTH_HEADER
        if request_type == 'post':
            headers |= AUTH_HEADER
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
            if '&' in self.uri and not self.uri.endswith('&'):
                self.uri += f'&'
            self.uri += f'{q}={params[q]}'

        return self

    def add_json(self, params: Dict, *fields) -> 'OsuApi':
        json_data = {k: params.get(k) for k in fields}
        if self.json_data is None:
            self.json_data = json_data
        else:
            self.json_data |= json_data

        return self
