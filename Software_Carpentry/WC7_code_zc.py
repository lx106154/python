'''
EN.540.635 Software Carpentry
Weekly Challenge 7 - Maze Generation and Solving
'''
from PIL import Image
import random
import collections


def get_colors():
    '''
    Colors map that the maze will use:
        0 - Black - A wall
        1 - White - A space to travel in the maze
        2 - Green - A valid solution of the maze
        3 - Red - A backtracked position during maze solving
        4 - Blue - Start and Endpoints of the maze

    **Returns**

        color_map: *dict, int, tuple*
            A dictionary that will correlate the integer key to
            a color.
    '''
    return {
        0: (0, 0, 0),
        1: (255, 255, 255),
        2: (0, 255, 0),
        3: (255, 0, 0),
        4: (0, 0, 255),
    }


def save_maze(maze, blockSize=10, name="maze"):
    '''
    This will save a maze object to a file.

    **Parameters**

        maze: *list, list, int*
            A list of lists, holding integers specifying the different aspects
            of the maze:
                0 - Black - A wall
                1 - White - A space to travel in the maze
                2 - Green - A valid solution of the maze
                3 - Red - A backtracked position during maze solving
                4 - Blue - Start and Endpoints of the maze
        blockSize: *int, optional*
            How many pixels each block is comprised of.
        name: *str, optional*
            The name of the maze.png file to save.

    **Returns**

        None
    '''
    nBlocks = len(maze)
    dims = nBlocks * blockSize
    colors = get_colors()
    # Verify that all values in the maze are valid colors.
    ERR_MSG = "Error, invalid maze value found!"
    assert all([x in colors.keys() for row in maze for x in row]), ERR_MSG
    img = Image.new("RGB", (dims, dims), color=0)
    # Parse "maze" into pixels
    for jx in range(nBlocks):
        for jy in range(nBlocks):
            x = jx * blockSize
            y = jy * blockSize
            for i in range(blockSize):
                for j in range(blockSize):
                    img.putpixel((x + i, y + j), colors[maze[jx][jy]])
    if not name.endswith(".png"):
        name += ".png"
    img.save("%s" % name)


