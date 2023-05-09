import tkinter as tk
import main_game

screen = tk.Tk()

screen.geometry("1135x888")
screen.title("main menu gui")

bg_image = tk.PhotoImage(file = "bg_images/notes_falling_golden.jpg")
bg_label = tk.Label(screen, image=bg_image)
bg_label.pack()


label = tk.Label(screen, text="CLICK TO PLAY", font=("Arial", 24))
label.place(x=480, y=210)

play_button = tk.Button(screen, text="PLAY", command=main_game.run, width=30, height=3)
play_button.place(x=470, y=430)

screen.mainloop()
