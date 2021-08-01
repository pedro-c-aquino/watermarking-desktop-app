import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont


class App(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.title("Watermarking Desktop App")
        self.label_title = tk.Label(text="Watermarking Desktop App", font=("Arial", 14))
        self.label_title.config(padx=20, pady=20)
        self.label_title.pack()

        self.file_label = tk.Label(text="Choose a file to be watermarked: ", font=("Arial", 10))
        self.file_label.pack()

        self.filename = ""
        self.new_window = ""
        self.text = StringVar()
        self.img = ""

        self.button = tk.Button(text="Browse", command=self.open_file)
        self.button.pack()

        self.mainloop()

    def open_file(self):
        self.filename = filedialog.askopenfilename()
        self.open_image()

    def open_image(self):
        self.img = Image.open(self.filename).convert("RGBA")
        self.img = self.img.resize((800, 600))
        filename = ImageTk.PhotoImage(self.img)
        self.new_window = tk.Toplevel(self)
        text_button = Button(master=self.new_window, text="Add Text", command=self.add_text)
        text_button.grid(row=0, column=0)
        logo_button = Button(master=self.new_window, text="Add Logo", command=self.add_logo)
        logo_button.grid(row=0, column=1)
        canvas = Canvas(self.new_window, height=600, width=800)
        canvas.image = filename
        canvas.create_image(0, 0, anchor='nw', image=filename)
        canvas.grid(row=1, column=0, columnspan=8)

    def add_text(self):
        entry = Entry(master=self.new_window, textvariable=self.text)
        entry.grid(row=0, column=2)
        self.text.set("Type the text you want as a watermark: ")
        self.scale = Scale(master=self.new_window, label="opacity", from_=0, to=100)
        self.scale.grid(row=0, column=3)
        ok_button = Button(master=self.new_window, text="Ok", command=self.text_watermark)
        ok_button.grid(row=0, column=4)

    def text_watermark(self):
        photo = self.img
        txt = Image.new("RGBA", photo.size, (255, 255, 255, 0))
        drawing = ImageDraw.Draw(txt)
        text = self.text.get()
        opacity = round(self.scale.get() * 255/100)
        font = ImageFont.truetype("times.ttf", 20)
        drawing.text((400, 300), text, fill=(255, 255, 255, opacity), font=font)
        water_marked = Image.alpha_composite(photo, txt)
        water_marked.show()

    def open_logo(self):
        self.logo_name = filedialog.askopenfilename()

    def add_logo(self):
        browse_logo = Button(master=self.new_window, text="Browse logo file", command=self.open_logo)
        browse_logo.grid(row=0, column=2)
        ok_button = Button(master=self.new_window, text="Ok", command=self.logo_watermark)
        ok_button.grid(row=0, column=4)

    def logo_watermark(self):
        photo = self.img
        watermark = Image.open(self.logo_name).convert("RGBA")
        watermark = watermark.resize((80, 60))
        width = watermark.size[0]
        height = watermark.size[1]
        for x in range(0, width):  # process all pixels
            for y in range(0, height):
                data = watermark.getpixel((x, y))
                if data[0] == 255 and data[1] == 255 and data[2] == 255:
                    watermark.putpixel((x, y), (255, 255, 255, 0))
        transparent = Image.new('RGBA', (800, 600), (0, 0, 0, 0))
        transparent.paste(photo, (0, 0))
        transparent.paste(watermark, (400, 300), watermark)
        transparent.show()


if __name__ == "__main__":
    App()
