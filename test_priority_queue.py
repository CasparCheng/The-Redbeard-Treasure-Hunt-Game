import pytest

from container import PriorityQueue

# test_name: (less_than, input_items, output_items)
PRIORITY_QUEUE_TESTS = {
    'shortest-first': (lambda a, b: len(a) < len(b), ['fred', 'arju', 'monalisa', 'hat'],
                       ['monalisa', 'arju', 'fred', 'hat']),
    'longest-first': (lambda a, b: len(a) > len(b), ['fred', 'arju', 'monalisa', 'hat'],
                      ['hat', 'arju', 'fred', 'monalisa']),
    'alphabetically-incr': (lambda a, b: a <= b, ['fred', 'arju', 'monalisa', 'hat'],
                            ['monalisa', 'hat', 'fred', 'arju']),
    'integers-and-floats': (lambda a, b: a <= b, [4, 3, 7, 1, 5.5], [7, 5.5, 4, 3, 1]),
    'identical-numbers-incr': (lambda a, b: a < b, [1, 2] * 50, [2] * 50 + [1] * 50),
    'identical-numbers-decr': (lambda a, b: a > b, [1, 2] * 50, [1] * 50 + [2] * 50),
}


@pytest.mark.parametrize(
    "less_than, input_items, output_items",
    PRIORITY_QUEUE_TESTS.values(),
    ids=list(PRIORITY_QUEUE_TESTS.keys()))
def test_private_queue(less_than, input_items, output_items):
    pq = PriorityQueue(less_than)
    for item in input_items:
        pq.add(item)
    assert pq._queue == output_items


@pytest.mark.parametrize(
    "less_than, input_items, output_items",
    PRIORITY_QUEUE_TESTS.values(),
    ids=list(PRIORITY_QUEUE_TESTS.keys()))
def test_remove(less_than, input_items, output_items):
    pq = PriorityQueue(less_than)
    for item in input_items:
        pq.add(item)
    while not pq.is_empty():
        assert pq.remove() == output_items.pop()
