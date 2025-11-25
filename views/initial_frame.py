import tkinter as tk

class WelcomeOverlay(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.text = tk.Text(self, wrap="word")
        self.text.pack(side="left", fill="both", expand=True)

        self.overlay = tk.Label(self.text, text="Overlay Info", bg="white", relief="solid")
        self.overlay.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")

root = tk.Tk()
root.title("Overlay")
root.geometry("250x250")
label = tk.Label(root, text="This is an overlay", fg="white", bg="red", font=("Arial", 14))
label.pack()
root.mainloop()