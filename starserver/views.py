# Resource map (routing table)
from . import api
from .models import Game, Turn, Planet, Fleet, Orders, FleetOrder
from .stars import new_game, process_turn

from flask import request
from flask.ext.restful import abort, Resource

from mongoengine.errors import ValidationError

# GameList
class GameList(Resource):
    """
    GET a list of all games, or POST a new game
    """
    def get(self):
        return [{"id": str(g.id), "name": g.name}
                for g in Game.objects]

    def post(self):
        data = request.get_json(force=True)
        g = new_game(name=data['name'])
        return {"created": True, "game_id": str(g.id)}


# Game: Get the settings for a game
class GameItem(Resource):
    """
    GET the settings for a single game
    """
    def get(self, game):
        g = Game.objects.get_or_404(id=game)
        return {"name": g.name}

class TurnList(Resource):
    """
    GET a list of turns for this game
    """
    def get(self, game):
        g = Game.objects.get_or_404(id=game)
        return [{"turn": t.turn, "done": t.is_done()}
                for t in Turn.objects(game=g)]

class TurnItem(Resource):
    """
    GET the universe for this turn
    """
    def get(self, game, turn):
        t= Turn.objects.get_or_404(game=game, turn=turn)

        planets = [{"planet": p.name,
                    "x": p.x,
                    "y": p.y,
                    "population": p.population}
                   for p in Planet.objects(turn=t)]

        fleets = [{"name": f.name,
                   "x": f.x,
                   "y": f.y}
                  for f in Fleet.objects(turn=t)]

        return {"planets": planets,
                "fleets": fleets,
                "done": t.is_done()}

class OrdersItem(Resource):
    """
    GET the current orders, or PUT new orders
    """
    def get(self, game, turn):
        t = Turn.objects.get_or_404(game=game, turn=turn)
        try:
            o = Orders.objects.get(turn=t)
        except Orders.DoesNotExist:
            o = Orders.objects.create(turn=t, done=False)

        fleetorders = [{"fleet": str(fo.fleet),
                        "dest_x": fo.dest_x,
                        "dest_y": fo.dest_y,
                        "warp": fo.warp}
                       for fo in FleetOrder.objects(orders=o)]
        return {"fleetorders": fleetorders, "done": o.done}

    def put(self, game, turn):
        data = request.get_json(force=True)
        t= Turn.objects.get_or_404(game=game, turn=turn)
        try:
            o = Orders.objects.get(turn=t)
            FleetOrder.objects(orders=o).delete()
        except Orders.DoesNotExist:
            o = Orders.objects.create(turn=t, done=False)

        for fo in data.get('fleetorders', []):
            f = Fleet.objects.get(turn=t, name=fo["fleet"])
            FleetOrder.objects.create(orders=o,
                                      fleet=f,
                                      dest_x=fo.get('dest_x'),
                                      dest_y=fo.get('dest_y'),
                                      warp=fo.get('warp'))
        o.done = bool(data.get('done'))
        o.save()

        if t.is_done():
            # "everyone"'s done, process turn
            process_turn(t)

        return {"status": "ok", "done": o.done}


# Resource map (routing table)
api.add_resource(GameList, '/games/')
api.add_resource(GameItem, '/games/<game>/')
api.add_resource(TurnList, '/games/<game>/turns/')
api.add_resource(TurnItem, '/games/<game>/turns/<int:turn>/')
api.add_resource(OrdersItem, '/games/<game>/turns/<int:turn>/orders/')
