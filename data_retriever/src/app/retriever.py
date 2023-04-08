from urllib.parse import parse_qs
import requests
import urllib3


class DataRetriever:

    def __init__(self, base_url: str, query_params: dict[str, str] = {}, pagination_key: str | None = None) -> None:
        self.BASE_URL = base_url
        self.QUERY_PARAMS = query_params
        self.pagination_key = pagination_key

    def request_information(self):
        response = requests.get(self.BASE_URL, params=self.QUERY_PARAMS)
        response.raise_for_status()
        yield response

        if not self.pagination_key:
            raise NoPaginationSetError

        next_page_link = response.json().get("result", {"_links": {}}).get("_links").get(self.pagination_key)
        records = response.json().get("result", {}).get("records")
        while records:
            offset = parse_qs(next_page_link)["offset"]
            next_params = self.QUERY_PARAMS.copy()
            next_params["offset"] = offset[0]
            response = requests.get(self.BASE_URL, params=next_params)
            response.raise_for_status()
            next_page_link = response.json().get("result", {"_links": {}}).get("_links").get(self.pagination_key)
            records = response.json().get("result", {}).get("records")
            yield response


class NoPaginationSetError(Exception):

    def __init__(self, *args):
        super().__init__(args)

    def __str__(self):
        return "Pagination requested without pagination key being set"


# TODO: change return to yield and use requests.Session() for pagination
#   response['_links']['next'] has the prepared full url for the next get request
