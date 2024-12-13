from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
SETTINGS_COLOR = "#BAACAC"

def load_image(file_path):
    try:
        image = Image.open(file_path)
        img_width, img_height = image.size
        photo = ImageTk.PhotoImage(image)
        return photo, img_width, img_height
    except Exception:
        print(f"Error loading image: {Exception}")
        return None, None, None

def create_photo_canvas(parent_frame, width, height, picture):
    canvas = Canvas(parent_frame, height=height, width=width, highlightthickness=0)
    canvas.create_image(0, 0, anchor=NW, image=picture)
    return canvas

def create_settings_frame(window, x, y, frame, button_function):
    frame = Frame(window, bg= SETTINGS_COLOR)
    frame.grid_rowconfigure((1,2,3,4), weight=1, uniform="equal")
    frame.grid(column=1, row=0, sticky="nsew", padx=(10,0))
    
    settings_label = Label(frame, text = "Settings", font = ("Arial", 30), bg=SETTINGS_COLOR)
    settings_label.grid(column=0, row=0, columnspan=2)

    coords_label = Label(frame, text = "Watermark coords(x, y)", font = ("Arial", 10), bg=SETTINGS_COLOR)
    coords_label.grid(column=0, row=1, padx=10)
    coords_entry = Entry(frame)
    coords_entry.insert(0, f"{x}, {y}")
    coords_entry.grid(column=1, row=1, padx=10)

    text_label = Label(frame, text = "Watermark text", font = ("Arial", 10), bg=SETTINGS_COLOR)
    text_label.grid(column=0, row=2)
    text_entry = Entry(frame)
    text_entry.grid(column=1, row=2)

    transparency_label = Label(frame, text = "Color intensity", font = ("Arial", 10), bg=SETTINGS_COLOR)
    transparency_label.grid(column=0, row=3)
    transparency_slider = Scale(frame, from_=0, to=255, orient=HORIZONTAL, bg=SETTINGS_COLOR, highlightthickness=0)
    transparency_slider.grid(column=1, row=3)

    create_button = Button(frame, text="Create watermark", command=button_function)
    create_button.grid(column=0, row=4)

    return frame, coords_entry, text_entry, transparency_slider

def update_coords_entry(entry, x, y):
    entry.delete(0, END)
    entry.insert(0, f"{x}, {y}")
    
def apply_watermark(file_path, coords, text, color):
    edit_photo = Image.open(file_path).convert("RGBA")
    draw = ImageDraw.Draw(edit_photo)
    draw.text(xy=coords, text=text, fill=color)
    return edit_photo

def save_picture(photo):
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
    if save_path:
        photo.save(save_path)
