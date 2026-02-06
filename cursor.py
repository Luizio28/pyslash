import os
import sys

if sys.platform == 'win32':
    # Windows
    import ctypes
    from ctypes import *
    clear_screen = "cls"

    renderer_gHandle = ctypes.windll.kernel32.GetStdHandle(c_long(-11))

    def setpos (y, x):
       value = x + (y << 16)
       ctypes.windll.kernel32.SetConsoleCursorPosition(renderer_gHandle, c_ulong(value))

    def draw(string,i = -1,j = -1):
        if i != -1 or j != -1:
            setpos(i,j)
        ctypes.windll.kernel32.WriteConsoleW(renderer_gHandle, c_wchar_p(string), c_ulong(len(string)), c_void_p(), None)

    # this bit i got from nneonneo at stackoverflow   
    class CONSOLE_CURSOR_INFO(Structure):
        _fields_ = [('dwSize', c_int),
                    ('bVisible', c_int)]
    STD_OUTPUT_HANDLE = -11

    hStdOut = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    cursorInfo = CONSOLE_CURSOR_INFO()
    #

    def show(a):
        cursorInfo.dwSize = 1
        cursorInfo.bVisible = a
        windll.kernel32.SetConsoleCursorInfo(hStdOut, byref(cursorInfo))
           
    #

if sys.platform == 'linux':
    # Linux
    clear_screen = "clear"

    def _flush():
        sys.stdout.flush()

    def setpos(y, x):
        sys.stdout.write(f"\x1b[{y+1};{x+1}H")
        _flush()

    def draw(string,i = -1,j = -1):
        if i != -1 or j != -1:
            setpos(i,j)
        sys.stdout.write(string)
        _flush()

    def show(a):
        if a == 0:
            sys.stdout.write("\x1b[?25l")
        elif a == 1:
            sys.stdout.write("\x1b[?25h")
        _flush()
    #

def clear():
    os.system(clear_screen)

# lame chagpt solution for echoing on linux

if os.name == "nt":
    def _noecho(): pass
    def _restore(): pass
else:
    import termios
    _fd = sys.stdin.fileno()
    _old = termios.tcgetattr(_fd)

    def _noecho():
        new = termios.tcgetattr(_fd)
        new[3] &= ~(termios.ECHO | termios.ICANON)
        new[6][termios.VMIN] = 1
        new[6][termios.VTIME] = 0
        termios.tcsetattr(_fd, termios.TCSADRAIN, new)

    def _restore():
        termios.tcsetattr(_fd, termios.TCSADRAIN, _old)






