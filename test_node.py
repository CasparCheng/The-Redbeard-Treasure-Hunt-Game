import pytest

from grid import Node


@pytest.mark.parametrize("hcost, gcost, fcost", [
    (3.0, 2.0, 5.0),
])
def test_fcost(hcost, gcost, fcost):
    n = Node(False, 0, 0)
    n.set_hcost(hcost)
    n.set_gcost(gcost)
    assert n.fcost() == fcost


@pytest.mark.parametrize("node, parent", [
    (Node(True, 1, 2), Node(True, 3, 4)),
])
def test_set_parent(node, parent):
    node.set_parent(parent)
    assert id(node.parent) == id(parent)


@pytest.mark.parametrize("n1, n2, distance", [
    (Node(True, 0, 0), Node(False, 0, 1), 10),
    (Node(True, 1, 0), Node(False, 0, 0), 10),
    (Node(True, 0, 0), Node(False, 1, 1), 14),
    (Node(True, 1, 0), Node(False, 0, 1), 14),
    (Node(True, 8, 4), Node(False, 1, 10), 94),
])
def test_distance(n1, n2, distance):
    assert n1.distance(n2) == distance


@pytest.mark.parametrize("n1, n2", [
    (Node(True, 1, 2), Node(True, 1, 2)),
    (Node(True, 2, 2), Node(True, 2, 2)),
    (Node(False, 1, 2), Node(False, 1, 2)),
    (Node(False, 2, 2), Node(False, 2, 2)),
])
def test_eq(n1, n2):
    assert n1 == n2


@pytest.mark.parametrize("n1, n2", [
    (Node(True, 1, 2), Node(True, 2, 1)),
    (Node(True, 1, 2), Node(True, 2, 2)),
    (Node(False, 0, 0), "Node(False, 0, 0)"),
    (Node(False, 0, 0), 0),
    (Node(False, 0, 0), None),
])
def test_neq(n1, n2):
    assert n1 != n2


def test_lt():
    ...


@pytest.mark.parametrize("node, node_string", [
    (Node(True, 1, 1), '.'),
    (Node(False, 1, 1), '+'),
])
def test_str(node, node_string):
    assert str(node) == node_string
