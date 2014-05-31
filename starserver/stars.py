"""
Game logic of stars!

Will contain methods to initialize a game, advance a turn, and everything it entails

(will need to be split up into multiple modules at some point)
"""

from .models import Game, Turn, Planet, Fleet, Orders, FleetOrder
import math

def new_game(name):
    g = Game.objects.create(name=name)
    # initialize universe: planets

    # turn 1, aka intial state
    t1 = Turn.objects.create(game=g, turn=1)
    Fleet.objects.create(turn=t1, name="Peeping Tom", x=10, y=10)
    Planet.objects.create(turn=t1, name="Sol", x=10, y=10, population=100000)
    Planet.objects.create(turn=t1, name="Alpha", x=100, y=100)

    # Initial orders, should be per player
    Orders.objects.create(turn=t1, done=False)

    return g

def process_turn(t):
    # Process a turn, creating new turn and orders
    # objects for storing new turn and orders
    t2 = Turn.objects.create(game=t.game, turn=t.turn + 1)
    print("Processing turn {t2.turn}".format(**locals()))
    o2 = Orders.objects.create(turn=t2)

    # Order of events
    # 6. Fleets move
    for f in Fleet.objects(turn=t):
        print("... Moving fleet {f.id}".format(**locals()))
        move_fleet(f, t2, o2)

    # 14. Pop grows
    for p in Planet.objects(turn=t):
        print("... Processing planet {p.id}".format(**locals()))
        process_planet(p, t2)

def process_planet(p, t2):
    p2 = Planet(turn=t2, name=p.name, x=p.x, y=p.y, population=p.population)
    if p.population:
        p2.population = int(p2.population * 1.1)
    p2.save()

def move_fleet(f, t2, o2):
    f2 = Fleet(turn=t2, name=f.name, x=f.x, y=f.y)
    print(">>>", f2.to_json())
    keep_order = False
    try:
        fo = FleetOrder.objects.get(fleet=f)
    except FleetOrder.DoesNotExist:
        pass # no orders, no move!
    else:
        speed = fo.warp ** 2
        dist = math.sqrt((f.x - fo.dest_x)**2 + (f.y - fo.dest_y)**2)
        if int(dist) <= speed:
            f2.x, f2.y = fo.dest_x, fo.dest_y
        else:
            frac = speed / dist
            f2.x += int(frac * (fo.dest_x - f.x))
            f2.y += int(frac * (fo.dest_y - f.y))
            keep_order = True
    f2.save()
    if keep_order:
        FleetOrder.objects.create(orders=o2, fleet=f2, dest_x=fo.dest_x, dest_y=fo.dest_y, warp=fo.warp)
