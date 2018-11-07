import random
from collections import namedtuple
from textwrap import dedent

DIRECTIONS = [
    # (1, -1, -1),
    ('NW', -1, -1),
    # (2, 0, -1),
    ('N', 0, -1),
    # (3, 1, -1),
    ('NE', 1, -1),
    # (4, -1, 0),
    ('W', -1, 0),
    # (5, 1, 0),
    ('E', 1, 0),
    # (6, -1, 1),
    ('SW', -1, 1),
    # (7, 0, 1),
    ('S', 0, 1),
    # (8, 1, 1),
    ('SE', 1, 1),
]

GridData = namedtuple("Grid", "grid, grid_solutions, cost, winning_commands, losing_commands")


def grid_0():
    grid = dedent("""\
        ..+..++
        ++.B..+
        .....++
        ++.....
        .T....+
    """)
    grid_solutions = [
        dedent("""\
            ..+..++
            ++.B..+
            ..*..++
            ++*....
            .T....+
        """),
        dedent("""\
            ..+..++
            ++.B..+
            ...*.++
            ++*....
            .T....+
        """),
    ]
    cost = 38
    winning_commands = [
        ['GO SW', 'GO S', 'GO SW'],
        ['GO S', 'GO SW', 'GO SW'],
    ]
    losing_commands = [['GO S', 'GO S', 'GO S', 'GO S']]
    return GridData(grid, grid_solutions, cost, winning_commands, losing_commands)


def grid_1():
    grid = dedent("""\
        B+T
        .+.
        .+.
        .+.
        .+.
        ...
    """)
    grid_solution = dedent("""\
        B+T
        *+*
        *+*
        *+*
        *+*
        .*.
    """)
    cost = 110
    winning_commands = [['GO S'] * 4 + ['GO SE', 'GO NE'] + ['GO N'] * 4]
    losing_commands = [['GO S', 'GO S', 'GO S', 'GO S']]
    return GridData(grid, [grid_solution], cost, winning_commands, losing_commands)


def grid_2():
    grid = [['.'] * 100 for _ in range(100)]
    grid[0][0] = 'B'
    grid[-1][-1] = 'T'
    grid_solution = [l[:] for l in grid]
    for i in range(1, len(grid_solution) - 1):
        grid_solution[i][i] = '*'
    cost = 14 * 98
    winning_commands = [['GO SE'] * 99]
    directions = [d for d in next(zip(*DIRECTIONS)) if isinstance(d, str)]
    losing_commands = [[
        'GO {}'.format(random.choice(directions)) for _ in range(random.randrange(5, 500))
    ] for _ in range(5)]
    losing_commands = filter(lambda x: x != winning_commands, losing_commands)
    return GridData('\n'.join(''.join(l) for l in grid) + '\n',
                    ['\n'.join(''.join(l) for l in grid_solution) + '\n'], cost, winning_commands,
                    losing_commands)


GRID_TEST_DATA = [grid_0(), grid_1(), grid_2()]
