from nose.tools import assert_equal, assert_not_equal
from contextlib import contextmanager

from starserver.models import *
from starserver.stars import move_fleet

@contextmanager
def test_game():
    g = Game.objects.create(name="Test")
    try:
        yield g
    finally:
        # delete all objects related to test game
        for t in Turn.objects(game=g):
            for o in Orders.objects(turn=t):
                FleetOrder.objects(orders=o).delete()
                o.delete()
            Fleet.objects(turn=t).delete()
            t.delete()
        g.delete()

def test_travel():
    with test_game() as g:
        t1 = Turn.objects.create(game=g, turn=1)
        # move from 0,0 to 100,0 at warp 5
        f = Fleet.objects.create(turn=t1, name="Test", x=0, y=0)
        o = Orders.objects.create(turn=t1)
        FleetOrder.objects.create(orders=Orders.objects.create(turn=t1),
                                  fleet=f, dest_x=100, dest_y=0, warp=5)

        # move fleet
        t2 = Turn.objects.create(game=g, turn=2)
        move_fleet(f, t2)

        # we should have moved to 25,0 with the existing order
        f2 = Fleet.objects.get(turn=t2, name="Test")
        assert_equal(f2.x, 25)
        assert_equal(f2.y, 0)
        fo = FleetOrder.objects.get(fleet=f2)
        assert_equal(fo.dest_x, 100)
        assert_equal(fo.dest_y, 0)

        # adjust order to warp 9 and check that we don't overshoot and that order is gone
        fo.warp = 9
        fo.save()
        t3 = Turn.objects.create(game=g, turn=3)
        move_fleet(f2, t3)

        f3 = Fleet.objects.get(turn=t3, name="Test")
        assert_equal(f3.x, 100)
        assert_equal(f3.y, 0)
        assert_equal(0, FleetOrder.objects(fleet=f3).count())

        # if we want to move 25.7 ly at warp 5, we should get there in one turn
        FleetOrder.objects.create(orders=Orders.objects.create(turn=t3),
                                  fleet=f3, dest_x=125, dest_y=5, warp=5)

        t4 = Turn.objects.create(game=g, turn=4)
        move_fleet(f3, t4)


        f4 = Fleet.objects.get(turn=t4, name="Test")
        assert_equal(f4.x, 125)
        assert_equal(f4.y, 5)
        assert_equal(0, FleetOrder.objects(fleet=f4).count())
