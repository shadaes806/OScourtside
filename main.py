import tkinter as tk

# Create the main window
root = tk.Tk()

# Set the window title and size
root.title("Courtside OS - CPU Scheduling Simulator")
root.geometry("800x600")

# Create the heading
title = tk.Label(root,text="COURTSIDE OS 🏀", font=("Arial", 24, "bold"))
title.pack(pady=20)

# Create the description
description = tk.Label(root, text="Where Basketball Meets Operating Systems",font=("Arial", 12))
description.pack()

# Keep the window open
root.mainloop()