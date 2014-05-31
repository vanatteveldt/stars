
# GameList
class GameList(Resource):
    """
    GET a list of all games, or POST a new game
    """
    def get(self):
        return GAMES

    def post(self):
        # we might want to do input validation at some point :)
        settings = request.get_json(force=True)
        game = {"settings": settings,
                "players" : [1],
                "turns": []
        GAMES.append(game)
        return {"created": True, "game_id": len(GAMES)-1}, 201


# Game: Get the settings for a game
class Game(Resource):
    """
    GET the settings for a single game
    """
    def get(self, game_id):
        try:
            g = GAMES[game_id]
        except IndexError:
            abort(404)
        else:
            return {"settings": game['settings'],
                    "players" : game['players']}
