maze = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1],
[1,0,1,0,0,1,0,0,0,0,0,0,0,0,0,1],
[1,0,1,0,0,1,1,0,0,0,0,0,0,0,0,1],
[1,0,1,1,0,0,1,1,0,0,0,0,0,0,0,1],
[1,1,0,1,0,0,0,1,0,0,0,1,1,1,1,1],
[1,0,0,1,1,0,0,1,0,0,0,1,0,0,0,1],
[3,0,1,0,1,0,0,1,1,0,1,1,0,0,0,3],
[1,0,1,0,1,0,0,0,1,0,1,0,0,0,0,1],
[1,0,1,1,1,0,1,0,1,1,1,0,0,1,1,1],
[1,0,0,0,0,0,1,0,0,0,0,0,1,1,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
[1,1,1,0,1,1,1,0,0,0,1,1,1,0,0,1],
[1,0,1,1,1,0,1,0,0,1,1,0,0,0,0,1],
[1,0,0,1,0,0,1,0,0,1,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

newMaze = []

for row in range(0, len(maze)):
    newMaze.append([])
    for col in range(0, len(maze[row])):
        if maze[row][col] == 1:
            newMaze[row].extend([1,1,1])
        else:
            newMaze[row].extend([0,maze[row][col],0])

newestMaze = []

for row in range(0, len(newMaze)):
    newestMaze.extend([newMaze[row][:], newMaze[row][:], newMaze[row][:]])

print(newestMaze)

for row in range(0, len(newestMaze)):
    for col in range(0, len(newestMaze[row])):
        if newestMaze[row][col] == 1:
            print(row, col)
            try:
                if newestMaze[row][col-1] == 0:
                    newestMaze[row][col-1] = 9
            except:
                pass

            try:
                if newestMaze[row][col+1] == 0:
                    newestMaze[row][col+1] = 9
            except:
                pass

            try:
                if newestMaze[row-1][col] == 0:
                    newestMaze[row-1][col] = 9
            except:
                pass

            try:
                if newestMaze[row+1][col] == 0:
                    newestMaze[row+1][col] = 9
            except:
                pass

            try:
                if newestMaze[row-1][col-1] == 0:
                    newestMaze[row-1][col-1] = 9
            except:
                pass

            try:
                if newestMaze[row-1][col+1] == 0:
                    newestMaze[row-1][col+1] = 9
            except:
                pass

            try:
                if newestMaze[row+1][col-1] == 0:
                    newestMaze[row+1][col-1] = 9
            except:
                pass

            try:
                if newestMaze[row+1][col+1] == 0:
                    newestMaze[row+1][col+1] = 9
            except:
                pass

print(newestMaze)
