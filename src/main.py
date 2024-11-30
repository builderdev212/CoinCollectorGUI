import logging
import os

from gui import gui


def main():
    logging.basicConfig(filename="gui.log", level=logging.INFO)
    ccgui = gui()
    ccgui.win.mainloop()


if __name__ == "__main__":
    main()
