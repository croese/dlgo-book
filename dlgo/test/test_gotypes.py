from dlgo.gotypes import Player, Point


def test_other_player():
    assert Player.white.other == Player.black
    assert Player.black.other == Player.white


def test_point_knows_its_neighbors():
    assert set(Point(3, 4).neighbors()) == set(
        [
            Point(3, 5),
            Point(3, 3),
            Point(2, 4),
            Point(4, 4),
        ]
    )
