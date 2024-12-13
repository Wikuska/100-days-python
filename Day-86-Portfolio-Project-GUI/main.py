from tkinter import *
from render_functions import render_main_menu

MAIN_COLOR = "#919191"

root = Tk()
root.title("Test yout typing skills")
root.geometry("1000x400")
root.resizable(False, False)
root.configure (padx = 20, pady = 20, bg = MAIN_COLOR)

render_main_menu(root)

root.mainloop()