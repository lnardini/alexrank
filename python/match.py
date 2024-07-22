from player import Player
from game import Game
from typing import List
from datetime import datetime

class Match():
  
  def __init__(self, id: int, completedAt: int, winnerId: int, state: int, slots) -> None:
    pass
  #   self.player_one = player_one
  #   self.player_two = player_two
  #   self.games = games
  #   self.winner = self.compute_winner()
  #   self.loser = player_one if self.winner == player_two else player_two
  #   self.timestamp = timestamp


  # def compute_winner(self) -> Player:
  #   if self.player_one == self.player_two:
  #     raise ValueError("Players are the same")
  #   p1_wins = p2_wins = 0
  #   for game in self.games:
  #     if game.winner == self.player_one:
  #       p1_wins+=1
  #     elif game.winner == self.player_two:
  #       p2_wins+=1
  #     else:
  #       raise ValueError("Game winner not in match")
  #   if p1_wins > p2_wins:
  #     return self.player_one
  #   elif p2_wins > p1_wins:
  #     return self.player_two
  #   else:
  #     raise ValueError("Tie game")
      