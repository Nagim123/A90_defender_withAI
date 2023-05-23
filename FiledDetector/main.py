import tkinter as tk
import webbrowser
from tkinter import font
from tkinter import messagebox
from multiprocessing import Process, Pipe
from defender import defender_run

process, child_conn, parent_conn = None, None, None

def open_help():
    # Function to handle the "Help" button action
    print("Help button clicked")

def open_github():
    # Function to handle the "Github page" button action
    webbrowser.open("https://github.com/Nagim123/A90_defender_withAI")

def open_author():
    # Function to handle the "Author" button action
    messagebox.showinfo("Author", "This application was created by ChatGPT, some guys from github issues\nand by me - Nagim Isyanbaev, poor student from Russia...")

def increase_attack_count():
    # Function to increase the attack count by 1
    current_count = int(attack_count_label['text'].split(': ')[-1])
    new_count = current_count + 1
    attack_count_label.config(text=f"Number of attacks: {new_count}")

def start_action():
    # Function to handle the "START" button action
    if start_button['text'] == "START":
        start_button.config(text="STOP")
        start_subprocess()
    else:
        start_button.config(text="START")
        kill_subprocess()

def start_subprocess():
    global process, parent_conn, child_conn
    parent_conn, child_conn = Pipe()
    process = Process(target=defender_run, args=(child_conn,))
    process.daemon = True
    process.start()

def kill_subprocess():
    global process
    if process.is_alive():
        process.terminate()
        process.join()

def check_loop():
    global process, parent_conn, child_conn
    if process is None:
        window.after(100, check_loop)    
        return

    if not process.is_alive() and start_button['text'] == "STOP":
        start_button['text'] = "START"
    else:
        if parent_conn.poll():
            msg = parent_conn.recv()
            if msg[0] == 1:
                messagebox.showerror("Error", msg[1])
            elif msg[0] == 0:
                increase_attack_count()
    window.after(100, check_loop)


if __name__ == '__main__':
    
    # Create the main window
    window = tk.Tk()

    # Set the window title
    window.title("A90 defender")

    window.geometry("270x150")
    window.resizable(False, False)

    # Create the top menu strip
    menubar = tk.Menu(window)
    about_menu = tk.Menu(menubar, tearoff=0)
    about_menu.add_command(label="Github page", command=open_github)
    about_menu.add_command(label="Author", command=open_author)
    menubar.add_cascade(label="Help", command=open_help)
    menubar.add_cascade(label="About", menu=about_menu)


    # Add the top menu strip to the window
    window.config(menu=menubar)

    button_font = font.Font(size=16)
    # Create the "START" button
    start_button = tk.Button(window, text="START", width=12, height=2, font=button_font, command=start_action)
    start_button.pack(pady=25)

    attack_count_label = tk.Label(window, text='Number of attacks: 0')
    attack_count_label.pack()
    check_loop()
    # Run the Tkinter event loop
    window.mainloop()