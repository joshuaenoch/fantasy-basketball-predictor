import requests
from bs4 import BeautifulSoup


def get_player_position(player_name):
    base_url = "https://www.basketball-reference.com"
    search_url = f"{base_url}/search/search.fcgi?search={player_name.replace(' ', '+')}"
    search_response = requests.get(search_url)
    search_soup = BeautifulSoup(search_response.content, "html.parser")
    player_link = search_soup.find("div", {"class": "search-item-url"}).text
    player_url = f"{base_url}{player_link}"

    player_response = requests.get(player_url)
    player_soup = BeautifulSoup(player_response.content, "html.parser")
    position = player_soup.find("span", {"itemprop": "position"}).text
    return position


player_name = "LeBron James"
player_position = get_player_position(player_name)
print(f"{player_name}'s specific position is {player_position}")
