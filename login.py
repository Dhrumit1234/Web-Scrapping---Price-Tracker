import tkinter as tk
from tkinter import messagebox
import mysql.connector
import subprocess  # To open another Python file

# MySQL connection setup
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="webscrapping"
)
cursor = db.cursor()

def login():
    username = username_entry.get()
    password = password_entry.get()

    query = "SELECT * FROM login WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    if result:
        messagebox.showinfo("Login", "Login successful!")
        root.destroy()
        open_mainpage()
    else:
        messagebox.showerror("Login", "Invalid username or password")

def open_mainpage():
    try:
        # Opens mainpage.py after login
        subprocess.Popen(["python", "mainpage.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open main page: {e}")

# --- Login GUI ---
root = tk.Tk()
root.title("Login Page")
root.geometry("350x250")
root.configure(bg="#e1f5fe")  # Light blue background

# Center the window on the screen
window_width = 350
window_height = 250
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))
root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

# Title Label
title_label = tk.Label(
    root, 
    text="Please Login", 
    font=("Helvetica", 18, "bold"),
    bg="#e1f5fe",
    fg="#0277bd"
)
title_label.pack(pady=15)

# Username
tk.Label(root, text="Username:", font=("Helvetica", 12), bg="#e1f5fe").pack(pady=(10, 0))
username_entry = tk.Entry(root, font=("Helvetica", 12), width=30)
username_entry.pack(pady=5)

# Password
tk.Label(root, text="Password:", font=("Helvetica", 12), bg="#e1f5fe").pack(pady=(10, 0))
password_entry = tk.Entry(root, font=("Helvetica", 12), show="*", width=30)
password_entry.pack(pady=5)

# Login Button
tk.Button(
    root,
    text="Login",
    font=("Helvetica", 14),
    bg="#0288d1",
    fg="white",
    activebackground="#0277bd",
    padx=10,
    pady=5,
    command=login
).pack(pady=20)

root.mainloop()
