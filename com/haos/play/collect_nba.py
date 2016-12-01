#encoding: utf-8
'''
@author: haos
'''
from bs4 import BeautifulSoup
import urllib2, urllib
import os
import json

app_dir = os.path.dirname((os.path.abspath(__file__)))
static_dir = os.path.join(app_dir, "static")
if not os.path.exists(static_dir):
    os.mkdir(static_dir)

def collect_info():
    host = "http://g.hupu.com"
    url = "http://g.hupu.com/nba/players/"
    data = urllib2.urlopen(url).read()
    soup_data = BeautifulSoup(data)
    team_name_soup = soup_data.find_all("span", {"class":"team_name"})
    team_info = []
    all_teams = []
    for team in team_name_soup:
        team_a = team.find("a")
        href = team_a.get("href")
        team_url = href
        team_name = team_a.get_text()
        all_teams.append(get_team_info(team_url.replace("players", "teams")))
        team_info.append({"team_name":team_name, "url":team_url, "players":get_all_players(team_url)})
    return team_info, all_teams

    
def get_all_players(url):
    player_list = []
    team_soup = BeautifulSoup(urllib2.urlopen(url).read())
    players_right = team_soup.find("table", {"class":"players_table"}).find_all("tr")
    ignore = True
    for player in players_right:
        if ignore:
            ignore = False
            continue
        td_padding = player.find("td", {"class":"td_padding"})
        a_href = td_padding.find("a")
        img_src = td_padding.find("img")
        player_url = a_href.get("href")
        img_url = img_src.get("src")
        player_name = player.find_all("a", {"target":"_blank"})[1].get_text()
        player_info = player.find_all("td", {"class":"left"})[1].get_text()
        player_list.append({"name":player_name, "info":player_info, "player_url":player_url, "image_url": img_url})
    return player_list
    
    
def get_team_info(url):
    data = urllib2.urlopen(url).read()
    soup_data = BeautifulSoup(data)
    div_content = soup_data.find("div", {"class":"content"})
    logo_url = div_content.find("img").get("src")
    url_array = logo_url.split("/")
    logo_name = url_array[len(url_array)-1]
    team_images_dir = os.path.join(static_dir, "team_image")
    if not os.path.exists(team_images_dir):
        os.mkdir(team_images_dir)
    urllib.urlretrieve(logo_url, os.path.join(team_images_dir, logo_name))
    static_logo_url = logo_url
    team_summary = soup_data.find("div", {"class":"font"}).get_text()
    team_info = soup_data.find("div", {"class":"txt"}).get_text().strip()
    player_list = soup_data.find_all("span", {"class":"c2"})
    ignore = True
    player_all = []
    for player in player_list:
        if ignore:
            ignore = False
            continue
        player_a = player.find("a")
        player_name = player_a.get_text()
        player_all.append(player_name)
    team_name = soup_data.find("span", {"class":"title-text"}).get_text().strip()
    return {"name":team_name, "logo":static_logo_url, "summary":team_summary, "info":team_info, "player":player_all}    
    
    
if __name__ == '__main__':
    json_data, team_data = collect_info()
    print json.dumps(json_data)
    
    
    
