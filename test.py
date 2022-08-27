from tkinter import *
class App(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Wordpress Downloader')
        self.geometry("700x600")
        self.frame = Frame()
        self.label = Label(master = self.frame,text="this a label")
        self.label.pack()
        self.frame.pack()
if __name__ == "__main__":
    app = App()
    app.mainloop()