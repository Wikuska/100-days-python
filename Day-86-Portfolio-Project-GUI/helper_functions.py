from tkinter import *
import random

def get_random_text(list):
    text = random.choice(list)
    return text

def get_label_text(label):
    label_text = label.cget("text")
    return label_text

def check_text_correctness(title_label, text_label, user_text):
    if user_text == "":
        return title_label.config(text = "There is nothing to check", fg = "red")
    else:
        original_text = get_label_text(text_label)
        original_words = original_text.split()
        user_words = user_text.split()
        for i in range(len(original_words)):
            if original_words[i] != user_words[i]:
                return title_label.config(text = f"There is mistake in word {user_words[i]}", fg = "red")
        return title_label.config(text = f"Everything looks correct", fg = "green")

def generate_new_text(title_label, text_label, entry, list):
    new_text = get_random_text(list)
    if entry.get():
        return text_label.config(text = new_text), entry.delete(0, END), title_label.config(text = "Practice your speed without time pression", fg = "black")
    return text_label.config(text = new_text), title_label.config(text = "Practice your speed without time pression", fg = "black")
