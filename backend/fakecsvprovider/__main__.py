import os

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index() -> str:
    return 'fake csv provider'


@app.route('/fixture.csv')
def fixture() -> str:
    return """season,date,league_id,league,team1,team2,spi1,spi2,prob1,prob2,probtie,proj_score1,proj_score2,importance1,importance2,score1,score2,xg1,xg2,nsxg1,nsxg2,adj_score1,adj_score2
2022,2022-11-13,0000,Test League,Always Wins,Always Loses,65.59,39.99,0.7832,0.0673,0.1495,2.58,0.62,77.1,28.8,90,0,0.49,0.45,1.05,0.75,3.15,0.0
2022,2022-11-13,0000,Test League,Team A,Team B,65.59,39.99,0.7832,0.0673,0.1495,2.58,0.62,77.1,28.8,1,1,0.49,0.45,1.05,0.75,3.15,0.0"""


app.run(debug=True, host="0.0.0.0", port=int(os.environ.get('PORT', 5002)))
