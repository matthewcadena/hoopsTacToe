from nba_api.stats.static import teams
from nba_api.stats.static import players
from .queries import *
import random
import requests
import jsonpickle
from dotenv import load_dotenv
import os

load_dotenv()


class Player:
    def __init__(self):
        playerData = getPlayer()
        self.id = playerData['id']
        self.name = playerData['full_name']
        self.imageUrl = getPlayerImageUrl(self.name)


class Team:
    def __init__(self, nickname):
        teamData = teams.find_teams_by_nickname(nickname)
        self.id = teamData[0]['id']
        self.fullName = teamData[0]['full_name']
        self.nickname = teamData[0]['nickname']
        self.imageUrl = getTeamImageUrl(self.nickname)


class Game:
    def __init__(self):
        self.team1 = None
        self.team2 = None
        self.team3 = None
        self.team4 = None
        self.team5 = None
        self.player = Player()
        self.setTeams()
        self.square1Answers = getTeamByTeamAnswers(self.team1, self.team3)
        self.square2Answers = getTeamByTeamAnswers(self.team2, self.team3)
        self.square3Answers = getTeamByPlayerAnswers(self.team3, self.player)
        self.square4Answers = getTeamByTeamAnswers(self.team1, self.team4)
        self.square5Answers = getTeamByTeamAnswers(self.team2, self.team4)
        self.square6Answers = getTeamByPlayerAnswers(self.team4, self.player)
        self.square7Answers = getTeamByTeamAnswers(self.team1, self.team5)
        self.square8Answers = getTeamByTeamAnswers(self.team2, self.team5)
        self.square9Answers = getTeamByPlayerAnswers(self.team5, self.player)
        self.board = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]
        self.turn = 1

    def to_json(self):
        return jsonpickle.encode(self)

    @classmethod
    def from_json(cls, json_data):
        return jsonpickle.decode(json_data)

    def setTeams(self):
        teamSet = teams.get_teams()
        usedTeams = set()
        teamCount = 0
        while teamCount < 5:
            team = teamSet[random.randint(0, len(teamSet) - 1)]
            while team['nickname'] in usedTeams:
                team = teamSet[random.randint(0, len(teamSet) - 1)]
            usedTeams.add(team['nickname'])
            teamCount += 1
        # use the Team constructor to create a team object for each team based on the nickname
        self.team1 = Team(usedTeams.pop())
        self.team2 = Team(usedTeams.pop())
        self.team3 = Team(usedTeams.pop())
        self.team4 = Team(usedTeams.pop())
        self.team5 = Team(usedTeams.pop())


# static set of 54 players that I thought would be good options for the "teammates of" column
def getPlayer():
    playerIDs = ['2544', '1627742', '203468', '101150', '2037', '1626157', '200755', '201942', '202326',
                 '201980', '201149', '201586', '200794', '201599', '708', '2546', '203999', '201565',
                 '203497', '202322', '201143', '200746', '2738', '200768', '200755', '2564', '203521',
                 '203109', '201976', '1627936', '201567', '202710', '201188', '203110', '202681', '202691',
                 '2203', '201988', '201980', '200765', '1891', '1628365', '202711', '201144', '1629628',
                 '202699', '1628398', '101108', '1628386', '203944', '203935', '203497', '203952', '204001']
    iD = playerIDs[random.randint(0, len(playerIDs) - 1)]

    return players.find_player_by_id(iD)


def getPlayerImageUrl(name):
    return getCustomImage(f'{name} basketball headhsot')


# gets player image urls from a static list taken from nba.com
def getTeamImageUrl(team):
    # source for images: nba.com
    teamUrls = {'Hawks': 'https://cdn.nba.com/logos/nba/1610612737/primary/L/logo.svg',
                'Celtics': 'https://cdn.nba.com/logos/nba/1610612738/primary/L/logo.svg',
                'Cavaliers': 'https://cdn.nba.com/logos/nba/1610612739/primary/L/logo.svg',
                'Pelicans': 'https://cdn.nba.com/logos/nba/1610612740/primary/L/logo.svg',
                'Bulls': 'https://cdn.nba.com/logos/nba/1610612741/primary/L/logo.svg',
                'Mavericks': 'https://cdn.nba.com/logos/nba/1610612742/primary/L/logo.svg',
                'Nuggets': 'https://cdn.nba.com/logos/nba/1610612743/primary/L/logo.svg',
                'Warriors': 'https://cdn.nba.com/logos/nba/1610612744/primary/L/logo.svg',
                'Rockets': 'https://cdn.nba.com/logos/nba/1610612745/primary/L/logo.svg',
                'Clippers': 'https://cdn.nba.com/logos/nba/1610612746/primary/L/logo.svg',
                'Lakers': 'https://cdn.nba.com/logos/nba/1610612747/primary/L/logo.svg',
                'Heat': 'https://cdn.nba.com/logos/nba/1610612748/primary/L/logo.svg',
                'Bucks': 'https://cdn.nba.com/logos/nba/1610612749/primary/L/logo.svg',
                'Timberwolves': 'https://cdn.nba.com/logos/nba/1610612750/primary/L/logo.svg',
                'Nets': 'https://cdn.nba.com/logos/nba/1610612751/primary/L/logo.svg',
                'Knicks': 'https://cdn.nba.com/logos/nba/1610612752/primary/L/logo.svg',
                'Magic': 'https://cdn.nba.com/logos/nba/1610612753/primary/L/logo.svg',
                'Pacers': 'https://cdn.nba.com/logos/nba/1610612754/primary/L/logo.svg',
                '76ers': 'https://cdn.nba.com/logos/nba/1610612755/primary/L/logo.svg',
                'Suns': 'https://cdn.nba.com/logos/nba/1610612756/primary/L/logo.svg',
                'Trail Blazers': 'https://cdn.nba.com/logos/nba/1610612757/primary/L/logo.svg',
                'Kings': 'https://cdn.nba.com/logos/nba/1610612758/primary/L/logo.svg',
                'Spurs': 'https://cdn.nba.com/logos/nba/1610612759/primary/L/logo.svg',
                'Thunder': 'https://cdn.nba.com/logos/nba/1610612760/primary/L/logo.svg',
                'Raptors': 'https://cdn.nba.com/logos/nba/1610612761/primary/L/logo.svg',
                'Jazz': 'https://cdn.nba.com/logos/nba/1610612762/primary/L/logo.svg',
                'Grizzlies': 'https://cdn.nba.com/logos/nba/1610612763/primary/L/logo.svg',
                'Wizards': 'https://cdn.nba.com/logos/nba/1610612764/primary/L/logo.svg',
                'Pistons': 'https://cdn.nba.com/logos/nba/1610612765/primary/L/logo.svg',
                'Hornets': 'https://cdn.nba.com/logos/nba/1610612766/primary/L/logo.svg'}
    return teamUrls[team]


# uses google images API to get the first image result from a given query
# (free account limits me to 100 queries a day, so it's only used to get the image for the teammate player)
def getCustomImage(query):
    # source: Google Programmable Search Engine
    key = os.environ.get('GOOGLE_API_KEY')
    cx = "3768f9c509d264e1c"
    q = query
    baseUrl = f"https://www.googleapis.com/customsearch/v1?key={key}&cx={cx}&searchType=image&q={q}?"
    response = requests.get(baseUrl)
    responseData = response.json()
    if 'items' in responseData:
        return responseData['items'][0]['link']
    else:
        return 'no image found (query limit exceeded)'
