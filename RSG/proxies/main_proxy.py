from RSG.proxies.process_proxy import (
    ProxySession,
    ProcessProxyFiles
)

from RSG.file_processing.file_process import FilesFunctions
from ballyregan.models import Protocols, Anonymities

from os import path

def look_for_proxies(filename: str, protocols : list[Protocols], anonymities : list[Anonymities], chunk_size, n_of_iterations):
    root_dir = FilesFunctions.get_project_root()
    proxy_dir = path.join(root_dir, 'RSG', 'proxy_files')

    file = path.join(proxy_dir, filename) 
    proxy_https_session = ProxySession(protocols, anonymities, file, chunk_size)
    while n_of_iterations:
        print(n_of_iterations)
        n_of_iterations -= 1
        proxy_https_session.search_and_write_proxy_in_file(proxy_https_session)
        ProcessProxyFiles.make_file_unique(proxy_https_session.filename)

if __name__ == '__main__':
    anonymities = [Anonymities.ELITE, Anonymities.ANONYMOUS, Anonymities.TRANSPARENT, Anonymities.UNKNOWN]
    protocols = [Protocols.HTTPS]
    filename = "tested_https_proxies.txt"
    look_for_proxies(filename, protocols, anonymities, 100, 50)