import pytest
from requests_mock import Mocker
from ..app.retriever import DataRetriever, NoPaginationSetError


class TestRetriever:

    def test_get_paginated_data_with_request_information(self, subtests):

        with Mocker() as m:
            m: Mocker
            test_url = "https://data.montreal.ca/api/3/action/datastore_search?resource_id=6173de60-c2da-4d63-bc75-0607cb8dcb74&limit=1000"
            params = {"resource_id": "6173de60-c2da-4d63-bc75-0607cb8dcb74", "offset": "1000"}
            test_url_next = f"{test_url}&offset={params['offset']}"
            response_json_next = {"result": {"_links": {"next": test_url_next}, "records": ["doesn't matter"]}}
            response_json_final = {"result": {"_links": {"next": test_url_next}, "records": []}}
            responses = [{"json": response_json_next}, {"json": response_json_final}]
            m.get(test_url, json=response_json_next)
            m.get(test_url_next, json=response_json_final)
            retriever = DataRetriever(test_url, pagination_key="next")

            results = retriever.retrieve_information()
            final_page_num = 0

            for page_num, response in enumerate(results):
                with subtests.test(subtest=page_num):
                    assert response.json() == responses[page_num]["json"]
                    final_page_num += 1
            assert final_page_num == 2

    def test_raise_pagination_error_when_pagination_key_not_set(self):
        with Mocker() as m:
            m: Mocker
            test_url = "http://andnothingelsematters"
            test_url_next = "http://andnothingelsematters2"
            response_json_next = {"result": {"_links": {"next": test_url_next}}}
            m.get(test_url, json=response_json_next)

            retriever = DataRetriever(test_url)

            with pytest.raises(NoPaginationSetError):
                for _ in retriever.retrieve_information():
                    continue
