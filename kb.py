import os, sys

ENTER = "ENTER"
BACKSPACE = "BACKSPACE"
TAB = "TAB"
ESC = "ESC"

ARROWS = {
    "\x1b[A": "UP",
    "\x1b[B": "DOWN",
    "\x1b[C": "RIGHT",
    "\x1b[D": "LEFT",
}

FUNCTION_KEYS = {
    "\x1bOP": "F1",
    "\x1bOQ": "F2",
    "\x1bOR": "F3",
    "\x1bOS": "F4",
}

if os.name == "nt":
    import msvcrt

    def get():
        ch = msvcrt.getch()

        # Special keys (arrows, F-keys)
        if ch in (b"\x00", b"\xe0"):
            ch = msvcrt.getch()
            return f"SPECIAL_{ch.hex()}"

        ch = ch.decode(errors="ignore")

        if ch == "\r":
            return ENTER
        if ch == "\b":
            return BACKSPACE
        if ch == "\x1b":
            return ESC

        if ord(ch) < 32:  # Ctrl + key
            return f"CTRL+{chr(ord(ch) + 64)}"

        return ch

    def enable():
        pass

    def disable():
        pass

else:
    import termios, tty

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)

    def enable():
        tty.setraw(fd)

    def disable():
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

    def get():
        ch = sys.stdin.read(1)

        if ch == "\r" or ch == "\n":
            return ENTER
        if ch == "\x7f":
            return BACKSPACE
        if ch == "\t":
            return TAB
        if ch == "\x1b":
            # Escape or escape sequence
            seq = ch + sys.stdin.read(2)
            if seq in ARROWS:
                return ARROWS[seq]
            if seq in FUNCTION_KEYS:
                return FUNCTION_KEYS[seq]
            return ESC

        if ord(ch) < 32:  # Ctrl + key
            return f"CTRL+{chr(ord(ch) + 64)}"

        return ch

