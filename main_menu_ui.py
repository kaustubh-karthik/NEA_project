import tkinter as tk
import main_game

screen = tk.Tk()

screen.geometry("1135x888")
screen.title("main menu gui")

def run():
    main_menu = tk.Frame(screen)
    main_menu.pack()
    main_menu.grid(row=0, column=0)

    bg_image = tk.PhotoImage(file = "bg_images/notes_falling_golden.png")
    bg_label = tk.Label(main_menu, image=bg_image)
    bg_label.pack()

    label = tk.Label(main_menu, text="CLICK TO PLAY", font=("Arial", 24))
    label.place(x=420, y=210)

    play_button_image = tk.PhotoImage(file = "bg_images/play_button.png")
    play_button = tk.Button(main_menu, text="PLAY", command=main_game.run, image=play_button_image, width=500, height=350)
    play_button.place(x=270, y=430)

    settings_screen = tk.Toplevel(screen)
    settings_screen.withdraw()
    settings_window = tk.Frame(settings_screen)
    settings_window.pack()
    title = tk.Label(settings_screen, text="SETTINGS PAGE", font=("Arial", 24))
    title.pack()
    
    fps_label = tk.Label(settings_screen, text="choose fps: ", font=("Arial", 24))
    fps_label.pack()
    fps_box = tk.Entry(settings_screen)
    fps_box.pack()
    
    note_speed_label = tk.Label(settings_screen, text="choose note_speed: ", font=("Arial", 24))
    note_speed_label.pack()
    note_speed_box = tk.Entry(settings_screen)
    note_speed_box.pack()
    
    num_lanes_label = tk.Label(settings_screen, text="choose num_lanes: ", font=("Arial", 24))
    num_lanes_label.pack()
    num_lanes_box = tk.Entry(settings_screen)
    num_lanes_box.pack()
    
    def write_text_file():
        note_speed = note_speed_box.get()
        fps = fps_box.get()
        num_lanes = num_lanes_box.get()
        
        with open("settings_vars.txt", "w") as vars:
            try:
                vars.write(f"{int(fps)} {int(note_speed)} {int(num_lanes)}")
            except ValueError:
                print("MUST BE INTEGER")

    submit_button = tk.Button(settings_screen, text="SUBMIT", command= write_text_file)
    submit_button.pack()

    settings_image = tk.PhotoImage(file = "bg_images/settingsbutton.png")
    settings_button = tk.Button(main_menu, command=settings_screen.deiconify, image=settings_image, width=100, height=100)
    settings_button.place(x=850, y=75)
    
    screen.mainloop()

if __name__ == "__main__":
    run()