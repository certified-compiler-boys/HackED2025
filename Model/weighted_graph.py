import cv2
import numpy as np
import heapq
threshold = 10
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
            normalized_weight = round(avg_weight / 255.0, 2)

            if np.mean(red_channel) - np.mean(green_channel) > threshold:
                normalized_weight = "inf"
            else:
                normalized_weight = (normalized_weight*10)**1.5

            average_weights[(x,y)] = normalized_weight

    return height, width, block_size, average_weights

def dijkstra(start, end, nodes, gridsize):
    # Priority queue for Dijkstra's algorithm
    pq = [(0, start)]  # (cost, node)
    distances = {coord: float('inf') for coord in nodes}
    distances[start] = 0
    previous = {coord: None for coord in nodes}

    if nodes[start] == "inf" or nodes[end] == "inf":
        return []

    while pq:

        current_cost, current = heapq.heappop(pq)

        if current == end:
            break  # Stop once we reach the end node

        x, y = current
        neighbors = [
            (x + gridsize, y), (x - gridsize, y),
            (x, y + gridsize), (x, y - gridsize),
            (x + gridsize, y + gridsize), (x + gridsize, y - gridsize),
            (x - gridsize, y - gridsize), (x - gridsize, y + gridsize)
        ]

        for neighbor in neighbors:
            if neighbor in nodes and nodes[neighbor] != "inf":  # Check if the node is valid and traversable
                magnitude = ((abs(neighbor[0]-x) + abs(neighbor[1]-y))/gridsize)**0.5
                new_cost = current_cost + nodes[neighbor]*magnitude
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




def parsePoint(x,y,size = 10):
    return ( x - (x % size), y - (y % size) )

def returnPath(image,start,goal):
    height, width, block_size, average_weights = imageread(image)

    start = (start[0]/100 *width, start[1]/100*height)
    goal = (goal[0]/100 *width, goal[1]/100*height)

    start = ( clamp(start[0],0,width) , clamp(start[1],0,height) )
    goal = ( clamp(goal[0],0,width) , clamp(goal[1],0,height) )

    start = parsePoint(start[0], start[1], block_size)
    start = (start[0]+block_size//2,start[1]+block_size//2)
    goal = parsePoint(goal[0], goal[1], block_size)
    goal = (goal[0]+block_size//2,goal[1]+block_size//2)

    path = dijkstra(start, goal, average_weights, block_size)
    new_path = []
    for point in (path):
        xc = point[0]*100
        yc = point[1]*100
        new_path.append([xc/width, yc/height])
    return new_path

def clamp(x,min,max):
    if x < min:
        return min
    if x > max:
        return max
    return x

def main():
    image = cv2.imread('frame1.png')
    start = (10,55)
    goal = (95,95)

    height, width, _ = image.shape
    height, width = parsePoint(height, width, 10)

    path = returnPath(image, start, goal)
    if path != []:
        path[0] = (int(path[0][0]/100 * width),int(path[0][1]/100 * height))

    for i in range(len(path) - 1):
##        path[i] = (int(path[i][0]),int(path[i][1]))
##        path[i+1] = (int(path[i+1][0]),int(path[i+1][1]))
##        print(path[i])
        
        path[i+1] = (int(path[i+1][0]/100 * width),int(path[i+1][1]/100 * height))
        cv2.line(image, path[i], path[i + 1], (0, 255, 0), 10)  # Green color, thickness = 2

##        Show the image (optional)

    image = cv2.bitwise_not(image)
    cv2.imshow('Image with Path', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
