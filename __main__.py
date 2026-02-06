import os
import sys

import cursor
import display
import color
import kb

import random

# Initial definitions
color.palette = color.load()

size = [48,16]

display.memory = display._init(size[0],size[1])
# #

# Game
pos = [10,10]

level = []

charlist = {}

tags = {
'solid':('wood','wood2','wall','boards','deep','boulder'),
'ground':('grass','grass2','sand','dirt'),
'nobuild':('deep')
}

inventory = {
'1':'wall',
'2':'boards',
'3':'floor',
'4':'door'
}  

selected = 'wall'

# Move player/cursor
def move(x,y):
    global pos
    newpos = [pos[0]+x,pos[1]+y]    

    try:
        if not newpos[0] == size[1] and not newpos[0] == -1:
            if not level[newpos[0]][newpos[1]] in tags['solid']:
                pos[0] += x
        if not newpos[1] == size[0] and not newpos[1] == -1:
            if not level[newpos[0]][newpos[1]] in tags['solid']:
                pos[1] += y
    except: pass



# Load charlist
loaded = open("data/char.txt", "r",encoding="UTF-8").read().rsplit("\n")
for i in range (0,len(loaded)-1):
    loaded[i] = loaded[i].rsplit(" ")
    charlist.update( { loaded[i][1]: color.set( loaded[i][2] , loaded[i][3] ) + loaded[i][0] + color.reset } )
loaded = ""


# Generate level
def level_generate():
    global level

    level = []
    # Flooding
    for i in range (0, size[1]):
        level.append([])
        for j in range (0, size[0]):
            level[i].append("water")
    for i in range (0, size[1]):
        for j in range (0, size[0]):
            if i == 0 or j == 0 or i == size[1]-1 or j == size[0]-1:
                roll = random.randint(1,100)
                if roll > 30:
                    level[i][j] = 'deep'

    # Filling
    for i in range (0, size[1]):
        for j in range (0, size[0]):
            roll = random.randint(1,100)
            if (roll > 90):
                level[i][j] = 'sand'

    for i in range (0, size[1]):
        for j in range (0, size[0]):
            offset_x = random.choice([7,7,7,7,7,5,5,5,5,5,5,5,5,5,3,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,1,1])
            offset_y = random.choice([7,7,7,7,7,5,5,5,5,5,5,5,5,5,3,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,1,1])-3
            if (i > offset_y and i < size[1]-offset_y) and (j > offset_x and j < size[0]-offset_x):
                level[i][j] = 'sand'

    for i in range (0, size[1]):
        for j in range (0, size[0]):
            offset_x = random.choice([7,7,7,7,7,5,5,5,5,5,5,5,5,5,3,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,1,1])+1
            offset_y = random.choice([7,7,7,7,7,5,5,5,5,5,5,5,5,5,3,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,1,1])-2
            if (i > offset_y and i < size[1]-offset_y) and (j > offset_x and j < size[0]-offset_x):
                level[i][j] = 'dirt'

    # Forming
    for i in range (0, size[1]):
        for j in range (0, size[0]):
            roll = random.randint(1,100)
            if (roll > 97) or (roll > 90 and level[i][j] == 'sand'):
                level[i][j] = 'stone'
    
    for i in range (0, size[1]):
        for j in range (0, size[0]):
            roll = random.randint(1,100)
            try:
                if (roll > 90 and level[i][j] == 'stone'):
                    level[i+random.choice([-1,1])][j+random.choice([-1,1])] = 'boulder'
            except: pass

    for i in range (0, size[1]):
        for j in range (0, size[0]):
            roll = random.randint(1,100)
            try:
                if (roll > 70 and level[i][j] == 'boulder'):
                    level[i+random.choice([-1,1])][j+random.choice([-1,1])] = 'boulder'
            except: pass

    for i in range (0, size[1]):
            for j in range (0, size[0]):
                roll = random.randint(1,100)
                try:
                    if (roll > 90 and level[i][j] == 'stone'):
                        level[i+random.choice([-1,1])][j+random.choice([-1,1])] = 'sand'
                except: pass


    # Eroding
    for i in range (0, size[1]):
        for j in range (0, size[0]):
            roll = random.randint(1,100)
            if (roll > 99):
                level[i][j] = 'water'

    for i in range (0, size[1]):
        for j in range (0, size[0]):
            roll = random.randint(1,100)
            try:
                if (roll > 90 and level[i][j] == 'water'):
                    level[i+random.choice([-1,1])][j+random.choice([-1,1])] = 'sand'
            except: pass


    # Planting
    plant = ['wood','wood','wood','wood','wood','wood','wood','wood','wood','bush','flower']
    grass = ['grass','grass','grass','grass','grass','grass','grass','grass','grass2','grass2','grass2','plant']

    for i in range (0, size[1]):
        for j in range (0, size[0]):
            roll = random.randint(1,100)
            if level[i][j] == 'dirt' and roll > 98:
                level[i][j] = random.choice(plant)

    for i in range (0, size[1]):
        for j in range (0, size[0]):
            roll = random.randint(1,100)
            if level[i][j] == 'dirt' and roll > 20:
                level[i][j] = random.choice(grass)






