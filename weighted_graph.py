import cv2
import numpy as np
import heapq

def imageread(image, block_size = 10):

    height, width, _ = image.shape
    # block_size = 10
    height, width = parsePoint(height, width, block_size)
    

    average_weights = {}

    for y in range(block_size//2, height, block_size):
        for x in range(block_size//2, width, block_size):
            block = image[y:y+block_size, x:x+block_size]
            green_channel = block[:,:,1]
            red_channel = block[:,:,2]
            avg_weight = np.mean(green_channel)
            normalized_weight = 1 - round(avg_weight / 255.0, 2)

            if np.mean(red_channel) > np.mean(green_channel):
                normalized_weight = "inf"

            average_weights[(x,y)] = normalized_weight

    return height, width, block_size, average_weights

def dijkstra(start, end, nodes, gridsize):
    # Priority queue for Dijkstra's algorithm
    pq = [(0, start)]  # (cost, node)
    distances = {coord: float('inf') for coord in nodes}
    distances[start] = 0
    previous = {coord: None for coord in nodes}

    while pq:

        current_cost, current = heapq.heappop(pq)

        if current == end:
            break  # Stop once we reach the end node

        x, y = current
        neighbors = [
            (x + gridsize, y), (x - gridsize, y),
            (x, y + gridsize), (x, y - gridsize)
        ]

        for neighbor in neighbors:
            if neighbor in nodes and nodes[neighbor] != "inf":  # Check if the node is valid and traversable
                new_cost = current_cost + nodes[neighbor]
                if new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    previous[neighbor] = current
                    heapq.heappush(pq, (new_cost, neighbor))
    path = []
    node = end
    while node:
        path.append(node)
        node = previous[node]

    return path[::-1] if path[-1] == start else []  # Return reversed path or empty if no path


def main():
    image = cv2.imread('img/frame1.png')
    start = (0,0)
    goal = (100,100)
    path = returnPath(image, start, goal)
    print(len(path))

def parsePoint(x,y,size = 10):
    return ( x - (x % size), y - (y % size) )

def returnPath(image,start,goal):
    height, width, block_size, average_weights = imageread(image)

    start = ( clamp(start[0],0,width) , clamp(start[1],0,height) )
    goal = ( clamp(goal[0],0,width) , clamp(goal[1],0,height) )

    start = parsePoint(start[0], start[1], block_size)
    start = (start[0]+block_size//2,start[1]+block_size//2)

    goal = parsePoint(goal[0], goal[1], block_size)
    goal = (goal[0]+block_size//2,goal[1]+block_size//2)

    path = dijkstra(start, goal, average_weights, block_size)

    return path

def clamp(x,min,max):
    if x < min:
        return min
    if x > max:
        return max
    return x

main()