import io
import os.path as op
import sys
import tempfile
from contextlib import contextmanager

import pytest

from grid import Grid
from grid_parameters import GRID_TEST_DATA
from treasurehunt import TreasureHunt

TESTS_DIR = op.abspath(op.dirname(__file__))


@contextmanager
def capture_print_statements(handle):
    stdout = sys.stdout
    sys.stdout = handle
    yield
    sys.stdout = stdout


@pytest.mark.parametrize("grid_data", GRID_TEST_DATA)
@pytest.mark.parametrize("sonars, so_range", [(1, 100)])
def test_init(grid_data, sonars, so_range):
    with tempfile.NamedTemporaryFile(mode='wt') as grid_file:
        grid_file.write(grid_data.grid)
        grid_file.flush()
        g = Grid(grid_file.name)
        th = TreasureHunt(grid_file.name, sonars, so_range)
    assert th.grid_path == grid_file.name
    assert th.grid.map == g.map
    assert th.sonars == sonars
    assert th.so_range == so_range
    assert th.state == 'STARTED'


@pytest.mark.parametrize("grid_data, winning_commands",
                         [(grid_data, winning_commands)
                          for grid_data in GRID_TEST_DATA
                          for winning_commands in grid_data.winning_commands])
@pytest.mark.parametrize("check_returned_state", [True, False])
def test_process_winning_commands(grid_data, winning_commands, check_returned_state):
    with tempfile.NamedTemporaryFile(mode='wt') as grid_file:
        grid_file.write(grid_data.grid)
        grid_file.flush()
        th = TreasureHunt(grid_file.name, 0, 0)
    for i, command in enumerate(winning_commands):
        state = th.process_command(command)
        assert (state if check_returned_state else
                th.state) == ('STARTED' if i != (len(winning_commands) - 1) else 'WON')


@pytest.mark.parametrize("grid_data, losing_commands",
                         [(grid_data, losing_commands)
                          for grid_data in GRID_TEST_DATA
                          for losing_commands in grid_data.losing_commands])
@pytest.mark.parametrize("check_returned_state", [True, False])
def test_process_losing_commands(grid_data, losing_commands, check_returned_state):
    with tempfile.NamedTemporaryFile(mode='wt') as grid_file:
        grid_file.write(grid_data.grid)
        grid_file.flush()
        th = TreasureHunt(grid_file.name, 0, 0)
    for i, command in enumerate(losing_commands):
        state = th.process_command(command)
        assert (state if check_returned_state else th.state) == 'STARTED'


@pytest.mark.parametrize("grid_data", GRID_TEST_DATA)
@pytest.mark.parametrize("padding", [0, 1, 2])
@pytest.mark.parametrize("check_returned_state", [True, False])
def test_successful_sonar(grid_data, padding, check_returned_state):
    # Grid
    text_grid = grid_data.grid.strip().split('\n')
    g = Grid("", text_grid)
    distance = g.boat.distance(g.treasure)
    # TreasureHunt
    grid_file = tempfile.NamedTemporaryFile(mode='wt')
    grid_file.write(grid_data.grid)
    grid_file.flush()
    th = TreasureHunt(grid_file.name, 1, distance + padding)
    # Logic
    state = th.process_command('SONAR')
    assert th.sonars == 0
    assert (state if check_returned_state else th.state) in ['STARTED', 'WON']


@pytest.mark.parametrize("grid_data", GRID_TEST_DATA)
@pytest.mark.parametrize("padding", [-3, -2, -1])
@pytest.mark.parametrize("check_returned_state", [True, False])
def test_failed_sonar(grid_data, padding, check_returned_state):
    # Grid
    text_grid = grid_data.grid.strip().split('\n')
    g = Grid("", text_grid)
    distance = g.boat.distance(g.treasure)
    # TreasureHunt
    grid_file = tempfile.NamedTemporaryFile(mode='wt')
    grid_file.write(grid_data.grid)
    grid_file.flush()
    th = TreasureHunt(grid_file.name, 1, distance + padding)
    # Logic
    state = th.process_command('SONAR')
    assert th.sonars == 0
    assert (state if check_returned_state else th.state) in ['STARTED', 'OVER']


@pytest.mark.parametrize("grid_data", GRID_TEST_DATA)
def test_plot(grid_data):
    # Grid
    text_grid = grid_data.grid.strip().split('\n')
    g = Grid("", text_grid)
    distance = g.boat.distance(g.treasure)
    # TreasureHunt
    grid_file = tempfile.NamedTemporaryFile(mode='wt')
    grid_file.write(grid_data.grid)
    grid_file.flush()
    # Logic
    th = TreasureHunt(grid_file.name, 1, distance + 2)
    th.process_command('SONAR')
    handle = io.StringIO()
    with capture_print_statements(handle):
        th.process_command('PLOT')
    handle.seek(0)
    assert handle.read().strip() in [s.strip() for s in grid_data.grid_solutions]


@pytest.mark.parametrize("grid_data", GRID_TEST_DATA)
@pytest.mark.parametrize("check_returned_state", [True, False])
def test_process_quit_command(grid_data, check_returned_state):
    with tempfile.NamedTemporaryFile(mode='wt') as grid_file:
        grid_file.write(grid_data.grid)
        grid_file.flush()
        th = TreasureHunt(grid_file.name, 0, 0)
    assert th.state == 'STARTED'
    state = th.process_command('QUIT')
    assert (state if check_returned_state else th.state) == 'OVER'
