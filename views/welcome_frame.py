import tkinter as tk
from tkinter import Toplevel
import os
from CardTemplatePicker import CardTemplatePicker
from PIL import Image, ImageTk
import overlay_images

def choose_image():

    templates = overlay_images.cards

    picker = CardTemplatePicker(root, templates)

    if picker.selected_image:
        lbl_result.config(text=f"Selected: {picker.selected_image}")

        template = Image.open(picker.selected_path)
        tk_template = ImageTk.PhotoImage(template)
        lbl_display.config(image=tk_template)
        lbl_display.image = template
    else:
        lbl_result.config(text="Selection cancelled")

    return tk_template


root = tk.Tk()
root.geometry("500x300")

label = tk.Label(root, text="Welcome to the Ed Sheeran card maker! To get started, select a template.")
label.pack(pady=20)

btn_open = tk.Button(root, text="Open Image Gallery", command=choose_image)
btn_open.pack(pady=20)

lbl_result = tk.Label(root, text="No image selected")
lbl_result.pack()

btn_continue = tk.Button(root, text="Continue to editor", command=root.destroy)
btn_continue.pack(pady=20)

lbl_display = tk.Label(root)
lbl_display.pack(pady=10)

root.mainloop()