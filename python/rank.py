from typing import List
from types import SimpleNamespace
import json
from player import Player
from game import Game
from match import Match
from graphqlclient import GraphQLClient


class Ranking():

  def __init__(self, players:List[Player] = []) -> None:
    self.rankings = players

  # Takes a list of matches from each player and zippers them into one list 
  # Result is ordered by ID and used for updating the rankings
  def merge_matches(self, matches: List[List[Match]]) -> None:
    pass

  def update_from_sgg(self) -> None:
    matches : List[List[Match]] = []
    for player in rankings:
      matches.append(self.get_recent_sets_from_sgg(player))
    merged_matches = self.merge_matches(matches)
    self.update_rankings(merged_matches)

  def get_recent_sets_from_sgg(self, player: Player) -> List[Match]:
    with open('sggapikey.txt', 'r') as file:
      authToken = file.read().rstrip()
    apiVersion = 'alpha'
    client = GraphQLClient('https://api.start.gg/gql/' + apiVersion)
    client.inject_token('Bearer ' + authToken)

    result = client.execute('''
      query getUserSets($userSlug: String) {
        user(slug: $userSlug) {
          id
          name
          slug
          player {
            prefix
            gamerTag
            id
            sets {
              nodes {
                id
                completedAt
                winnerId
                state
                slots {
                  entrant {
                    name
                    id
                  }
                }
              }
            }
          }
        }
      }
      ''',
      {
       "userSlug": f"{player.slug}"
      }
    )
    resultData = json.loads(result, object_hook=lambda d: SimpleNamespace(**d))
    if 'errors' in resultData:
      pass #TODO
    user = resultData["data"]["user"]
    resultPlayer = user["player"]
    nodes: List[any] = resultPlayer["sets"]["nodes"]
    for node in nodes:
      if not node["state"] == 3 or not node["winnerId"]:
        continue # match in progress, ignore
      winnerId = node["winnerId"]
      slots = node["slots"]
      winner = None # TODO: Assign winner somewhere
      for slot in slots:
        entrant = slot["entrant"]
        if entrant["id"] == winnerId:
          winner = entrant
          break
   
    

  # Updates rankings based on a sequence of matches, say for a tournament
  def update_rankings(self, matches: List[Match]) -> None:
    for match in matches:
      if match.loser not in self.rankings: # No one needs to be replaced
        continue
      highRank = self.rankings.index(match.loser)
      if match.winner not in self.rankings[0:highRank]: # Loser ranked below the winner, loser takes winner's spot
        print(f"{match.winner} took {match.loser}'s spot at #{highRank+1}")
        try:
          lowRank = self.rankings.index(match.winner)
          self.rankings[lowRank] = match.loser
        except ValueError:
          pass # winner previously was not ranked 
        self.rankings[highRank] = match.winner
        
        
  def __str__(self) -> str:
    out = ""
    for ranking, player in enumerate(self.rankings):
      out += f"{ranking+1}. {player}\n"
    return out

# Players in the ranking, i.e. "This is a player named Ethan"
ethan = Player("Ethan")
aidan = Player("Aidan")
alex = Player("Alex")
luke = Player("Luke")
justin = Player("Justin")
mike = Player("Mike")

# Initial rankings in order, so ethan is #1
rankings = Ranking([ethan, aidan, alex, luke, justin])

# Matches - Match(player1, player2, and the games between them). Game(alex) means alex won the game. 
match1 = Match(aidan, alex, [Game(alex), Game(alex)]) # ethan alex aidan luke justin
match2 = Match(justin, alex, [Game(justin), Game(justin)]) # ethan justin aidan luke alex
match3 = Match(ethan, alex, [Game(ethan), Game(ethan)]) # no change
match4 = Match(luke, ethan, [Game(luke), Game(luke)]) # luke justin aidan ethan alex
match5 = Match(ethan, mike, [Game(mike), Game(ethan), Game(mike)]) # luke justin aidan mike alex 

# Based on the results of these matches, update the rankings. The results after each match are after the # next to them above
rankings.update_rankings([match1, match2, match3, match4, match5])
print(rankings) # Outputs the rankings below when I run the command 



        

