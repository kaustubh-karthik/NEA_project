import tkinter as tk

root = tk.Tk()
root.title("Menu")
frame = tk.Frame(root)
frame.pack()
play_button = tk.Button(frame, text="Play")
play_button.pack(side=tk.BOTTOM)
settings_button = tk.Button(frame, text="Settings")
settings_button.pack(side=tk.TOP, anchor=tk.E)

new_window = tk.Toplevel(root)
new_window.withdraw()
frame2 = tk.Frame(new_window)
frame2.pack()
label1 = tk.Label(frame2, text="Variable 1:")
label1.pack(side=tk.LEFT)
entry1 = tk.Entry(frame2)
entry1.pack(side=tk.LEFT)
label2 = tk.Label(frame2, text="Variable 2:")
label2.pack(side=tk.LEFT)
entry2 = tk.Entry(frame2)
entry2.pack(side=tk.LEFT)

def show_settings():
    new_window.deiconify()

settings_button.config(command=show_settings)

root.mainloop()