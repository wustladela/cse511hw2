def manhattanDist(point1, point2):
    "The Manhattan distance for two positions"
    x1 = point1[0]
    x2 = point2[0]
    y1 = point1[1]
    y2 = point2[0]
    return abs(x1 - x2) + abs(y1 - y2)
