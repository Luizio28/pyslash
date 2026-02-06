import colorama

colorama.init()

# Prefix strings
preFg = "\x1b[38;2;"
preBg = "\x1b[48;2;"
reset = "\x1b[0m"

# Pallete dictionary
palette = {}

# Setup function
def load(path = "data/palette.txt"):
    colors = {}
    count = 0

    loaded = open(path, "r",encoding="UTF-8").read().rsplit("\n")

    for i in range (0,len(loaded)-1):
        loaded[i] = loaded[i].rsplit(" ")
        colors.update( {str( loaded[i][0] ): str(loaded[i][1])+";"+ str(loaded[i][2]) +";"+ str(loaded[i][3]) +"m"} )
        count += 1

    colors.update({"none":""})
    return colors

# Color function
def set(fg='white',bg='none'):
    _fg = ""
    _bg = ""

    if fg != 'none':
        _fg = preFg
    if bg != 'none':
        _bg = preBg

    try: return _fg+palette[fg] + _bg+palette[bg]
    except: return ""

