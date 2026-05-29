# Two Knights at Trenstein's by Mason Rustad

# === RUN THIS FILE === #

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
from game import Game
def main() -> None:
    '''
    Creates the game and runs the loop.
    '''
    Game("Five Knights at Trensteins").loop()

if __name__ == "__main__":
    main()