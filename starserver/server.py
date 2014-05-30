"""
Stub server code.
It is possible to list and add games and retrieve 'settings' for a game.

This is obviously not a complete stars clone yet :-)
- global GAMES should turn into a database
  (and we can't assume 1:1 API to internal state)
- code should be split into different modules
- some actual content would be nice
"""

from flask import Flask, request
from flask.ext.restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

# obviously will need to be replaced by a database of sorts at some point
GAMES = []


# GameList
class GameList(Resource):
    """
    GET a list of all games, or POST a new game
    """
    def get(self):
        return GAMES

    def post(self):
        # we might want to do input validation at some point :)
        game = request.get_json(force=True)
        GAMES.append(game)
        return {"created": True, "game_id": len(GAMES)-1}, 201


# Game: Get the settings for a game
class Game(Resource):
    """
    GET the settings for a single game
    """
    def get(self, game_id):
        try:
            return GAMES[game_id]
        except IndexError:
            abort(404)


# Resource map (routing table)
api.add_resource(GameList, '/games')
api.add_resource(Game, '/games/<int:game_id>')


if __name__ == '__main__':
    # start debug server if called on command line
    app.run(debug=True)
