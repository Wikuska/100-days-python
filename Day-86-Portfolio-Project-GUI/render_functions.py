from tkinter import *
import random
from test_texts import test_texts, practice_texts
from best_scores import scores

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

    practice_button = Button(main_menu_frame, text = "Typing speed practice", bg = WIDGETS_COLOR, bd = 5, relief = "solid", font = BUTTON_FONT, command = lambda: render_new_frame(root, render_speed_practice))
    practice_button.grid(column = 1, row = 3, sticky="nsew")

    test_button = Button(main_menu_frame, text = "Typing speed test", bg = WIDGETS_COLOR, bd = 5, relief = "solid", font = BUTTON_FONT, command = lambda: render_new_frame(root, render_speed_test))
    test_button.grid(column = 3, row = 3, sticky="nsew")

    scores_button = Button(main_menu_frame, text = "Best test scores", bg = WIDGETS_COLOR, bd = 5, relief = "solid", font = BUTTON_FONT, command = lambda: render_new_frame(root, render_speed_scores))
    scores_button.grid(column = 5, row = 3, sticky="nsew")

    main_menu_frame.grid_rowconfigure((0,1,2,3,4), weight=1)
    main_menu_frame.grid_columnconfigure((0,1,2,3,4,5,6), weight=1)


def render_speed_practice(root):
    speed_practice_frame = Frame(root, bg=MAIN_COLOR)
    speed_practice_frame.pack(fill='both', expand=True)

    title_label = title_label = Label(speed_practice_frame, text = "Practice your speed without time pression", bg = WIDGETS_COLOR, font = HEADER_FONT)
    title_label.grid(column = 0, row = 0, columnspan = 3, sticky="nsew")

    main_text_label = Label(speed_practice_frame, text = random.choice(practice_texts), font = BUTTON_FONT, bg = WIDGETS_COLOR, wraplength = 700)
    main_text_label.grid(column = 0, row = 2,columnspan = 3, rowspan = 2, sticky="nsew")

    user_text_entry = Entry(speed_practice_frame, font = BUTTON_FONT)
    user_text_entry.grid(column = 0, row = 5, columnspan = 3, sticky="nsew")

    main_menu_button = Button(speed_practice_frame, text = "Main menu", bg = WIDGETS_COLOR, font = ("Open Sans", 14, "bold"),bd = 5, relief = "solid", command = lambda: render_new_frame(root, render_main_menu))
    main_menu_button.grid(column = 0, row = 7, sticky="nsew")

    check_text_button = Button(speed_practice_frame, text = "Check your answer", bg = WIDGETS_COLOR, font = ("Open Sans", 14, "bold"),bd = 5, relief = "solid")
    check_text_button.grid(column = 1, row = 7, sticky="nsew", padx = 10)

    next_text_button = Button(speed_practice_frame, text = "Next text", bg = WIDGETS_COLOR, font = ("Open Sans", 14, "bold"),bd = 5, relief = "solid")
    next_text_button.grid(column = 2, row = 7, sticky="nsew")

    speed_practice_frame.grid_columnconfigure((0,1,2), weight = 1)
    speed_practice_frame.grid_rowconfigure((1,2,3,4,5,6), weight = 2)
    speed_practice_frame.grid_rowconfigure((0,7), weight = 1)


def render_speed_test(root):
    speed_test_frame = Frame(root, bg=MAIN_COLOR)
    speed_test_frame.pack(fill='both', expand=True)

    title_label = Label(speed_test_frame, text = "Timer starts as you start typing", bg = WIDGETS_COLOR, font = HEADER_FONT)
    title_label.grid(column = 1, row = 0, columnspan = 5, sticky="nsew")

    main_text_label = Label(speed_test_frame, text = random.choice(test_texts), bg = WIDGETS_COLOR, font = BUTTON_FONT, wraplength = 900)
    main_text_label.grid(column = 1, row = 2, columnspan = 5, rowspan = 2, sticky="nsew")

    user_text_entry = Entry(speed_test_frame, font = BUTTON_FONT)
    user_text_entry.grid(column = 1, row = 5, columnspan = 4, rowspan = 2, sticky="nsew")

    back_to_menu_button = Button(speed_test_frame, text = "Main menu", bg = WIDGETS_COLOR, font = ("Open Sans", 14, "bold"),bd = 5, relief = "solid", command = lambda: render_new_frame(root, render_main_menu))
    back_to_menu_button.grid(column = 5, row = 5, rowspan = 2, sticky="nsew", padx = (10,0))

    speed_test_frame.grid_columnconfigure((0,1,2,3,4,5,6), weight=2)
    speed_test_frame.grid_rowconfigure((1,2,3,4,5), weight=2)
    speed_test_frame.grid_rowconfigure(0, weight=1)

def render_speed_scores(root):
    speed_scores_frame = Frame(root, bg=MAIN_COLOR)
    speed_scores_frame.pack(fill='both', expand=True)

    title_label = Label(speed_scores_frame, text = "Your 10 best scores", bg = WIDGETS_COLOR, font = HEADER_FONT)
    title_label.grid(column = 0, row = 0, columnspan = 3, sticky="nsew")

    scores_label = Label(speed_scores_frame, bg = WIDGETS_COLOR, font = BUTTON_FONT)
    scores_label.grid(column = 0, row = 1, columnspan = 3, sticky="nsew", pady = 10)

    main_menu_button = Button(speed_scores_frame, text = "Main menu", bg = WIDGETS_COLOR, font = ("Open Sans", 14, "bold"),bd = 5, relief = "solid", command = lambda: render_new_frame(root, render_main_menu))
    main_menu_button.grid(column = 1, row = 2, sticky="nsew")

    speed_scores_frame.grid_columnconfigure((0,1,2), weight = 1)
    speed_scores_frame.grid_rowconfigure(1, weight = 3)
    speed_scores_frame.grid_rowconfigure((0,2), weight = 1)