import requests

import readConfig
from common import optionexcel, zuhecase


class GetResponse(object):
    def download(self,url,proxies,params):
        response = requests.get(url, proxies=proxies, params=params)


        if response.status_code != 200 :
            return None

        print(response.url)
        return response.text

