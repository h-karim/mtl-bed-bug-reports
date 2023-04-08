import requests


class DataRetriever:

    def __init__(self, base_url: str, query_params: str | None = None, pagination_key: str | None = None) -> None:
        self.BASE_URL = base_url
        self.QUERY_PARAMS = query_params
        self.pagination_key = pagination_key

    def request_information(self):
        response = requests.get(self.BASE_URL, params=self.QUERY_PARAMS)
        response.raise_for_status()
        yield response

        if not self.pagination_key:
            raise NoPaginationSetError

        next_page_link = response.json().get("_links", {}).get(self.pagination_key)
        while next_page_link:
            response = requests.get(next_page_link)
            response.raise_for_status()
            next_page_link = response.json().get("_links", {}).get(self.pagination_key)
            yield response


class NoPaginationSetError(Exception):

    def __init__(self, *args):
        super().__init__(args)

    def __str__(self):
        return "Pagination requested without pagination key being set"


# TODO: change return to yield and use requests.Session() for pagination
#   response['_links']['next'] has the prepared full url for the next get request
