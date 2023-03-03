import heapq

# Define the goal state
goal_state = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

# Define the heuristic function (Manhattan distance)
def heuristic(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                x, y = divmod(state[i][j] - 1, 3)
                distance += abs(x - i) + abs(y - j)
    return distance

# Define the Greedy Best First Search algorithm
def greedy_best_first_search(start_state):
    heap = []
    heapq.heappush(heap, (heuristic(start_state), start_state))
    visited = set()
    while heap:
        _, state = heapq.heappop(heap)
        if state == goal_state:
            return state
        visited.add(str(state))
        for neighbor in get_neighbors(state):
            if str(neighbor) not in visited:
                heapq.heappush(heap, (heuristic(neighbor), neighbor))

# Define the function to get the neighbors
def get_neighbors(state):
    neighbors = []
    row, col = find_blank(state)
    if row > 0:
        new_state = [row[:] for row in state]
        new_state[row][col], new_state[row - 1][col] = new_state[row - 1][col], new_state[row][col]
        neighbors.append(new_state)
    if row < 2:
        new_state = [row[:] for row in state]
        new_state[row][col], new_state[row + 1][col] = new_state[row + 1][col], new_state[row][col]
        neighbors.append(new_state)
    if col > 0:
        new_state = [row[:] for row in state]
        new_state[row][col], new_state[row][col - 1] = new_state[row][col - 1], new_state[row][col]
        neighbors.append(new_state)
    if col < 2:
        new_state = [row[:] for row in state]
        new_state[row][col], new_state[row][col + 1] = new_state[row][col + 1], new_state[row][col]
        neighbors.append(new_state)
    return neighbors

# Define the function to find the blank tile
def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

# Define the main function
def main():
    start_state = [[7, 2, 4], [5, 0, 6], [8, 3, 1]]
    goal = greedy_best_first_search(start_state)
    print("Goal state:")
    for state in goal:
        print(state)
    print("Total Jarak:", heuristic(goal))

if __name__ == "__main__":
    main()
