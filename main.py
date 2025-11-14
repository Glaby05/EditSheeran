import tkinter as tk

# Window / Root with fixed size
# put Frames as partitions of the app:
#   - to divide the app into different main parts
#   -> left: options for Ed Sheeran pictures (1/4 of window vertically)
#   -> middle: the main editing Frame/scene  (2-3/4 of window vertically)
#   -> right: (last quarter of window vertically)
#       -> top:
#       -> bottom: display the last update of the picture
#


class CommandField(tk.Frame):
    def __init__(self, parent, label=''):
        super().__init__(parent)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

    def create_widgets(self):
        pass



