import tkinter as tk

screen = tk.Tk()

screen.geometry("1135x888")
screen.title("main menu gui")

settings_screen = tk.Frame(screen)

title = tk.Label(settings_screen, text="SETTINGS PAGE", font=("Arial", 24))
title.place(x=420, y=75)

screen.mainloop()