import requests
import pandas as pd
import csv
import json 
import os

from RSG.file_processing.file_process import FilesFunctions
from RSG.parsers.metacritic_parse import ProxyRotate
from RSG.proxies.main_proxy import ProcessProxyFiles
import sys
import random 

class ResultWriter:
    prj_root = FilesFunctions.get_project_root()
    result_folder = os.path.join(prj_root, 'results') 

    @classmethod
    def save_page(cls, url, proxy, headers, filename) -> None:
        status = 0
        try:
            res = requests.get(url, proxies=proxy, headers=headers, timeout=random.uniform(1, 5)) 
            if res.status_code == requests.codes.ok:
                # Request was successful (status code 200)
                print('Request succeeded')
                status = res.status_code
            
            elif res.status_code == 403:
                # 403 Forbidden response
                print('Access denied')
                res = 0
        
        
        except (requests.HTTPError, requests.RequestException, Exception) as e:
            print(f'An HTTP error occurred: {str(e)}')

            ProcessProxyFiles.delete_proxie_from_file(
                filename=os.path.join(cls.prj_root,'RSG','proxy_files', 'tested_https_proxies.txt'),
                proxy=proxy['https']
            )
            new_headers, new_proxy = ProxyRotate.prepare_header_proxy()
            if new_proxy:
                ResultWriter.save_page(url, new_proxy, new_headers, filename)
            else:
                return
        
        if status:
            src = res.text
            with open(filename, 'w', encoding="utf-8") as file:
                file.write(src)
                return
            
            
        else:
            new_headers, new_proxy = ProxyRotate.prepare_header_proxy()
            
            if new_proxy:
                ResultWriter.save_page(url, new_proxy, new_headers, filename)
            
            else:
                print('NO PROXIES FAGGOT')
                sys.exit()

    
        
    @staticmethod   
    def json_to_csv(json_list, csv_file) -> None:
        fieldnames = list(json_list[0].keys())

        with open(csv_file, 'w', newline='',encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for json_obj in json_list:
                writer.writerow(json_obj)

    @classmethod 
    def csv_to_xlsx(cls, csv_file, xlsx_file) -> None:
        df = pd.read_csv(csv_file)
        writer = pd.ExcelWriter(xlsx_file, engine='xlsxwriter')
        df.to_excel(writer, index=False)
        writer.save()
    
    @staticmethod   
    def read_json_from_file(filename) -> json:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    
    @staticmethod   
    def save_result_in_csv_and_xlsx(games) -> None:
        csv = ResultWriter.json_to_csv(games, 'output.csv')
        ResultWriter.csv_to_xlsx('output.csv', 'output.xlsx')