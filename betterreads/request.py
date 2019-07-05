import requests
import xmltodict
import json
import os


class GoodreadsRequestException(Exception):
    def __init__(self, error_msg, url):
        self.error_msg = error_msg
        self.url = url

    def __str__(self):
        return self.url, ":", self.error_msg


class GoodreadsRequest:
    def __init__(self, client, path, query_dict, req_format="xml"):
        """Initialize request object."""
        self.params = query_dict
        self.params.update(client.query_dict)
        self.host = client.base_url
        self.path = path
        self.req_format = req_format

    def request(self):
        http_proxy = os.getenv('http_proxy')
        https_proxy = os.getenv('https_proxy')
        proxies =dict(http=http_proxy,https=https_proxy)
        resp = requests.get(self.host + self.path, params=self.params, proxies=proxies)
        if resp.status_code != 200:
            raise GoodreadsRequestException(resp.reason, self.path)
        if self.req_format == "xml":
            data_dict = xmltodict.parse(resp.content, dict_constructor=dict)
            return data_dict["GoodreadsResponse"]
        elif self.req_format == "json":
            return json.loads(resp.content)
        else:
            raise Exception("Invalid format")
