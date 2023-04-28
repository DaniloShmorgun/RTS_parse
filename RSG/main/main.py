from RSG.parsers.main_parser import ResultWriter
from RSG.parsers.steam_parser import SteamParser
from RSG.parsers.metacritic_parse import MetacriticMainParser

import os
import pandas as pd

from pathlib import Path
import string

if __name__ == "__main__":

    project_root = ResultWriter.prj_root

    jsons_folder = os.path.join(project_root, 'saved_jsons')

    results_folder = os.path.join(project_root, 'results')

    # MetacriticMainParser.save_n_metacritic_TOP_RTS_game_pages(2)
    
    # metacritic_TOP_RTS_pages = MetacriticMainParser.get_n_metacritic_game_pages(2)

    # metacritic_game_urls = MetacriticMainParser.get_n_metacritic_game_urls(metacritic_TOP_RTS_pages, 150)

    # games = MetacriticMainParser.get_games_info_from_metacritic(metacritic_game_urls)
    
    games = pd.read_csv(results_folder + '\output.csv')

    game_names = games['title'].to_list()
    
    # steam_game_names = ResultWriter.read_json_from_file(jsons_folder + '\steam_ids.json')

    steam_game_ids = SteamParser.get_steam_game_id_by_game_names(jsons_folder + '\steam_ids.json', game_names)

    # SteamParser.get_detailed_steam_games_data(steam_game_ids[14:])

    read_steam_game_json = ResultWriter.read_json_from_file(os.path.join(jsons_folder, 'game_6830.json'))


    keys = ["title", "short_description", "website", "price", 'screenshot']
    
    steam_games = []
    for id in steam_game_ids:
        id = str(id)
        read_steam_game_json = ResultWriter.read_json_from_file(os.path.join(jsons_folder, f'game_{id}.json'))
        
        if read_steam_game_json[id]['success'] != True:
            continue
        
        game = read_steam_game_json[id]['data']
        
        res = {}
        res['title'] = game['name']
        res['description'] = game['short_description']
        res['website'] = game['website']
        
        if game['is_free'] == True:
            res['price'] = 0
        else:
            if 'price_overview' in game.keys():
                res['price'] = game['price_overview']['final_formatted']
            else:
                res['price'] = None
        
        if 'screenshots' in game.keys():
            res['screenshot'] = game['screenshots'][0]['path_full']
        else:
            res['screenshot'] = None
        
        steam_games.append(res)

    list_of_df = []
    for game in steam_games:
        new_df = pd.DataFrame([game])
        list_of_df.append(new_df)
        

    res_df = pd.concat(list_of_df, axis=0)
    
    games = games.drop(['description', 'critic_outof', 'url','critic_count', 'user_count'], axis=1)



    res_df = pd.merge(games,res_df , on='title', how='left')

    print(res_df['website'])

    # res_df = res_df[['website', 'screenshot', 'description']]
    # print(res_df)
    # res_df.to_csv('result.csv', index=False)
    # res_df.to_excel('merged_data.xlsx', index=False)

    

    



    