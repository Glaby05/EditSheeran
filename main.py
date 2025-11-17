import tkinter as tk
from PIL import ImageTk, Image

root=tk.Tk(); root.title("EditSheeran")
root.iconbitmap(r"assets/ed.ico")
root.geometry("900x500")

# Window / Root with fixed size - done sw
# put Frames as partitions of the app:
#   - to divide the app into different main parts
#   -> left: options for Ed Sheeran pictures (1/4 of window vertically)
#   -> middle: the main editing Frame/scene  (2-3/4 of window vertically)
#   -> right: (last quarter of window vertically)
#       -> top:
#       -> bottom: display the last update of the picture
#

class ImageEditor:
    # Note: we can also grayscale the image to further edit them, like the
    # contrast etc. BUT my concern is making the Ed too editable will drive the
    # user away from editing the actual card
    # (which is also Prof's concern from OH)
    def __init__(self, master):
        self.master = master
        master.title("Image Editor")

        self.image = None  # in the form of file opened
        self.photo_image = None  # ImageTk.PhotoImage(self.image)
        self.canvas = tk.Canvas(master, bg="lightgray")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()

    def create_widgets(self):
        # buttons that triggers the change of chosen photo_image
        # trigger -> command=self.display_image
        pass

    def display_image(self):
        self.open_image()
        if self.image:
            self.photo_image = ImageTk.PhotoImage(self.image)
        pass

    def open_image(self):
        # update (Properties.state) with the chosen image
        # get image from one of the Ed Pict, from properties.py class object
        pass


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ed Sheeran Photo Editor")
        self.geometry("1200x700")

        self.card = None  # shared model

        self.attributes_frame = AttributesFrame(self)
        self.preview_frame = PreviewFrame(self)
        self.photobook_frame = PhotobookFrame(self)

        self.attributes_frame.pack(side="left", fill="y")
        self.preview_frame.pack(side="left", expand=True, fill="both")
        self.photobook_frame.pack(side="right", fill="y")

    def create_widgets(self):
        pass

root.mainloop()