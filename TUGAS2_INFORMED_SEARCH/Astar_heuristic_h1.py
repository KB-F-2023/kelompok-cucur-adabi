import heapq

# Define the goal state
goal_state = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

# Define the heuristic function
def heuristic(state):
    count = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != goal_state[i][j] and state[i][j] != 0:
                count += 1
    return count

# Define the A* algorithm
def A_star(start_state):
    heap = []
    heapq.heappush(heap, (heuristic(start_state), start_state, 0, None))
    visited = set()
    while heap:
        f, state, g, prev = heapq.heappop(heap)
        if state == goal_state:
            path = [(state, g)]
            while prev:
                path.append(prev)
                state, g, prev = prev
            path.reverse()
            return path
        visited.add(str(state))
        for neighbor in get_neighbors(state):
            if str(neighbor) not in visited:
                new_g = g + 1
                heapq.heappush(heap, (new_g + heuristic(neighbor), neighbor, new_g, (state, g, prev)))

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
    path = A_star(start_state)
    for state in path:
        print(state)
        print()
    print("Jumlah kotak yang salah letaknya:", heuristic(start_state))

if __name__ == "__main__":
    main()
