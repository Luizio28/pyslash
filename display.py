import cursor

memory = []
width = 80
height = 22

def _init(y = width,x = height):
    global memory, width, height
    
    memory = []
    width = y
    height = x

    for i in range (0, x):
        memory.append([])
        for j in range (0, y):
            memory[i].append("")

    return memory

# Function for drawing the entire frame
def draw():
    cursor._noecho()
    cursor.show(0)

    for i in range (0,height):
        for j in range (0,width):
            cursor.draw(memory[i][j],i,j)

    cursor._restore()
