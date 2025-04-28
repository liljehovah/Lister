# program: M06 Final Project: Lister (Version 1)
# author: ejm
# created: 2025-04-27
# ide: Visual Studio Code
# purpose: simple GUI note taking app
# NO CODING ASSISTANCE was used in this program

# pseudo code
# import relevant modules
# define main window
# define create new note
# define load existing note
# define note taking window
# start program

# import relevant modules
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

# create directory for saving notes
NOTES_DIR = os.path.join(os.path.dirname(__file__), 'data', 'notes')
os.makedirs(NOTES_DIR, exist_ok=True)

# define main window
def create_main_window():
    root = tk.Tk()
    root.title('Lister by ejm')
    root.geometry('400x300')

    title = tk.Label(root, text='Lister by ejm', font=('Arial', 20))
    title.pack(pady=20)

    btn_new = tk.Button(root, text='Create New Note', width=20, command=create_new_note)
    btn_new.pack(pady=10)

    btn_load = tk.Button(root, text='Load Existing Note', width=20, command=load_existing_note)
    btn_load.pack(pady=10)

    btn_exit = tk.Button(root, text='Exit', width=20, command=root.quit)
    btn_exit.pack(pady=10)

    root.mainloop()

# define create new note
def create_new_note():
    note_window(editing=False)

# define load existing note
def load_existing_note():
    files = os.listdir(NOTES_DIR)
    if not files:
        messagebox.showinfo('No Notes', 'No notes found to load.')
        return

    load_window = tk.Toplevel()
    load_window.title('Load Note')
    load_window.geometry('300x400')

    file_listbox = tk.Listbox(load_window)
    file_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    for file in files:
        file_listbox.insert(tk.END, file)

    def open_selected_file():
        selected = file_listbox.curselection()
        if selected:
            filename = file_listbox.get(selected[0])
            filepath = os.path.join(NOTES_DIR, filename)
            load_window.destroy()
            note_window(filepath)

    btn_open = tk.Button(load_window, text='Open', command=open_selected_file)
    btn_open.pack(pady=5)

# define note taking window
def note_window(filepath=None, editing=True):
    window = tk.Toplevel()
    window.title('Edit Note' if filepath else 'New Note')
    window.geometry('500x500')

    text_area = tk.Text(window, wrap=tk.WORD)
    text_area.pack(fill=tk.BOTH, expand=True)

    if filepath:
        with open(filepath, 'r') as f:
            content = f.read()
            text_area.insert(tk.END, content)

    def save_note():
        content = text_area.get('1.0', tk.END).strip()
        if not content:
            messagebox.showwarning('Empty Note', 'Cannot save an empty note.')
            return

        if filepath:
            save_path = filepath
        else:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            save_path = os.path.join(NOTES_DIR, f'{timestamp}.txt')

        with open(save_path, 'w') as f:
            f.write(content)

        messagebox.showinfo('Saved', f'Note saved to {save_path}')
        window.destroy()

    btn_frame = tk.Frame(window)
    btn_frame.pack(fill=tk.X)

    btn_save = tk.Button(btn_frame, text='Save', command=save_note)
    btn_save.pack(side=tk.LEFT, padx=10, pady=5)

    btn_quit = tk.Button(btn_frame, text='Quit Without Saving', command=window.destroy)
    btn_quit.pack(side=tk.RIGHT, padx=10, pady=5)

# start program
create_main_window()