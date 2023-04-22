from pprint import pprint
from retriever import DataRetriever
from constants import BASE_URL, QUERY_PARAMETERS, PAGINATION_KEY

if __name__ == "__main__":
    data_retriever = DataRetriever(BASE_URL, query_params=QUERY_PARAMETERS, pagination_key=PAGINATION_KEY)

    for data in data_retriever.request_information():
        a = data
        pprint(data.json()["result"]["_links"]["next"])

    print(a.json()["result"]["records"])
