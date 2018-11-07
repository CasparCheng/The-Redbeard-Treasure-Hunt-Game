"""Assignment 1 - TreasureHunt

This module contains the TreasureHunt class.

Your only task here is to implement the methods
where indicated, according to their docstring.
Also complete the missing doctests.
"""
from grid import Grid


class TreasureHunt:
    """
    Represents an instance of the treasure hunt game.

    === Attributes: ===
    @type grid_path: str
        pathname to a text file that contains the grid map
        see Grid and Node classes for the format
    @type grid: Grid
        a representation of the game world
    @type sonars: int
        the number of sonars the boat can drop
    @type so_range: int
        the range of sonars
    @type state: str
        the state of the game:
          STARTED, OVER, WON
    """

    def __init__(self, grid_path, sonars, so_range):
        """
        Initialize a new game with map data stored in the file grid_path
        and commands to be used to play the game in game_path file.

        @type grid_path: str
           pathname to a text file that contains the grid map
           see Grid and Node classes for the format
        @type sonars: int
        @type so_range: int
        """
        # TODO
        # initialize the grid path
        self.grid_path = grid_path
        # intitialize the Grid
        self.grid = Grid(grid_path)
        # initialize the sonars
        self.sonars = sonars
        # initialize the range of sonar
        self.so_range = so_range
        # set the started
        self.state = 'STARTED'
        # initialize the remainning sonars
        self._remaining_sonars = sonars
        # initialize the scannde treasure as false
        self._treasure_scanned = False

    def process_command(self, command):
        """
        Process a command, set and return the state of the game
        after processing this command
        @type command: str
           a command that can be used to play, as follows:
           GO direction, where direction=N,S,E,W,NW,NE,SW,SE
           SONAR, drops a sonar
           PLOT, plots the shortest path from the boat to the treasure
           (on condition the SONAR has discovered the treasure and
           the optimal Path has already been determined)
           QUIT, quit the game
        @rtype: str
           the state of the game

        >>> th = TreasureHunt('grid.txt', 3, 38)
        >>> th.process_command('GO N')
        'STARTED'
        >>> th.process_command('GO E')
        'STARTED'
        >>> th.process_command('GO E')
        'STARTED'
        >>> th.process_command('GO N')
        'STARTED'
        >>> th.process_command('GO S')
        'STARTED'
        >>> print(th.grid)
        ..+..++
        ++..B.+
        .....++
        ++.....
        .T....+
        >>> th.grid.boat.distance(th.grid.treasure)
        42
        >>> th.process_command('SONAR')
        'STARTED'
        >>> th.process_command('GO S')
        'STARTED'
        >>> th.grid.boat.distance(th.grid.treasure)
        38
        >>> th.process_command('SONAR')
        'STARTED'
        >>> th.process_command('GO W')
        'STARTED'
        >>> th.process_command('GO SW')
        'STARTED'
        >>> th.process_command('GO SW')
        'WON'
        >>> th = TreasureHunt('grid.txt', 3, 38)
        >>> th.process_command('SONAR')
        'STARTED'
        >>> th.process_command('SONAR')
        'STARTED'
        >>> th.process_command('SONAR')
        'OVER'
        """
        # TODO
        # if the command start with GO
        if command.startswith('GO'):
            # get the direction from the command
            direction = command[3:]
            # start the moving on the grid for the direction
            self.grid.move(direction)
            # if the boat on the grid is equal to the treasure on the grid
            if self.grid.boat == self.grid.treasure:
                # if the state is started
                if self.state == 'STARTED':
                    # then the state changes to WON
                    self.state = 'WON'
        # else if the command is SONAR
        elif command == 'SONAR':
            # if the remaining sonar is zero
            if self._remaining_sonars == 0:
                # then the sonars is none
                self.state = 'run out of sonars!'
            # otherwise
            else:
                # lose one sonar
                self._remaining_sonars -= 1
                # if the treasure is scanned
                if not self._treasure_scanned:
                    # if the treasure in the sonar range is not none
                    if self.grid.get_treasure(self.so_range) is not None:
                        # the treasure is found
                        self._treasure_scanned = True
                # if there is no remaining sonars
                if self._remaining_sonars == 0:
                    # if the state is STARTED
                    if self.state == 'STARTED':
                        # the state changes to OVER
                        self.state = 'OVER'
        # else if the command is QUIT
        elif command == 'QUIT':
            self.state = 'OVER'
        # otherwise the command is unsupported
        else:
            self.state = 'unsupported command!'

        return self.state


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    import python_ta
    python_ta.check_all(config='pylintrc.txt')