def load_maze(filename, blockSize=10):
    '''
    This will read a maze from a png file into a 2d list with values
    corresponding to the known color dictionary.

    **Parameters**

        filename: *str*
            The name of the maze.png file to load.
        blockSize: *int, optional*
            How many pixels each block is comprised of.

    **Returns**

        maze: *list, list, int*
            A 2D array holding integers specifying each block's color.
    '''
    if ".png" in filename:
        filename = filename.split(".png")[0]
    img = Image.open(filename + ".png")
    dims, _ = img.size
    nBlocks = int(dims / blockSize)
    colors = get_colors()
    color_map = {v: k for k, v in colors.items()}
    maze = [[0 for x in range(nBlocks)] for y in range(nBlocks)]
    # Parse pixels into the maze array
    for i, x in enumerate(range(0, dims, dims // nBlocks)):
        for j, y in enumerate(range(0, dims, dims // nBlocks)):
            px = x
            py = y
            maze[i][j] = color_map[img.getpixel((px, py))]
    return maze


def pos_chk(x, y, nBlocks):
    '''
    Validate if the coordinates specified (x and y) are within the maze.

    **Parameters**

        x: *int*
            An x coordinate to check if it resides within the maze.
        y: *int*
            A y coordinate to check if it resides within the maze.
        nBlocks: *int*
            How many blocks wide the maze is.  Should be equivalent to
            the length of the maze (ie. len(maze)).

    **Returns**

        valid: *bool*
            Whether the coordiantes are valid (True) or not (False).
    '''
    return x >= 0 and x < nBlocks and y >= 0 and y < nBlocks


def generate_maze(nBlocks, name="maze", start=(0, 0), blockSize=10,
                  slow=False):
    '''
    Generate a maze using the Depth First Search method.

    **Parameters**

        nBlocks: *int*
            The number of blocks in the maze (x and y dims are the same).
        name: *str, optional*
            The name of the output maze.png file.
        start: *tuple, int, optional*
            Where the maze will start from, and the initial direction.
        blockSize: *int, optional*
            How many pixels each block will be.
        slow: *bool, optional*
            Whether to save and lag on generation so as to view the mazegen.

    **Returns**

        None
    '''

    def _get_neighbors(x, y):
        cand = list(filter(
            lambda n: pos_chk(n[0], n[1], nBlocks),
            [
                (x - 1, y),
                (x + 1, y),
                (x, y - 1),
                (x, y + 1)
            ]))
        return cand

    def _is_valid(x, y):
        nbs = _get_neighbors(x, y)
        num_blanks = len(list(filter(lambda n: maze[n[0]][n[1]] == 1, nbs)))
        return num_blanks <= 2 if (
                    (x, y) == (nBlocks - 1, nBlocks - 2) or (x, y) == (nBlocks - 2, nBlocks - 1)) else num_blanks == 1

    maze = [[0 for _ in range(nBlocks)] for _ in range(nBlocks)]
    maze[0][0] = 1
    maze[nBlocks - 1][nBlocks - 1] = 1

    slow_count = 0
    visited = set()
    stack = collections.deque()
    stack.append(start)
    while stack:
        curr_node = stack.pop()
        visited.add(curr_node)
        next_nodes = list(filter(lambda n: (n[0], n[1]) not in visited and _is_valid(n[0], n[1]), _get_neighbors(curr_node[0], curr_node[1])))
        if len(next_nodes) > 0:
            rand_id = random.randrange(0, len(next_nodes), 1)
            # stack.append(curr_node)
            for i, node in enumerate(next_nodes):
                # visited.add(node)
                if i != rand_id:
                    stack.append(node)
            stack.append(next_nodes[rand_id])
            visited.add(next_nodes[rand_id])
            maze[next_nodes[rand_id][0]][next_nodes[rand_id][1]] = 1
        if slow:
            slow_name = name + '_' + str(slow_count)
            save_maze(maze, name=slow_name, blockSize=blockSize)
            slow_count += 1

    maze[0][0] = 4
    maze[nBlocks - 1][nBlocks - 1] = 4
    save_maze(maze, name=name, blockSize=blockSize)


def solve_maze(filename, start=(0, 0), end=(49, 49), blockSize=10, slow=False):
    '''
    Solve a maze using the Depth First Search method.

    **Parameters**

        filename: *str*
            The name of the maze.png file to be solved.
        start: *tuple, int, optional*
            Where the maze will start from.
        end: *tuple, int, optional*
            Where the maze will end.
        blockSize: *int, optional*
            How many pixels each block will be.
        slow: *bool, optional*
            Whether to save and lag on generation so as to view the mazegen.

    **Returns**

        None
    '''
    maze = load_maze(filename=filename, blockSize=blockSize)
    nBlocks = len(maze)

    def _get_neighbors(x, y):
        cand = list(filter(
            lambda n: pos_chk(n[0], n[1], nBlocks),
            [
                (x - 1, y),
                (x + 1, y),
                (x, y - 1),
                (x, y + 1)
            ]))
        return cand

    def _is_valid(x, y):
        nbs = _get_neighbors(x, y)
        return 1 in [maze[n[0]][n[1]] for n in nbs]

    maze[start[0]][start[1]] = 1
    maze[end[0]][end[1]] = 1

    slow_count = 0
    visited = set()
    path = collections.deque()
    stack = collections.deque()
    stack.append(start)
    while stack[0] != end:
        curr_node = stack.pop()
        visited.add(curr_node)
        next_nodes = list(filter(lambda n: (n[0], n[1]) not in visited and maze[n[0]][n[1]] == 1, _get_neighbors(curr_node[0], curr_node[1])))
        if len(next_nodes) > 0:
            rand_id = random.randrange(0, len(next_nodes), 1)
            maze[curr_node[0]][curr_node[1]] = 2
            stack.append(next_nodes[rand_id])
            path.append(next_nodes[rand_id])
            visited.add(next_nodes[rand_id])
        else:
            maze[curr_node[0]][curr_node[1]] = 3
            stack.append(path.pop())
        if slow:
            slow_name = filename + '_solved_' + str(slow_count)
            save_maze(maze, name=slow_name, blockSize=blockSize)
            slow_count += 1

    maze[0][0] = 4
    maze[nBlocks - 1][nBlocks - 1] = 4
    save_maze(maze, name=filename+'_solved', blockSize=blockSize)


if __name__ == "__main__":
    generate_maze(50, name="maze", start=(0, 0), blockSize=10, slow=False)
    solve_maze("maze", start=(0, 0), end=(49, 49), blockSize=10, slow=False)