# render level
def level_render():
    for i in range(0, size [1]):
        for j in range (0, size[0]):
            display.memory[i][j] = charlist[level[i][j]]

def level_modify(y,x,tile):
    level[y][x] = tile
    level_render()
    display.draw() 

def player_build(y,x,item = 'none'):
    try:
        if level[y][x] not in tags['ground'] and level[y][x] not in tags['nobuild']:
            level_modify(y,x,'dirt')
        elif level[y][x] in tags['nobuild']:
            return    
        elif item == 'none':
            return
        else:
            level_modify(y,x,item)
    except: return






# Level saving / loading
def level_save(name):
    name = name.lower()

    try:    
        os.makedirs('saves/'+name+'/')
    except: pass

    file_terrain = open("saves/"+name+"/terrain.txt", "w")
    file_data = open("saves/"+name+"/data.txt", "w")

    for i in range(0,size[1]):
        for j in range(size[0]):
            file_terrain.write(level[i][j])
            if not j == size[0]-1:
                file_terrain.write(" ")
        if not i == size[1]-1:
            file_terrain.write("\n")

def level_load(name):
    name =  name.lower()
    
    path = "saves/"+name+"/"
    file_terrain = open(path+"terrain.txt", "r",encoding="UTF-8").read().rsplit("\n")
    for i in range (0,len(file_terrain)):
        file_terrain[i] = file_terrain[i].rsplit(" ")
        for j in range(0,len(file_terrain[i])):
            level[i][j] = file_terrain[i][j]
    
    




# Setup
level_generate()
level_render()

# #

# Main
def main():
    global selected

    cursor.clear()
    
    cursor.draw("CTRL+N: New Level",19,0)
    cursor.draw("CTRL+S: Save Level",20,0)
    cursor.draw("CTRL+L: Load Level",21,0)
    cursor.draw("CTRL+Q: Quit",22,0)
    
    
    cursor.show(1)
    cursor.draw("Selected: "+charlist[selected]+" "*8,17,0)
    # Main loop
    display.draw()

    while True:
        cursor.setpos(pos[0],pos[1])

        kb.enable()
        cursor.show(1)

        key = kb.get()
        kb.disable()
        cursor.show(0)

        if key == "CTRL+Q": break

        if key == "CTRL+N":
            level_generate()
            level_render()
            display.draw() 

        if key == "CTRL+S":
            cursor.setpos(16,0)
            cursor.show(1)

            levelname = input(color.set('white','black')+"Save level as:"+color.reset+" ")
            level_save(levelname)

            cursor.show(0)
            cursor.draw(" "*80,16,0)
        
        if key == "CTRL+L":
            cursor.setpos(16,0)
            cursor.show(1)

            levelname = input(color.set('white','black')+"Level name to load:"+color.reset+" ")
            try: level_load(levelname)
            except: pass

            cursor.show(0)
            cursor.draw(" "*80,16,0)

            level_render()
            display.draw() 

        if key == "UP": move(-1,0)
        if key == "DOWN":move(1,0)
        if key == "LEFT":move(0,-1)
        if key == "RIGHT":move(0,1)

        if key == "w":
            player_build(pos[0]-1,pos[1],selected)
        if key == "s":
            player_build(pos[0]+1,pos[1],selected)
        if key == "a":
            player_build(pos[0],pos[1]-1,selected)
        if key == "d":
            player_build(pos[0],pos[1]+1,selected)

        if key in ('1','2','3','4'):
            selected = inventory[key]
            cursor.draw("Selected: "+charlist[selected]+" "*8,17,0)

# Start program
if __name__ == "__main__":
    try:    
        main()
    finally:
        cursor.clear()
        cursor.setpos(0,0)
        cursor._restore()
        cursor.show(1)




