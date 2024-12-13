from tkinter import *

MAIN_COLOR = "#919191"
WIDGETS_COLOR = "#707070"
HEADER_FONT = ("Open Sans", 23, "bold")
BUTTON_FONT = ("Open Sans", 14)

def render_new_frame(root, render_function):
    for widget in root.winfo_children():
        widget.destroy()
    render_function(root)

def render_main_menu(root):
    main_menu_frame = Frame(root, bg = MAIN_COLOR)
    main_menu_frame.pack(fill='both', expand=True)

    title_label = Label(main_menu_frame, text = "Test your typing skills", bg = WIDGETS_COLOR, font = HEADER_FONT)
    title_label.grid(column = 1, row = 1, columnspan = 5, sticky="nsew")

    practice_button = Button(main_menu_frame, text = "Typing speed practice", bg = WIDGETS_COLOR, bd = 5, relief = "solid", font = BUTTON_FONT, command = lambda: render_new_frame(root, render_speed_test))
    practice_button.grid(column = 1, row = 3, sticky="nsew")

    test_button = Button(main_menu_frame, text = "Typing speed test", bg = WIDGETS_COLOR, bd = 5, relief = "solid", font = BUTTON_FONT, command = lambda: render_new_frame(root, render_speed_test))
    test_button.grid(column = 3, row = 3, sticky="nsew")

    scores_button = Button(main_menu_frame, text = "Speed test scores", bg = WIDGETS_COLOR, bd = 5, relief = "solid", font = BUTTON_FONT, command = lambda: render_new_frame(root, render_speed_scores))
    scores_button.grid(column = 5, row = 3, sticky="nsew")

    main_menu_frame.grid_rowconfigure((0,1,2,3,4), weight=1)
    main_menu_frame.grid_columnconfigure((0,1,2,3,4,5,6), weight=1)


def render_speed_practice(root):
    speed_practice = Frame(root, bg=MAIN_COLOR)
    speed_practice.pack(fill='both', expand=True)

def render_speed_test(root):
    speed_test_frame = Frame(root, bg=MAIN_COLOR)
    speed_test_frame.pack(fill='both', expand=True)

def render_speed_scores(root):
    speed_scores_frame = Frame(root, bg=MAIN_COLOR)
    speed_scores_frame.pack(fill='both', expand=True)