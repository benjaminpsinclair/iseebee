import tkinter as tk
from tkinter import scrolledtext

class Window:
    def __init__(self, title, geometry):
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry(geometry) 
        self.messageLabel = scrolledtext.ScrolledText(self.window, width = 300, height = 600)
        self.messageLabel.grid(row=0, column=0)
        self.messageLabel.pack()
   
    def displayMessage(self, message):
        self.messageLabel.insert(tk.INSERT, message)
        #self.messageLabel.configure(state='disabled')
    def update(self):
        self.window.update()
#TODO update text box function 
