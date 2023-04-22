from urllib.parse import parse_qs
import requests
from requests import Response


class DataRetriever:

    def __init__(self, base_url: str, query_params: dict[str, str] = {}, pagination_key: str | None = None) -> None:
        self.BASE_URL = base_url
        self.QUERY_PARAMS = query_params
        self.pagination_key = pagination_key
        self._next_params = None

    def _get_request(self, query_params):
        response = requests.get(self.BASE_URL, params=query_params)
        response.raise_for_status()
        return response

    def retrieve_information(self):
        response = self._get_request(self.QUERY_PARAMS)
        yield response
        if not self.pagination_key:
            raise NoPaginationSetError

        records = self._get_response_records(response)
        while records:
            next_page_params = self._extract_parameters_for_next_page(response)
            response = self._get_request(next_page_params)
            records = self._get_response_records(response)
            yield response

    def _extract_parameters_for_next_page(self, response):
        next_page_link = self._get_next_page_link(response)
        offset = self._get_offset_value_from_url(next_page_link)
        next_params = self._prepare_next_request_params(offset)
        return next_params

    def _get_next_page_link(self, response: Response):
        next_page_link = response.json().get("result", {"_links": {}}).get("_links").get(self.pagination_key)
        return next_page_link

    def _prepare_next_request_params(self, offset: str):
        next_params = self.QUERY_PARAMS.copy()
        next_params["offset"] = offset
        return next_params

    def _get_offset_value_from_url(self, url: str):
        offset = parse_qs(url)["offset"][0]
        return offset

    def _get_response_records(self, response: Response):
        records = response.json().get("result", {}).get("records")
        return records


class NoPaginationSetError(Exception):

    def __init__(self, *args):
        super().__init__(args)

    def __str__(self):
        return "Pagination requested without pagination key being set"
