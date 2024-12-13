from tkinter import *
from tkinter import filedialog
from PIL import ImageTk
from helper_functions import load_image, create_photo_canvas, create_settings_frame, update_coords_entry, apply_watermark, save_picture
MAIN_COLOR = "#C3BBBB"

class AppInterface:
    def __init__(self):
        self.window = Tk()
        self.window.title("Watermark App")
        self.window.configure(padx = 20, pady = 20, bg = MAIN_COLOR)

        self.main_frame = Frame(self.window, bg=MAIN_COLOR)
        self.main_frame.grid(row=0, column=0)
        self.name_label = Label(self.main_frame, text = "Watermark creator", font = ("Arial", 30), bg=MAIN_COLOR)
        self.name_label.grid(column=0, row=0)

        self.canvas = None
        self.settings_frame = None
        self.save_button = None

        self.choose_button = Button(self.main_frame, text="Choose a picture", command = self.get_picture)
        self.choose_button.grid(column=0, row=2, pady=10)

        self.window.mainloop()

    def get_picture(self):
        if self.save_button:
            self.save_button.destroy()
            self.save_button = None

        self.file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
        if self.file_path:
            self.photo, self.photo_width, self.photo_height = load_image(self.file_path)
            if self.photo:
                self.display_picture()

    def display_picture(self):
        if self.canvas:
                self.canvas.destroy()
        self.canvas = create_photo_canvas(self.main_frame, self.photo_width, self.photo_height, self.photo)
        self.canvas.grid(column=0,row=1)
        self.canvas.bind("<Button-1>", self.on_image_click)

    def on_image_click(self, event):
        if self.settings_frame is None:
            self.settings_frame, self.coords_entry, self.text_entry, self.transparency_slider = create_settings_frame(
                self.window, event.x, event.y, self.settings_frame, self.create_watermark)
        else:
            update_coords_entry(self.coords_entry, event.x, event.y)

    def create_watermark(self):
        coords = tuple([int(num) for num in self.coords_entry.get().split(", ")])
        text_color = (255, 0, 0, self.transparency_slider.get())
        self.edit_photo = apply_watermark(self.file_path, coords, self.text_entry.get() ,text_color)
        self.photo = ImageTk.PhotoImage(self.edit_photo)
        self.display_picture()
        if self.save_button is None:
            self.save_button = Button(self.settings_frame, text="Save picture", command=lambda: save_picture(self.edit_photo))
            self.save_button.grid(column=1, row=4)

app = AppInterface()

