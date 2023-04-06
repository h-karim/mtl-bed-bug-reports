# import requests


class Retriever:

    def __init__(self, base_url: str, query_params: str, pagination_key: str) -> None:
        self.BASE_URL = base_url
        self.QUERY_PARAMS = query_params
        self.pagination_key = pagination_key

    def _get(self):
        response = requests.get(self.BASE_URL, params=self.QUERY_PARAMS)
        response.raise_for_status()
        return response.json()