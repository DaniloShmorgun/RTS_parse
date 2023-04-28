from ballyregan import ProxyFetcher
from ballyregan.models import Protocols, Anonymities
from ballyregan.core.exceptions import ProxyException
from typing import Optional, List

import threading
import requests

from fake_useragent import UserAgent

import os

from pydantic import (
    BaseModel,
    validator,
    PositiveInt,
    conlist,
    constr,
)

class MyThread(threading.Thread):
    def __init__(self, target, args=()):
        threading.Thread.__init__(self)
        self.target = target
        self.args = args
        self.result = None

    def run(self):
        self.result = self.target(*self.args)


# Regular expression for proxy
class ProxyStrType(BaseModel):
    proxy_str : constr(regex=r'^(?:(\w+)(?::(\w+))?@)?((?:\d{1,3})(?:\.\d{1,3}){3})(?::(\d{1,5}))?$')

# Constrains for Protocols
class ProtocolCon(BaseModel):
    protocols : conlist(
                Protocols,
                min_items=1, 
                max_items=len(Protocols.__members__),
                unique_items = True
            )
    
    @validator('protocols')
    def check_protocols(cls, v) -> list:
        
        valid_protocols = Protocols.__members__
        
        if not (v in valid_protocols):
             raise ValueError(f'protocol is not a valid protocol')
        
        return v
    
# Constrains for proxy anonymity    
class AnonymityCon(BaseModel):
    anonymity : conlist(
                    Anonymities,
                    min_items=1,
                    max_items=len(Anonymities.__members__),
                    unique_items= True
                )

    
class ProxySession():
    def __init__(
                self, 
                protocols : List[AnonymityCon],
                anonymity : List[ProtocolCon],
                filename : Optional[str] = 'tested_proxy.txt',
                num : Optional[PositiveInt] = 20,
            ) -> None:
        
        self.protocols = protocols
        self.anonymity = anonymity
        self.num = num
        self.filename = filename
    
     
    # Writes setted number of proxies to proxy.txt file
    @staticmethod
    def search_and_write_proxy_in_file(self) -> None:
        
        fetcher = ProxyFetcher(debug=True)
        
        try:
            proxies = fetcher.get(
                limit=self.num,
                protocols= self.protocols,
                anonymities=self.anonymity,
            )
        
        except Exception:
            raise ProxyException

        def check_proxy(proxy):
            
            ua = UserAgent()
            header = {
                'User-Agent' : str(ua.random)
            }

            new = {   
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'TE': 'Trailers',
            }
            
            proxy_json = {}
            
            if proxy.protocol == Protocols.HTTPS:
                proxy.protocol = Protocols.HTTP
                proxy_str = proxy.__str__()
                proxy.protocol = Protocols.HTTPS
            
            else:
                proxy_str = proxy.__str__()

         
            proxy_json = {
                'http' : 'http://138.117.219.108:80',

            }

            proxy_json.update({
                f'{proxy.protocol}' : proxy_str
            })

            print(proxy_json)
            header.update(new)
            
            try:
                response = requests.get('https://ipinfo.io/json', headers=header, proxies=proxy_json, timeout=5)
            
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                return None

              
            if response.status_code == 200:
                print(response.json())
                return proxy_str


        valid_proxies = []
        
        threads = [MyThread(target=check_proxy, args=(proxy,)) for proxy in proxies]

        for thread in threads:
            thread.start()

        # Wait for the threads to finish and collect their results
        for thread in threads:
            thread.join()
            valid_proxies.append(thread.result)

        valid_proxies = [value for value in valid_proxies if value is not None]
        if valid_proxies:
            try:
                append_write = str
                
                if os.path.exists(self.filename):
                    append_write = 'a' # append if already exists
                
                else:
                    append_write = 'w' # make a new file if not
                
                valid_proxies
                with open(self.filename, append_write, encoding='utf-8') as file:
                    valid_proxies[0]
                    for proxy in valid_proxies:
                        print(proxy)
                        file.write(proxy + '\n')
            except PermissionError:
                print("You do not have permission to write to the file.")
            
            except UnicodeEncodeError as e:
                    print(f"Encoding error: {e}")

class ProcessProxyFiles:
    def __init__(
            self,
            raw_filename : Optional[str] = 'tested_proxy.txt',
            tested_filename : Optional[str] = 'tested_proxy.txt',
        ) -> None:
        
        self.raw_filename = raw_filename,
        self.tested_filename = tested_filename

    # Deletes specific proxy in proxy.txt file
    @staticmethod
    def delete_proxie_from_file(filename : str, proxy : ProxyStrType) -> None:
        
        with open(filename, "r") as f:
            lines = f.readlines()
        
        with open(filename, "w") as f:
            for line in lines:
                if line.strip("\n") != proxy:
                    f.write(line)

    @staticmethod
    def add_proxie_to_file(filename : str, proxy : ProxyStrType) -> None:
        if os.path.exists(filename):
            append_write = 'a' # append if already exists
        else:
            append_write = 'w' # make a new file if not
        
        try:
            with open(filename, append_write) as f:
                f.write(proxy + '\n')
            
        except FileNotFoundError:
            print('Error: File not found.')
        
        except PermissionError:
            print("You do not have permission to write to the file.")
      
    
    @staticmethod
    def make_file_unique(filename) -> None:
        unique_proxies = ProcessProxyFiles.get_unique_proxies(filename)
        
        try:
            with open(filename, 'w') as f:
                for proxy in unique_proxies:
                    f.write(proxy + '\n')
        except FileNotFoundError:
            print('Error: File not found.')
        
        except PermissionError:
            print("You do not have permission to write to the file.")

    @staticmethod
    def get_unique_proxies(filename):
        proxy_set = set()
        
        try:
            with open(filename, 'r') as file:
                for line in file:
                    proxy_set.add(line.strip())
        
        except FileNotFoundError:
            print('Error: File not found.')
        
        except PermissionError:
            print("You do not have permission to write to the file.")
        
        return list(proxy_set)
    
    @staticmethod
    def proxies_not_in_second_file(
            first_filename,
            second_filename,
        ) -> list[ProxyStrType]:

        
        first_proxies = ProcessProxyFiles.get_unique_proxies(first_filename)
        second_proxies = ProcessProxyFiles.get_unique_proxies(second_filename)
        
        first_proxies = set(first_proxies)
        second_proxies = set(second_proxies)
        
        res = second_proxies - first_proxies
        return list(res)
    
    @staticmethod
    def is_proxy_files_same(
            first_filename,
            second_filename,
        ) -> bool:
        
        return bool(ProcessProxyFiles.proxies_not_in_second_file(first_filename, second_filename))
    
    # Gets proxies from file, with specific protocol type: "HTTP", "HTTPS", etc.
    @staticmethod
    def get_protocol_proxies(
            filename,
            proxy_protocols : list(Protocols)
        ) -> list[ProxyStrType]:
        
        proxies = ProcessProxyFiles.get_unique_proxies(filename) 
        
        protocol_proxies = []
        for proxy in proxies:
            if (proxy.split(':')[0].strip() in proxy_protocols):
                protocol_proxies.append(proxy)
            else:
                pass

        return protocol_proxies

if __name__ == '__main__':
    pass