"""
Representation of Stars! objects such as planets, ships, etc.

Uses mongoengine to easily persist and query.
Maybe we should move to a relational db at some point, but maybe not.
"""

from . import db

class Game(db.Document):
    name = db.StringField(required=True)

class Turn(db.Document):
    """
    Representation of the universe on a given turn
    """
    game = db.ReferenceField(Game)
    turn = db.IntField(required=True)

    def is_done(self):
        """Is everyone done with their turn?"""
        return all(o.done for o in Orders.objects(turn=self))

class Planet(db.Document):
    """
    The status of a planet on a given turn.
    Contains all information (name, location, owner, population, minerals etc)
    Maybe at some point split into variable (owner etc) and invariant (name, location) parts
    """
    turn = db.ReferenceField(Turn)
    name = db.StringField(required=True)
    x = db.IntField(required=True)
    y = db.IntField(required=True)
    population = db.IntField()


class Fleet(db.Document):
    """
    A fleet at a certain turn.
    Will contain ownwer, location, damage, ships, etc
    """
    turn = db.ReferenceField(Turn)
    name = db.StringField(required=True)
    x = db.IntField(required=True)
    y = db.IntField(required=True)


class Orders(db.Document):
    """
    Orders for a player for a given turn
    (currently ignoring "player")
    """
    turn = db.ReferenceField(Turn)
    done = db.BooleanField()

class FleetOrder(db.Document):
    """
    An order for a fleet
    (fixme: since fleet is per turn, there is some redundancy here)
    """
    orders = db.ReferenceField(Orders)
    fleet = db.ReferenceField(Fleet)
    dest_x = db.IntField()
    dest_y = db.IntField()
    warp = db.IntField()
