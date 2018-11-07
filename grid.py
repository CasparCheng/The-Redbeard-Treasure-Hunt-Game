"""Assignment 1 - Node and Grid

This module contains the Node and Grid classes.

Your only task here is to implement the methods
where indicated, according to their docstring.
Also complete the missing doctests.
"""

import functools
import sys
from container import PriorityQueue


@functools.total_ordering
class Node:
    """
    Represents a node in the grid. A node can be navigable
    (that is located in water)
    or it may belong to an obstacle (island).

    === Attributes: ===
    @type navigable: bool
       navigable is true if and only if this node represents a
       grid element located in the sea
       else navigable is false
    @type grid_x: int
       represents the x-coordinate (counted horizontally, left to right)
       of the node
    @type grid_y: int
       represents the y-coordinate (counted vertically, top to bottom)
       of the node
    @type parent: Node
       represents the parent node of the current node in a path
       for example, consider the grid below:
        012345
       0..+T..
       1.++.++
       2..B..+
       the navigable nodes are indicated by dots (.)
       the obstacles (islands) are indicated by pluses (+)
       the boat (indicated by B) is in the node with
       x-coordinate 2 and y-coordinate 2
       the treasure (indicated by T) is in the node with
       x-coordinate 3 and y-coordinate 0
       the path from the boat to the treasure if composed of the sequence
       of nodes with coordinates:
       (2, 2), (3,1), (3, 0)
       the parent of (3, 0) is (3, 1)
       the parent of (3, 1) is (2, 2)
       the parent of (2, 2) is of course None
    @type in_path: bool
       True if and only if the node belongs to the path plotted by A-star
       path search
       in the example above, in_path is True for nodes with coordinates
       (2, 2), (3,1), (3, 0)
       and False for all other nodes
    @type gcost: float
       gcost of the node, as described in the handout
       initially, we set it to the largest possible float
    @type hcost: float
       hcost of the node, as described in the handout
       initially, we set it to the largest possible float
    """

    def __init__(self, navigable, grid_x, grid_y):
        """
        Initialize a new node

        @type self: Node
        @type navigable: bool
        @type grid_x: int
        @type grid_y: int
        @rtype: None

        Preconditions: grid_x, grid_y are non-negative

        >>> n = Node(True, 2, 3)
        >>> n.grid_x
        2
        >>> n.grid_y
        3
        >>> n.navigable
        True
        """
        # initialize the navigable place
        self.navigable = navigable
        # initialize the x on the grid
        self.grid_x = grid_x
        # initialize the y on the grid
        self.grid_y = grid_y
        # intitialize the false bool for in path
        self.in_path = False
        # initialize the parent being none
        self.parent = None
        self.gcost = sys.float_info.max
        self.hcost = sys.float_info.max

    def set_gcost(self, gcost):
        """
        Set gcost to a given value

        @type gcost: float
        @rtype: None

        Precondition: gcost is non-negative

        >>> n = Node(True, 1, 2)
        >>> n.set_gcost(12.0)
        >>> n.gcost
        12.0
        """
        # set gcost
        self.gcost = gcost

    def set_hcost(self, hcost):
        """
        Set hcost to a given value

        @type hcost: float
        @rtype: None

        Precondition: gcost is non-negative

        >>> n = Node(True, 1, 2)
        >>> n.set_hcost(12.0)
        >>> n.hcost
        12.0
        """
        # set hcost
        self.hcost = hcost

    def fcost(self):
        """
        Compute the fcost of this node according to the handout

        @type self: Node
        @rtype: float

        >>> n = Node(True, 1, 2)
        >>> n.set_hcost(12.5)
        >>> n.set_gcost(21.5)
        >>> n.fcost()
        34.0
        """
        # get the total distance which means f-cost
        return self.gcost + self.hcost

    def set_parent(self, parent):
        """
        Set the parent to self
        @type self: Node
        @type parent: Node
        @rtype: None

        >>> n_child = Node(True, 1, 2)
        >>> n_parent = Node(True, 2, 3)
        >>> n_child.set_parent(n_parent)
        >>> print(n_child.parent.grid_x, n_child.parent.grid_y)
        2 3
        """
        # set parent
        self.parent = parent

    def distance(self, other):
        """
        Compute the distance from self to other
        @self: Node
        @other: Node
        @rtype: int

        >>> n_1 = Node(True, 1, 2)
        >>> n_2 = Node(True, 4, 3)
        >>> n_1.distance(n_2)
        34
        >>> n_3 = Node(True, 1, 2)
        >>> n_1.distance(n_3)
        0
        >>> n_4 = Node(True, 1, 10)
        >>> n_1.distance(n_4)
        80
        >>> n_5 = Node(True, 9, 2)
        >>> n_1.distance(n_5)
        80
        """
        # get the distance x
        dstx = abs(self.grid_x - other.grid_x)
        # get the distancce y
        dsty = abs(self.grid_y - other.grid_y)
        # if the distance of x is greater than the distance of y
        if dstx > dsty:
            # calculate the distance
            result = 14 * dsty + 10 * (dstx - dsty)
        else:
            # calculate the distance
            result = 14 * dstx + 10 * (dsty - dstx)
        return result

    def __eq__(self, other):
        """
        Return True if self equals other, and false otherwise.

        @type self: Node
        @type other: Node
        @rtype: bool

        >>> n_1 = Node(True, 1, 2)
        >>> n_2 = n_1
        >>> n_1 == n_2
        True
        >>> n_3 = Node(True, 1, 2)
        >>> n_1 == n_3
        True
        """
        # TODO
        return (
            self.grid_x == other.grid_x and
            self.grid_y == other.grid_y and
            self.navigable == self.navigable)

    def __lt__(self, other):
        """
        Return True if self less than other, and false otherwise.

        @type self: Node
        @type other: Node
        @rtype: bool
        >>> n_1 = Node(True, 1, 2)
        >>> n_1.set_hcost(12.5)
        >>> n_1.set_gcost(21.5)
        >>> n_2 = Node(True, 4, 1)
        >>> n_2.set_hcost(11.5)
        >>> n_2.set_gcost(22.5)
        >>> n_1 < n_2
        False
        >>> n_2.set_hcost(12.0)
        >>> n_1 < n_2
        True
        """
        # TODO
        # compare the f-cost between self and other
        return self.fcost() < other.fcost()

    def __str__(self):
        """
        Return a string representation.

        @type self: Node
        @rtype: str
        >>> n = Node(True, 0, 0)
        >>> print(n)
        .
        >>> n = Node(False, 1, 2)
        >>> print(n)
        +
        >>> n = Node(True, 3, 9)
        >>> n.set_hcost(13.2)
        >>> n.set_gcost(7.3)
        >>> print(n)
        .
        """
        # TODO
        # set the string for island
        string = '+'
        # if the island is navigable
        if self.navigable:
            # then the symbol is a dot
            string = '.'
        # otherwise
        else:
            # the symbol is '+'
            string = '+'
        return string


