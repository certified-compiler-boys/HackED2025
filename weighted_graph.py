import cv2
import numpy as np
import heapq

def imageread():

    # Load the image
    image = cv2.imread('img/frame1.png')

    if image is None:
        raise FileNotFoundError("The image 'fram1.png could not be found")

    height, width, _ = image.shape
    block_size = 10
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
            print(neighbor)
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
    start = (1,5)
    goal = (1900,1070)

    
    
    height, width, block_size, average_weights = imageread()

    start = (max(0,start[0]),min(width,start[1]))
    goal = (max(0,goal[0]),min(width,goal[1]))

    # path = algorithm2.a_star(start, goal, width, height, average_weights, block_size, 5)
    start = parsePoint(start[0], start[1], block_size)
    start = (start[0]+block_size//2,start[1]+block_size//2)
    goal = parsePoint(goal[0], goal[1], block_size)
    goal = (goal[0]+block_size//2,goal[1]+block_size//2)

    path = dijkstra(start, goal, average_weights, block_size)
    
    if path != None:
        for k in range (len(path)):
            print(path[k])
    else:
        print(path)


def parsePoint(x,y,size = 10):
    return ( x - (x % size), y - (y % size) )


main()