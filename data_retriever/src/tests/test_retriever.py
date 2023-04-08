import requests_mock  # noqa
from ..app.retriever import Retriever


class TestRetriever:

    def test_get_paginated_data_with_request_information(self, requests_mock):  # noqa
        test_url = "http://andnothingelsematters"
        test_url_next = "http://andnothingelsematters2"
        response_json_next = {"_links": {"next": test_url_next}}
        response_json_final = {}
        responses = [response_json_next, response_json_final]
        requests_mock.get(test_url, json=response_json_next)
        requests_mock.get(test_url_next, json=response_json_final)
        retriever = Retriever(test_url)
        for i, response in enumerate(retriever.request_information()):
            assert response.json() == responses[i]
