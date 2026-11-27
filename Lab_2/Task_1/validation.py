def validate_path(map, path, start, goal):

    if path is None:
        raise Exception("Error: no path found")

    # Check starting position
    if tuple(path[0]) != start:
        raise Exception("Error: Incorrect starting position")

    # Check goal position
    if tuple(path[-1]) != goal:
        raise Exception("Error: Incorrect goal position")

    # Check obstacles and movements
    for i in range(len(path)):

        x, y = path[i]

        # Check obstacle
        if map[x][y] == -1:
            raise Exception("Error: Path crosses an obstacle")

        # Check movement between consecutive positions
        if i > 0:
            previous = path[i - 1]

            distance = abs(x - previous[0]) + abs(y - previous[1])

            if distance != 1:
                raise Exception("Error: Invalid movement")

    print("Path is valid!")
    return True