from bs4 import BeautifulSoup
from requests_html import HTMLSession


def get_game_info(url):

    session = HTMLSession()
    r = session.get(url)
    r.html.render()  # this call executes the js in the page
    html_text = r.html.html


    soup = BeautifulSoup(html_text, 'html.parser')
    teams = soup.find('div', {'id': 'all_shots'}).find('div', {'class': 'filter switcher'}).find_all('div', {'class': ''})
    home_team = teams[0].find('a').text
    away_team = teams[1].find('a').text

    shots_table = soup.find('table', {'id': 'shots_all'})
    shots = shots_table.select('tr[class^="shots_"]')

    xg_lists = {home_team: [], away_team: []}
    xgot_lists = {home_team: [], away_team: []}
    first_half_extra = 0
    for shot in shots:
        player = shot.find('td', {'data-stat': 'player'}).find("a").text
        minute = shot.find('th', {'data-stat': 'minute'}).text

        if "+" in minute and minute.split("+")[0] == "45":
            extra = int(minute.split("+")[1])
            first_half_extra = extra if extra > first_half_extra else first_half_extra
            minute = int(minute.split("+")[0]) + extra
        elif "+" in minute:
            minute = int(minute.split("+")[0]) + int(minute.split("+")[1]) + first_half_extra
        else:
            minute = int(minute) + first_half_extra

        team = shot.find('td', {'data-stat': 'team'}).find("a").text
        xg = shot.find('td', {'data-stat': 'xg_shot'}).text
        xgot = shot.find('td', {'data-stat': 'psxg_shot'}).text

        xg_info = {
            "minute": minute,
            "player": player,
            "xg": float(xg)
        }
        xg_lists[team].append(xg_info)
        if xgot != "":
            xgot_info = {
                "minute": minute,
                "player": player,
                "xgot": float(xgot)
            }
            xgot_lists[team].append(xgot_info)


    result = {
        "home_team": {
            "name": home_team,
            "xg": xg_lists[home_team],
            "xgot": xgot_lists[home_team]
        },
        "away_team": {
            "name": away_team,
            "xg": xg_lists[away_team],
            "xgot": xgot_lists[away_team]
        }
    }

    return result
