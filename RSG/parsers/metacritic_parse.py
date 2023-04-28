from bs4 import BeautifulSoup
import json
import os

from itertools import chain

from RSG.proxies.process_proxy import(
    ProcessProxyFiles,
    Protocols
)

from RSG.file_processing.file_process import FilesFunctions
from RSG.proxies.rotate_proxy import ProxyRotate

from typing import Tuple, Dict

class MetacriticMainParser:

    root_dir = FilesFunctions.get_project_root()
    
    metacritic_games_dir = os.path.join(root_dir, 'saved_html', 'metacritic_game_pages')
    metacritic_top_games_dir = os.path.join(root_dir, 'saved_html', 'metacritic_top_pages')

    metacritic_root_url = 'http://www.metacritic.com/'
    
    # Finds game urls, from saved html file of TOP games
    @classmethod
    def find_game_urls(cls, filename) -> list[str]:
        with open(filename, 'r', encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, 'html.parser')
        game_tags = soup.body.find_all('a', class_='title')

        urls = []
        for tag in game_tags:
            urls.append(cls.metacritic_root_url + tag.get('href'))
        return urls
    
    @classmethod
    def get_games_info_from_metacritic(cls, urls) -> list[Dict[str, str]]:
        games = []
        
        for i in range(len(urls)):
            res = MetaCriticScraper(os.path.join(cls.metacritic_games_dir, f'game{i}.html'), urls[i])
            games.append(res.game)
        
        return games
    
    @staticmethod
    def get_n_metacritic_game_urls(pages, num) -> list:
        game_urls = [MetacriticMainParser.find_game_urls(page) for page in pages]
        game_urls = list(chain(*game_urls))
        game_urls = game_urls[0:num]
        return game_urls
    
    @classmethod
    def save_n_metacritic_TOP_RTS_game_pages(cls,url, num) -> None:
        header, proxy = ProxyRotate.prepare_header_proxy()
        url = "https://www.metacritic.com/browse/games/genre/metascore/real-time?page="
        for i in range(0, num):
            parsed_page = ResultWriter.save_page(url + str(i), proxy, header, os.path.join(cls.metacritic_top_games_dir, f'index{i}.html'))

    @classmethod
    def get_n_metacritic_game_pages(cls, num) -> list[str]:
        save_pages = []
        for i in range(0, num):
            save_pages.append(os.path.join(cls.metacritic_top_games_dir, f'index{i}.html'))
        return save_pages

class MetaCriticScraper:
    def __init__(self, filename, url):
        self.game = {
                    'url': '',
					 'image': '',
					 'title': '',
					 'description': '',
					 'platform': '',
					 'publisher': '',
					 'release_date': '',
					 'critic_score': '',
					 'critic_outof': '',
					 'critic_count': '',
					 'user_score': '',
					 'user_count': '',
					 'developer': '',
					 'genre': '',
					 'rating': '',
					}
		
        with open(filename, 'r', encoding="utf-8") as file:
            html = file.read()

        self.game['url'] = url
        self.soup = BeautifulSoup(html,'html.parser')
        self.scrape()

	
    def scrape(self):
        try:
            product_title_div = self.soup.find("div", class_="product_title")
            self.game['title'] = product_title_div.a.text.strip()
        except:
            print("WARNING: Problem getting title and platform information")
            pass
			
        try:
            self.game['publisher'] = self.soup.find("li", class_="summary_detail publisher").a.text.strip()
            self.game['release_date'] = self.soup.find("li", class_="summary_detail release_data").find("span", class_="data").text.strip()

        except:
            print("WARNING: Problem getting publisher and release date information")
            pass
			
        try:
            res = self.soup.find("script",type="application/ld+json")
            js = json.loads(res.string)
            self.game['image'] = js['image']
            self.game['platform'] = js['gamePlatform']
            self.game['description'] = js['description']
            self.game['critic_score'] = js['aggregateRating']['ratingValue']
            self.game['critic_count'] = js['aggregateRating']['ratingCount']

            self.game['genre'] = '|'.join(set(js['genre']))
        except Exception as e:
            print(e)
            print("WARNING: Problem getting critic score information")
            pass
            
        # Get user information
        try:
            users = self.soup.find("div", class_="details side_details")
            self.game['user_score'] = users.find("div", class_="metascore_w").text.strip()
            raw_users_count = users.find("span", class_="count").a.text
            user_count = ''
            for c in raw_users_count:
                if c.isdigit(): user_count += c
            self.game['user_count'] = user_count.strip()
        except:
            print("WARNING: Problem getting user score information")
            pass
                
        # Get remaining information
        try:
            product_info = self.soup.find("div", class_="section product_details").find("div", class_="details side_details")
            self.game['developer'] = product_info.find("li", class_="summary_detail developer").find("span", class_="data").text.strip()
            # self.game['genre'] = product_info.find("li", class_="summary_detail product_genre").find("span", class_="data").text.strip()
            self.game['rating'] = product_info.find("li", class_="summary_detail product_rating").find("span", class_="data").text.strip()
        
        except:
            print("WARNING: Problem getting miscellaneous game information")
            pass
        