class Grid:
    """
    Represents the world where the action of the game takes place.
    You may define helper methods as you see fit.

    === Attributes: ===
    @type width: int
       represents the width of the game map in characters
       the x-coordinate runs along width
       the leftmost node has x-coordinate zero
    @type height: int
       represents the height of the game map in lines
       the y-coordinate runs along height; the topmost
       line contains nodes with y-coordinate 0
    @type map: List[List[Node]]
       map[x][y] is a Node with x-coordinate equal to x
       running from 0 to width-1
       and y-coordinate running from 0 to height-1
    @type treasure: Node
       a navigable node in the map, the location of the treasure
    @type boat: Node
       a navigable node in the map, the current location of the boat

    === Representation invariants ===
    - width and height are positive integers
    - map has dimensions width, height
    """

    def __init__(self, file_path, text_grid=None):
        """
        If text_grid is None, initialize a new Grid assuming file_path
        contains pathname to a text file with the following format:
        ..+..++
        ++.B..+
        .....++
        ++.....
        .T....+
        where a dot indicates a navigable Node, a plus indicates a
        non-navigable Node, B indicates the boat, and T the treasure.
        The width of this grid is 7 and height is 5.
        If text_grid is not None, it should be a list of strings
        representing a Grid. One string element of the list represents
        one row of the Grid. For example the grid above, should be
        stored in text_grid as follows:
        ["..+..++", "++.B..+", ".....++", "++.....", ".T....+"]

        @type file_path: str
           - a file pathname. See the above for the file format.
           - it should be ignored if text_grid is not None.
           - the file specified by file_path should exists, so there
             is no need for error handling
           Please call open_grid to open the file
        @type text_grid: List[str]
        @rtype: None
        """
        # TODO
        # if the text_grid is not none
        if not text_grid:
            # open the grid file path
            text_grid = self.open_grid(file_path).readlines()
        # create an empty list
        _map = []
        # loop the element in the grid with index
        for y, row in enumerate(text_grid):
            # create an empty list for row
            map_row = []
            # loop the element in the row with index
            for x, sym in enumerate(row):
                # if the symbol is plus
                if sym == '+':
                    # add the node as false to the row
                    map_row.append(Node(False, x, y))
                # else if the symbol is not plus
                elif sym in ('.', 'B', 'T'):
                    # add the node as true to the row
                    map_row.append(Node(True, x, y))
                    # if the symbol is B
                    if sym == 'B':
                        self.boat = map_row[-1]
                    # else if the symbol is T
                    elif sym == 'T':
                        self.treasure = map_row[-1]
            # add the row in the map
            _map.append(map_row)
        self.map = list(list(x) for x in zip(*_map))
        # get the wide length of the map
        self.width = len(self.map)
        # get the height of the map
        self.height = len(self.map[0])

    @classmethod
    def open_grid(cls, file_path):
        """
        @rtype: TextIOWrapper
        """
        # open the path file
        return open(file_path)

    def __str__(self):
        """
        Return a string representation.

        @type self: Grid
        @rtype: str

        >>> g = Grid("", ["B.++", ".+..", "...T"])
        >>> print(g)
        B.++
        .+..
        ...T
        """
        # TODO
        # create an empty list for strings
        strings = []
        # get the map list which is zipped
        _map = list(zip(*self.map))
        # loop the row in the map
        for row in _map:
            # create an empty string
            string = ''
            # loop the node on the row
            for node in row:
                # if the node is not navigable
                if not node.navigable:
                    # add the plus symbol to the string
                    string += '+'
                # otherwise
                else:
                    # if the node is the boat
                    if node is self.boat:
                        # add the B to the string
                        string += 'B'
                    # else if the node is the treasure
                    elif node is self.treasure:
                        # add the T to the big string
                        string += 'T'
                    # otherwise
                    else:
                        # add the dot symbol to the big string
                        string += '.'
            # add the string to the list of string
            strings.append(string)
        return '\n'.join(strings)

    def move(self, direction):
        """
        Move the boat in a specific direction, if the node
        corresponding to the direction is navigable
        Else do nothing

        @type self: Grid
        @type direction: str
        @rtype: None

        direction may be one of the following:
        N, S, E, W, NW, NE, SW, SE
        (north, south, ...)
        123
        4B5
        678
        1=NW, 2=N, 3=NE, 4=W, 5=E, 6=SW, 7=S, 8=SE
        >>> g = Grid("", ["B.++", ".+..", "...T"])
        >>> g.move("S")
        >>> print(g)
        ..++
        B+..
        ...T
        """
        # TODO
        # define x for the boat on the grid-x
        x = self.boat.grid_x
        # define y for the boat on the grid-y
        y = self.boat.grid_y
        # if the direction is north
        if direction == 'N':
            # if the y is greater than 0, and the island is navigale on
            # this index
            if y > 0 and self.map[x][y - 1].navigable:
                # let boat come to that position
                self.boat = self.map[x][y - 1]
        # else if the direction is south
        elif direction == 'S':
            # if y is less than the height - 1, and the island is navigable on
            # this index
            if y < self.height - 1 and self.map[x][y + 1].navigable:
                # let boat come to that position
                self.boat = self.map[x][y + 1]

        # else if the direction is east
        elif direction == 'E':
            # if x is less than the wide length - 1, and the island is
            # navigable on this index
            if x < self.width - 1 and self.map[x + 1][y].navigable:
                # let boat come to that position
                self.boat = self.map[x + 1][y]
        # else if the direction is west
        elif direction == 'W':
            # if the x is greater than 0, and the island is navigale on
            # this index
            if x > 0 and self.map[x - 1][y].navigable:
                # let boat come to that position
                self.boat = self.map[x - 1][y]
        # else if the direction is northwest
        elif direction == 'NW':
            # if y and x both greater than 0, and the island is navigale on
            # this index
            if y > 0 and x > 0 and self.map[x - 1][y - 1].navigable:
                # let boat come to that position
                self.boat = self.map[x - 1][y - 1]
        # else if the direction is northeast
        elif direction == 'NE':
            # if y is greater than0, x is less than the wide length of map
            # and the island is navigable on this index
            if (y > 0 and x < self.width - 1 and
                    self.map[x + 1][y - 1].navigable):
                # let boat come to that position
                self.boat = self.map[x + 1][y - 1]
        # else if the direction is southwest
        elif direction == 'SW':
            # if y is less than height - 1, x is greater than 0
            # and the island is navigable on this index
            if (y < self.height - 1 and x > 0 and
                    self.map[x - 1][y + 1].navigable):
                # let boat come to that position
                self.boat = self.map[x - 1][y + 1]
        # else if the direction is southeast
        elif direction == 'SE':
            # if y is less than height - 1, x is less than wide length
            # and the island is navigable on this index
            if (y < self.height - 1 and x < self.width - 1 and
                    self.map[x + 1][y + 1].navigable):
                # let boat come to that position
                self.boat = self.map[x + 1][y + 1]
        else:
            pass

    def get_neighours(self, node):
        """
        Find the neighours of the input node
        @type self: Grid
        @type node: Node
            the node to be found the neighours of
        @rtype: list[Node]
            the neighours of the input node

        >>> g = Grid("", ["B.++", ".+..", "...T"])
        >>> n = g.map[1][0]
        >>> ns = g.get_neighours(n)
        >>> print(len(ns))
        3
        >>> for n in ns:
        ...     print(n.grid_x, n.grid_y)
        0 0
        2 1
        0 1
        >>> n = g.map[3][2]
        >>> ns = g.get_neighours(n)
        >>> print(len(ns))
        3
        >>> for n in ns:
        ...     print(n.grid_x, n.grid_y)
        3 1
        2 2
        2 1
        >>> n = g.map[1][1]
        >>> ns = g.get_neighours(n)
        >>> print(len(ns))
        7
        >>> for n in ns:
        ...     print(n.grid_x, n.grid_y)
        1 2
        1 0
        2 1
        0 1
        2 2
        0 2
        0 0
        """
        # deifne x as the node on the grid-x
        x = node.grid_x
        # difine y as the node on the grid-y
        y = node.grid_y
        # create an empty list as neighours
        neighours = []
        # loop the tuple of y and x in these tuple
        for delta_y, delta_x in ((1, 0), (-1, 0), (0, 1), (0, -1),
                                 (1, 1), (1, -1), (-1, 1), (-1, -1)):
            # get the new-x
            new_x = x + delta_x
            # get the new-y
            new_y = y + delta_y
            # if the new y is greater than -1 and less than height
            # and the new x is greater than -1 and less than the wide
            if -1 < new_y < self.height and -1 < new_x < self.width:
                # define the map of new x and new y as current node
                curr_node = self.map[new_x][new_y]
                # if the current node is navigable
                if curr_node.navigable:
                    # add the current node to the list of neighours
                    neighours.append(curr_node)
        return neighours

    def find_path(self, start_node, target_node):
        """
        Implement the A-star path search algorithm
        If you will add a new node to the path, don't forget to set the parent.
        You can find an example in the docstring of Node class
        Please note the shortest path between two nodes may not be unique.
        However all of them have same length!

        @type self: Grid
        @type start_node: Node
           The starting node of the path
        @type target_node: Node
           The target node of the path
        @rtype: None

        >>> g = Grid("", ["B.++", ".+..", "...T"])
        >>> g.find_path(g.boat, g.treasure)
        >>> n = g.treasure
        >>> print(n.grid_x, n.grid_y,
        ...     n.gcost, n.hcost, n.fcost(),
        ...     n.parent.grid_x, n.parent.grid_y)
        3 2 38 0 38 2 1
        >>> n = g.treasure.parent
        >>> print(n.grid_x, n.grid_y,
        ...     n.gcost, n.hcost, n.fcost(),
        ...     n.parent.grid_x, n.parent.grid_y)
        2 1 24 14 38 1 0
        >>> n = g.map[1][0]
        >>> print(n.grid_x, n.grid_y,
        ...     n.gcost, n.hcost, n.fcost(),
        ...     n.parent.grid_x, n.parent.grid_y)
        1 0 10 28 38 0 0
        >>> n = g.map[0][1].parent
        >>> n == g.boat
        True
        """
        # TODO
        def less_than(x_node, y_node):
            """
            Compare the priority of x over y
            @type x_node: Node
            @type y_node: Node
            @rtype: bool
                True if x has higher priority over y otherwise False
            """
            return x_node < y_node
        # create an empty list as open set
        open_set = []
        # loop the row on the map
        for row in self.map:
            # extend the row in the list
            open_set.extend(row)
        # remove the start node from the list
        open_set.remove(start_node)
        # define a closed set as the priority queue in less_than
        closed_set = PriorityQueue(less_than)
        # add the start node to the list of closed set
        closed_set.add(start_node)
        # set the gcost for start node
        start_node.set_gcost(0)
        # loop the closed set if it is not empty
        while not closed_set.is_empty():
            # get the current node from the closed set
            curr_node = closed_set.remove()
            # if the current node is the target node
            if curr_node is target_node:
                # done
                break
            # loop the next node in the neighours for current node
            for next_node in self.get_neighours(curr_node):
                # if the next node is in the open set
                if next_node in open_set:
                    # remove the next node
                    open_set.remove(next_node)
                    # add it to the closed set
                    closed_set.add(next_node)
                    # set the gcost for the next node
                    next_node.set_gcost(
                        curr_node.gcost + curr_node.distance(next_node))
                    # set the hcost for the next_node
                    next_node.set_hcost(
                        next_node.distance(target_node))
                    # set the parent for the next node
                    next_node.set_parent(curr_node)

    def retrace_path(self, start_node, target_node):
        """
        Return a list of Nodes, starting from start_node,
        ending at target_node, tracing the parent
        Namely, start from target_node, and add its parent
        to the list. Keep going until you reach the start_node.
        If the chain breaks before reaching the start_node,
        return an empty list.

        @type self: Grid
        @type start_node: Node
        @type target_node: Node
        @rtype: list[Node]

        >>> g = Grid("", ["B.++", ".+..", "...T"])
        >>> g.find_path(g.boat, g.treasure)
        >>> path = g.retrace_path(g.boat, g.treasure)
        >>> for n in path:
        ...     print(n.grid_x, n.grid_y,
        ...         n.gcost, n.hcost, n.fcost(),
        ...         n.in_path)
        0 0 0 1.7976931348623157e+308 1.7976931348623157e+308 True
        1 0 10 28 38 True
        2 1 24 14 38 True
        3 2 38 0 38 True
        """
        # TODO
        # define the path as the list of target node
        path = [target_node]
        # define the target node as the current node
        curr_node = target_node
        # set the default bool is not found
        is_found = False
        # loop the current node exist
        while curr_node.parent:
            # define the parent as the current node
            curr_node = curr_node.parent
            # add the current node to the path
            path.append(curr_node)
            # if the current node is the start node
            if curr_node is start_node:
                # it is found
                is_found = True
                # done
                break
        # if it is found
        if is_found:
            # reverse the path
            path.reverse()
            # loop the node in the path
            for node in path:
                # the node is in the path
                node.in_path = True
        # otherwise
        else:
            # the path is empty list
            path = []

        return path

    def get_treasure(self, s_range):
        """
        Return treasure node if it is located at a distance s_range or
        less from the boat, else return None
        @type s_range: int
        @rtype: Node, None

        >>> g = Grid("", ["B.++", ".+..", "...T"])
        >>> dist = g.boat.distance(g.treasure)
        >>> print(dist)
        38
        >>> print(g.get_treasure(dist - 1))
        None
        >>> n = g.get_treasure(dist)
        >>> print(n.grid_x, n.grid_y)
        3 2
        >>> n = g.get_treasure(dist + 1)
        >>> print(n.grid_x, n.grid_y)
        3 2
        """
        # TODO
        # if the distance between the boat and the treasure is less or equal
        # than the range of sonar
        if self.boat.distance(self.treasure) <= s_range:
            # get the treasure
            return self.treasure

    def plot_path(self, start_node, target_node):
        """
        Return a string representation of the grid map,
        plotting the shortest path from start_node to target_node
        computed by find_path using "*" characters to show the path
        @type self: Grid
        @type start_node: Node
        @type target_node: Node
        @rtype: str
        >>> g = Grid("", ["B.++", ".+..", "...T"])
        >>> print(g.plot_path(g.boat, g.treasure))
        B*++
        .+*.
        ...T
        """
        # TODO
        # call the find_path function
        self.find_path(start_node, target_node)
        # get the nodes on the path
        path_nodes = self.retrace_path(start_node, target_node)
        # create an empty list of strings
        strings = []
        # zip the map
        _map = zip(*self.map)
        # loop the row in the map
        for row in _map:
            # create an empty string
            string = ''
            # loop the node in the row
            for node in row:
                # if the node is not navigable
                if not node.navigable:
                    # add the plus symbol to the big string
                    string += '+'
                # otherwise
                else:
                    # if the node is the boat
                    if node is self.boat:
                        # add B to the big string
                        string += 'B'
                    # else if the node is the treasure
                    elif node is self.treasure:
                        # add T to the bug string
                        string += 'T'
                    # else if the node is in the path of nodes
                    elif node in path_nodes:
                        # add star symbol to the big string
                        string += '*'
                    # otherwise
                    else:
                        # it is not navigable, and add the dot to the string
                        string += '.'
            # add the big string to the list of strings
            strings.append(string)
        return '\n'.join(strings)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    import python_ta
    python_ta.check_all(config='pylintrc.txt')
