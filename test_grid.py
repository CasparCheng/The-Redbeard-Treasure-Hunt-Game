import os
import os.path as op
import tempfile

import pytest

from grid import Grid, Node
from grid_parameters import DIRECTIONS, GRID_TEST_DATA

TESTS_ROOT_DIR = op.dirname(op.abspath(__file__))


@pytest.mark.parametrize("grid_data", GRID_TEST_DATA)
def test_init(grid_data):
    with tempfile.NamedTemporaryFile(mode='wt') as grid_file:
        grid_file.write(grid_data.grid)
        grid_file.flush()
        grid_1 = Grid(grid_file.name)
    grid_2 = Grid("", grid_data.grid.strip().split())
    assert grid_1.map == grid_2.map


@pytest.mark.parametrize("grid_data", GRID_TEST_DATA)
def test_grid_width(grid_data):
    text_grid = grid_data.grid.strip().split('\n')
    grid = Grid("", text_grid)
    assert grid.width == len(text_grid[0])


@pytest.mark.parametrize("grid_data", GRID_TEST_DATA)
def test_grid_height(grid_data):
    text_grid = grid_data.grid.strip().split('\n')
    grid = Grid("", text_grid)
    assert grid.height == len(text_grid)


@pytest.mark.parametrize("grid_data", GRID_TEST_DATA)
def test_grid_node_easy(grid_data):
    text_grid = grid_data.grid.strip().split('\n')
    grid = Grid("", text_grid)
    for i in range(len(text_grid[0])):
        for j in range(len(text_grid)):
            navigable = text_grid[j][i] == '.'
            try:
                node = grid.map[i][j]
            except IndexError:
                node = grid.map[j][i]
            assert node == Node(navigable, i, j) or node == Node(navigable, j, i)


@pytest.mark.parametrize("grid_data", GRID_TEST_DATA)
def test_grid_node_hard(grid_data):
    text_grid = grid_data.grid.strip().split('\n')
    grid = Grid("", text_grid)
    for i in range(len(text_grid[0])):
        for j in range(len(text_grid)):
            navigable = text_grid[j][i] == '.'
            assert grid.map[i][j] == Node(navigable, i, j)


@pytest.mark.parametrize("grid_data", GRID_TEST_DATA)
def test_grid_boat_easy(grid_data):
    text_grid = grid_data.grid.strip().split('\n')
    grid = Grid("", text_grid)
    for i in range(len(text_grid[0])):
        for j in range(len(text_grid)):
            if text_grid[j][i] == 'B':
                assert grid.boat == Node(True, i, j) or grid.boat == Node(True, j, i)
                return


@pytest.mark.parametrize("grid_data", GRID_TEST_DATA)
def test_grid_boat_hard(grid_data):
    text_grid = grid_data.grid.strip().split('\n')
    grid = Grid("", text_grid)
    for i in range(len(text_grid[0])):
        for j in range(len(text_grid)):
            if text_grid[j][i] == 'B':
                assert grid.boat == Node(True, i, j)
                return


@pytest.mark.parametrize("grid_data", GRID_TEST_DATA)
def test_str(grid_data):
    grid = Grid("", grid_data.grid.strip().split('\n'))
    # Call .strip() because we don't care about tailing newline
    assert str(grid).strip() == grid_data.grid.strip()


@pytest.mark.parametrize("grid_data", GRID_TEST_DATA)
@pytest.mark.parametrize("direction", DIRECTIONS)
def test_move(grid_data, direction):
    text_grid = grid_data.grid.strip().split('\n')
    g = Grid("", text_grid)
    x_before = g.boat.grid_x
    y_before = g.boat.grid_y
    g.move(direction[0])
    x_after = x_before + direction[1]
    y_after = y_before + direction[2]
    if (x_after in range(0, g.width - 1) and y_after in range(0, g.height - 1)
            and text_grid[y_after][x_after] != '+'):
        assert g.boat.grid_x == x_after
        assert g.boat.grid_y == y_after
    else:
        assert g.boat.grid_x == x_before
        assert g.boat.grid_y == y_before


@pytest.mark.parametrize("grid_data", GRID_TEST_DATA)
def test_find_path_length_1(grid_data):
    """Test that find_path finds a path with the correct length."""
    text_grid = grid_data.grid.strip().split('\n')
    g = Grid("", text_grid)
    # None of the nodes have any parents at this point,
    # so there should be no path from boat to treasure
    assert g.retrace_path(g.boat, g.treasure) == []
    g.find_path(g.boat, g.treasure)
    path = g.retrace_path(g.boat, g.treasure)
    solution_length = sum(grid_data.grid_solutions[0].count(c) for c in ['B', 'T', '*'])
    assert len(path) == solution_length


@pytest.mark.parametrize("grid_filename",
                         [f for f in os.listdir(op.join(TESTS_ROOT_DIR, 'find_path'))])
def test_find_path_length_2(grid_filename):
    """Test that find_path finds a path with the correct length.

    This test uses additional examples provided by @ProfDema.
    """
    with open(op.join(TESTS_ROOT_DIR, 'find_path', grid_filename), 'r') as ifh:
        grid_data = ifh.read().strip()
    num_steps = grid_data.count('*') + 2
    text_grid = grid_data.replace('*', '.').split('\n')
    g = Grid("", text_grid)
    g.find_path(g.boat, g.treasure)
    path = g.retrace_path(g.boat, g.treasure)
    assert len(path) == num_steps


@pytest.mark.parametrize("grid_data", GRID_TEST_DATA)
def test_find_path_solution(grid_data):
    """Test that find_path finds the correct path."""
    text_grid = grid_data.grid.strip().split('\n')
    g = Grid("", text_grid)
    g.find_path(g.boat, g.treasure)
    path = g.retrace_path(g.boat, g.treasure)
    for solution in grid_data.grid_solutions:
        solution_grid = [list(l) for l in solution.strip().split('\n')]
        match_found = all(solution_grid[n.grid_y][n.grid_x] in ['B', 'T', '*'] for n in path)
        if match_found:
            break
    assert match_found


@pytest.mark.parametrize("grid_data", GRID_TEST_DATA)
def test_get_treasure(grid_data):
    text_grid = grid_data.grid.strip().split('\n')
    g = Grid("", text_grid)
    distance = g.boat.distance(g.treasure)
    assert all(g.get_treasure(s_range) is None for s_range in range(0, distance))
    assert all(g.get_treasure(s_range) == g.treasure for s_range in range(distance, distance + 100))


@pytest.mark.parametrize("grid_data", GRID_TEST_DATA)
def test_plot_path(grid_data):
    text_grid = grid_data.grid.strip().split('\n')
    g = Grid("", text_grid)
    assert g.plot_path(g.boat, g.treasure).strip() in [s.strip() for s in grid_data.grid_solutions]
