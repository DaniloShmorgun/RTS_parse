from RSG.parsers.main_parser import ResultWriter
from RSG.proxies.rotate_proxy import ProxyRotate 

import os

class SteamParser:

    def save_steam_ids_names_json_file() -> None:
        header, proxy = ProxyRotate.prepare_header_proxy()
        url = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=STEAMKEY&format=json"
        ResultWriter.save_page(url, proxy, header, 'steam_ids.json')

    @staticmethod   
    def get_steam_game_id_by_game_names(steam_id_json_file : str, game_names : list[str]) -> list[str]:
        data = ResultWriter.read_json_from_file(steam_id_json_file)
        apps = data['applist']['apps']

        steam_ids = [] 
        for app in apps:
            if app['name'].strip() in game_names:
                steam_ids.append(app['appid'])
        
        return steam_ids
    
    @staticmethod
    def get_detailed_steam_games_data(ids):
        main_url = "https://store.steampowered.com/api/appdetails?appids="
        header, proxy = ProxyRotate.prepare_header_proxy()

        for id in ids:
            url = main_url + str(id)
            print(id)
            ResultWriter.save_page(url, proxy, header, os.path.join(ResultWriter.prj_root,'saved_jsons', f'game_{str(id)}.json'))

