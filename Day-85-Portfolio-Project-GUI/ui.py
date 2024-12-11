from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

MAIN_COLOR = "#C3BBBB"
SETTINGS_COLOR = "#BAACAC"

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

        self.choose_button = Button(self.main_frame, text="Choose a picture", command = self.get_picture)
        self.choose_button.grid(column=0, row=2, pady=10)

        self.settings_frame = None

        self.window.mainloop()

    def get_picture(self):
        try:
            if self.canvas:
                self.canvas.destroy()

            file_path = filedialog.askopenfilename(
                filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")]
            )
            if file_path:
                image = Image.open(file_path)
                img_width, img_height = image.size
                self.photo = ImageTk.PhotoImage(image)

                self.canvas = Canvas(self.main_frame, height = img_height, width = img_width, highlightthickness=0)
                self.canvas.create_image(0, 0, anchor=NW, image=self.photo)
                self.canvas.grid(column=0,row=1)

                self.canvas.bind("<Button-1>", self.on_image_click)
        except Exception as e:
            print(f"Error loading image: {e}")

    def on_image_click(self, event):
        if self.settings_frame is None:

            self.settings_frame = Frame(self.window, bg= SETTINGS_COLOR)
            self.settings_frame.grid(column=1, row=0, sticky="nsew", padx=(10,0))
            
            self.settings_label = Label(self.settings_frame, text = "Watermark settings", font = ("Arial", 30), bg=SETTINGS_COLOR)
            self.settings_label.grid(column=0, row=0, columnspan=2)

            self.coords_label = Label(self.settings_frame, text = "Watermark coords", font = ("Arial", 10), bg=SETTINGS_COLOR)
            self.coords_label.grid(column=0, row=1)
            self.coords_entry = Entry(self.settings_frame)
            self.coords_entry.insert(0, f"{event.x}, {event.y}")
            self.coords_entry.grid(column=1, row=1)

            self.text_label = Label(self.settings_frame, text = "Watermark text", font = ("Arial", 10), bg=SETTINGS_COLOR)
            self.text_label.grid(column=0, row=2)
            self.text_entry = Entry(self.settings_frame)
            self.text_entry.grid(column=1, row=2)
        
        else:
            self.coords_entry.delete(0,END)
            self.coords_entry.insert(0, f"{event.x}, {event.y}")
