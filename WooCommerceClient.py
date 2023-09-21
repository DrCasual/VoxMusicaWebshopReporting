import json
import requests
import pandas as pd

from requests_oauthlib import OAuth1


class WooCommerceClient:
    def __init__(self, conf_path: str) -> None:
        with open(conf_path, "r") as fo:
            self.__conf = json.loads(fo.read())

    def __get_auth(self) -> OAuth1:
        return OAuth1(self.__conf["WC_API_CLIENT_KEY"], self.__conf["WC_API_CLIENT_SECRET"], signature_type='query')

    def get_object_by_name(self, name: str) -> pd.DataFrame:
        queryoauth = self.__get_auth()

        page = 1
        res = []

        while True:
            r = requests.get(
                f"{self.__conf['WC_API_BASE_URL']}/{name}?per_page=100&page={page}", auth=queryoauth)
            data = json.loads(r.text)
            if not len(data):
                break
            _ = [res.append(x) for x in data]
            page += 1

        return pd.DataFrame(res)


if __name__ == "__main__":
    test = WooCommerceClient("./config.json")
    print(test.get_object_by_name("products"))
