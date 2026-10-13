from pyamaze import maze, agent, COLOR, textLabel
from queue import PriorityQueue

def h(cell1, cell2):
    """
    Calculate Manhattan distance between two cells as a heuristic.
    """
    return abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])

def aStar(m):
    """
    Implement A* search algorithm using pyamaze library.
    """
    start = (m.rows, m.cols)
    
    g_score = {cell: float('inf') for cell in m.grid}
    g_score[start] = 0
    
    f_score = {cell: float('inf') for cell in m.grid}
    f_score[start] = h(start, (1, 1))
    
    open_p = PriorityQueue()
    open_p.put((f_score[start], h(start, (1, 1)), start))
    
    a_path = {}
    
    while not open_p.empty():
        current = open_p.get()[2]
        
        if current == (1, 1):
            break
            
        for d in 'ESNW':
            if m.maze_map[current][d] == True:
                if d == 'E':
                    child = (current[0], current[1] + 1)
                elif d == 'W':
                    child = (current[0], current[1] - 1)
                elif d == 'S':
                    child = (current[0] + 1, current[1])
                elif d == 'N':
                    child = (current[0] - 1, current[1])
                    
                temp_g_score = g_score[current] + 1
                
                if temp_g_score < g_score[child]:
                    g_score[child] = temp_g_score
                    f_score[child] = temp_g_score + h(child, (1, 1))
                    open_p.put((f_score[child], h(child, (1, 1)), child))
                    a_path[child] = current
                    
    forward_path = {}
    cell = (1, 1)
    while cell != start:
        forward_path[a_path[cell]] = cell
        cell = a_path[cell]
        
    return forward_path

if __name__ == '__main__':
    my_maze = maze(20, 20)
    my_maze.CreateMaze()
    
    path = aStar(my_maze)
    
    a = agent(my_maze, x=my_maze.rows, y=my_maze.cols, footprints=True, color=COLOR.red)
    textLabel(my_maze, 'A* Path Length', len(path) + 1)
    
    my_maze.tracePath({a: path}, delay=300)
    my_maze.run()