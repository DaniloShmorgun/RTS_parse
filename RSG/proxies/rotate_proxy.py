from ballyregan.models import Protocols, Anonymities

from RSG.proxies.process_proxy import ProcessProxyFiles
from RSG.file_processing.file_process import FilesFunctions

from fake_useragent import UserAgent

from typing import Dict
import random
import os


class ProxyRotate:

    @staticmethod
    def pick_proxy() -> None:
        root_dir = FilesFunctions.get_project_root()
        proxy_dir = os.path.join(root_dir, 'RSG', 'proxy_files')
        
        valid_http_proxy = os.path.join(proxy_dir, "tested_http_proxies.txt")
        valid_https_proxy = os.path.join(proxy_dir, "tested_https_proxies.txt")

        used_http_proxy = os.path.join(proxy_dir, "used_http_proxies.txt")
        used_https_proxy = os.path.join(proxy_dir, "used_https_proxies.txt")

        peek_http = ProcessProxyFiles.proxies_not_in_second_file(used_http_proxy, valid_http_proxy)
        peek_https = ProcessProxyFiles.proxies_not_in_second_file(used_https_proxy, valid_https_proxy)
        
        if peek_https and peek_http:
            http_proxy =  random.choice(peek_http)
            https_proxy =  random.choice(peek_https)

            ProcessProxyFiles.add_proxie_to_file(used_http_proxy, http_proxy)
            ProcessProxyFiles.add_proxie_to_file(used_https_proxy, https_proxy)

            if not(ProcessProxyFiles.is_proxy_files_same(used_http_proxy, valid_http_proxy)):
                FilesFunctions.clear_file(used_http_proxy)

            if not(ProcessProxyFiles.is_proxy_files_same(used_https_proxy, valid_https_proxy)):
                FilesFunctions.clear_file(used_https_proxy)
            
            proxy = {
                "http" : http_proxy,
                "https" : https_proxy
            }
            return proxy
        return

    @staticmethod
    def prepare_header_proxy() -> tuple[Dict, str]:
        header = {"User-Agent" : str(UserAgent.random)}

        new = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",

            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6",
            'Connection': 'keep-alive',
        }

        header.update(new)
        proxy = ProxyRotate.pick_proxy()

        return header, proxy