from flask import Flask
from rank import Ranking
from player import Player

app = Flask(__name__)

@app.route("/")
def main():
  pass