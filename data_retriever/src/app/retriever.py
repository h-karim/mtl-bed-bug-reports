from urllib.parse import parse_qs
import requests


class DataRetriever:

    def __init__(self, base_url: str, query_params: dict[str, str] = {}, pagination_key: str | None = None) -> None:
        self.BASE_URL = base_url
        self.QUERY_PARAMS = query_params
        self.pagination_key = pagination_key
        self._next_params = None

    def _foo(self, query_params):
        response = requests.get(self.BASE_URL, params=query_params)
        response.raise_for_status()
        return response

    def request_information(self):
        response = self._foo(self.QUERY_PARAMS)
        yield response
        if not self.pagination_key:
            raise NoPaginationSetError

        records = response.json().get("result", {}).get("records")
        while records:
            next_page_link = response.json().get("result", {"_links": {}}).get("_links").get(self.pagination_key)
            offset = parse_qs(next_page_link)["offset"]
            next_params = self.QUERY_PARAMS.copy()
            next_params["offset"] = offset[0]
            response = self._foo(next_params)
            records = response.json().get("result", {}).get("records")
            yield response


class NoPaginationSetError(Exception):

    def __init__(self, *args):
        super().__init__(args)

    def __str__(self):
        return "Pagination requested without pagination key being set"
