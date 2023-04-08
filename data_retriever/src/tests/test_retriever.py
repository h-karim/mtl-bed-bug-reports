import pytest
import requests_mock  # noqa
from ..app.retriever import DataRetriever, NoPaginationSetError


class TestRetriever:

    def test_get_paginated_data_with_request_information(self):
        with requests_mock.Mocker() as m:
            test_url = "http://andnothingelsematters"
            test_url_next = "andnothingelsematters2"
            response_json_next = {"result": {"_links": {"next": test_url_next}}}
            response_json_final = {}
            responses = [response_json_next, response_json_final]
            m.get(test_url, json=response_json_next)
            m.get(test_url_next, json=response_json_final)
            retriever = DataRetriever(test_url, pagination_key="next")
            for i, response in enumerate(retriever.request_information()):
                assert response.json() == responses[i]

    def test_raise_pagination_error_when_pagination_key_not_set(self):
        with requests_mock.Mocker() as m:
            test_url = "http://andnothingelsematters"
            test_url_next = "http://andnothingelsematters2"
            response_json_next = {"result": {"_links": {"next": test_url_next}}}
            m.get(test_url, json=response_json_next)

            retriever = DataRetriever(test_url)

            with pytest.raises(NoPaginationSetError):
                for _ in retriever.request_information():
                    continue
