import tkinter as tk
import main_game

screen = tk.Tk()

screen.geometry("1135x888")
screen.title("main menu gui")

main_menu = tk.Frame(screen)
main_menu.grid(row=0, column=0)

bg_image = tk.PhotoImage(file = "bg_images/notes_falling_golden.png")
bg_label = tk.Label(main_menu, image=bg_image)
bg_label.pack()

label = tk.Label(main_menu, text="CLICK TO PLAY", font=("Arial", 24))
label.place(x=420, y=210)

play_button_image = tk.PhotoImage(file = "bg_images/play_button.png")
play_button = tk.Button(main_menu, text="PLAY", command=main_game.run, image=play_button_image, width=500, height=350)
play_button.place(x=270, y=430)

settings_image = tk.PhotoImage(file = "bg_images/settingsbutton.png")
settings_button = tk.Button(main_menu, image=settings_image, width=100, height=100)
settings_button.place(x=850, y=75)


screen.mainloop()
