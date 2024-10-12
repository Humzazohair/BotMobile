import time
import picar_4wd as fc
import heapq
from turn import turn_left, turn_right

# Global variables for the robot's current state
CAR_X = 50
CAR_Y = 99
GOAL_X = 75
GOAL_Y = 0
TIME_TO_MOVE = 1 / 22 # 1 cm per 22 seconds
CM_COUNTER = 99  # Count the number of centimeters moved
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
current_orientation = 'UP'  # Car starts facing up

# Works
class Node:
    def __init__(self, position, parent=None, g=0, h=0, f=0):
        self.position = position
        self.parent = parent
        self.g = g  # Cost from start to this node
        self.h = h  # Heuristic (estimated cost from this node to goal)
        self.f = f  # Total cost (g + h)

    def __lt__(self, other):
        return self.f < other.f
# Works
def heuristic(a, b, move, parent_position, grand_parent_position):
    """Calculate the Manhattan distance heuristic (L1 norm) between two points."""
    heuristic = abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    if(a == (CAR_Y, CAR_X + 1) or a == (CAR_Y, CAR_X - 1)): 
        return (heuristic + 1000)
    if grand_parent_position == None:
        return heuristic

    # current[0] = parent[0] + prev_move[0]
    move_causes_turn = False 
    prev_move = (parent_position[0] - grand_parent_position[0], parent_position[1] - grand_parent_position[1])
    if(prev_move != move):
        move_causes_turn = True

    if(move_causes_turn):
        heuristic += 50

    return heuristic

def is_valid_position(grid, position):
    """Check if a position is within bounds and not an obstacle."""
    y, x = position
    return 0 <= y < len(grid) and 0 <= x < len(grid[0]) and grid[y][x] == 0

# Works
def reconstruct_path(current_node):
    """Reconstruct the path by tracing back from the goal node to the start."""
    path = []
    while current_node is not None:
        path.append(current_node.position)
        current_node = current_node.parent
    return path[::-1]  

# Works
def run_a_star(grid, start, goal):
    """Perform the A* search to find the shortest path from start to goal on the grid."""
    open_list = []
    closed_list = set()
    start_node = Node(start, g=0, h=heuristic(start, goal, (0, 0), (start[0], start[1] - 1), None ), f=heuristic(start, goal, (0, 0), (start[0], start[1] - 1), None))
    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)
        if current_node.position == goal:
            return reconstruct_path(current_node)
        closed_list.add(current_node.position)

        for move in MOVES:
            neighbor_pos = (current_node.position[0] + move[0], current_node.position[1] + move[1])
            if not is_valid_position(grid, neighbor_pos) or neighbor_pos in closed_list:
                continue
            g = current_node.g + 1
            h = heuristic(neighbor_pos, goal, move, current_node.position, current_node.parent.position if current_node.parent else None)
            f = g + h
            neighbor_node = Node(neighbor_pos, parent=current_node, g=g, h=h, f=f)
            heapq.heappush(open_list, neighbor_node)

    return None  # Return None if there's no path to the goal

def path_to_moves(path):
    """Convert a list of coordinates (A* path) into a list of moves."""
    moves = []
    global current_orientation
    for i in range(len(path) - 1):
        current_pos = path[i]
        next_pos = path[i + 1]
        dy = next_pos[0] - current_pos[0]
        dx = next_pos[1] - current_pos[1]

        if dy == -1 and dx == 0:
            direction = 'UP'
        elif dy == 1 and dx == 0:
            direction = 'DOWN'
        elif dx == 1 and dy == 0:
            direction = 'RIGHT'
        elif dx == -1 and dy == 0:
            direction = 'LEFT'

        if direction != current_orientation:
            moves.append({'action': 'turn', 'direction': direction})
            current_orientation = direction

        moves.append({'action': 'move_forward', 'distance': 1})  # 1 cm per grid step

    current_orientation = 'UP'
    return moves

def turn_to_direction(target_direction):
    """Turn the car to face the target direction."""
    global current_orientation

    if current_orientation == target_direction:
        return  # No need to turn
    
    # Turn logic based on current and target orientations
    if current_orientation == 'UP':
        if target_direction == 'LEFT':
            turn_left()
        elif target_direction == 'RIGHT':
            turn_right()
        elif target_direction == 'DOWN':
            turn_right()
            turn_right()

    elif current_orientation == 'DOWN':
        if target_direction == 'LEFT':
            turn_right()
        elif target_direction == 'RIGHT':
            turn_left()
        elif target_direction == 'UP':
            turn_right()
            turn_right()

    elif current_orientation == 'LEFT':
        if target_direction == 'UP':
            turn_right()
        elif target_direction == 'DOWN':
            turn_left()
        elif target_direction == 'RIGHT':
            turn_right()
            turn_right()

    elif current_orientation == 'RIGHT':
        if target_direction == 'UP':
            turn_left()
        elif target_direction == 'DOWN':
            turn_right()
        elif target_direction == 'LEFT':
            turn_right()
            turn_right()

    fc.stop()
    current_orientation = target_direction

def move_in_path(move):
    """Executes a single move from the path."""
    global CAR_X, CAR_Y, CM_COUNTER, current_orientation

    print(current_orientation)
    if move['action'] == 'turn':
        target_direction = move['direction']
        turn_to_direction(target_direction)
        # print(f"Turned to {current_orientation}")
        
        # After turning, move forward 1 cm in the new direction
        time.sleep(1)
        fc.forward(1)
        time.sleep(TIME_TO_MOVE)  # Move 1 cm
        fc.stop()
        
        # Update car position
        if current_orientation == 'UP':
            CAR_Y -= 1
        elif current_orientation == 'DOWN':
            CAR_Y += 1
        elif current_orientation == 'LEFT':
            CAR_X -= 1
        elif current_orientation == 'RIGHT':
            CAR_X += 1

        # print(f"Moved forward 1 cm after turning, new position: {(CAR_X, CAR_Y)}, CM_COUNTER: {CM_COUNTER}")

    elif move['action'] == 'move_forward':
        fc.forward(1)
        time.sleep(TIME_TO_MOVE)  # Move 1 cm
        fc.stop()
        
        # Update car position
        if current_orientation == 'UP':
            CAR_Y -= 1
        elif current_orientation == 'DOWN':
            CAR_Y += 1
        elif current_orientation == 'LEFT':
            CAR_X -= 1
        elif current_orientation == 'RIGHT':
            CAR_X += 1

        
        # print(f"Moved forward 1 cm, new position: {(CAR_X, CAR_Y)}, CM_COUNTER: {CM_COUNTER}")