import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

def create_table():
    conn = sqlite3.connect('manga.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS manga
                 (id INTEGER PRIMARY KEY, title TEXT, date_started TEXT, participants TEXT)''')
    conn.commit()
    conn.close()

def add_manga(title, date_started, participants):
    conn = sqlite3.connect('manga.db')
    c = conn.cursor()
    c.execute("INSERT INTO manga (title, date_started, participants) VALUES (?, ?, ?)", (title, date_started, participants))
    conn.commit()
    conn.close()

def view_data():
    conn = sqlite3.connect('manga.db')
    c = conn.cursor()
    c.execute("SELECT * FROM manga")
    rows = c.fetchall()
    conn.close()
    return rows

def delete_data(id):
    conn = sqlite3.connect('manga.db')
    c = conn.cursor()
    c.execute("DELETE FROM manga WHERE id=?", (id,))
    conn.commit()
    conn.close()

def submit_data():
    title = entry_title.get()
    date_started = entry_date.get() if entry_date.get() else datetime.now().strftime('%Y-%m-%d')
    participants = entry_participants.get().replace(" ", "").replace(",", ", ")
    add_manga(title, date_started, participants)
    messagebox.showinfo("Success", "Manga successfully added")
    update_list()

def update_list():
    for row in tree.get_children():
        tree.delete(row)
    for row in view_data():
        tree.insert('', 'end', values=row)

def delete_selected():
    selected_item = tree.selection()[0]
    id = tree.item(selected_item)['values'][0]
    delete_data(id)
    update_list()

create_table()

root = tk.Tk()
root.title("Manga Tracker")

label_title = tk.Label(root, text="Manga Title:")
label_title.grid(row=0, column=0, padx=5, pady=5)
entry_title = tk.Entry(root, justify='center')
entry_title.grid(row=0, column=1, padx=5, pady=5)

label_date = tk.Label(root, text="Date started (YYYY-MM-DD):")
label_date.grid(row=1, column=0, padx=5, pady=5)
entry_date = tk.Entry(root, justify='center')
entry_date.grid(row=1, column=1, padx=5, pady=5)

label_participants = tk.Label(root, text="Participants (separated by commas):")
label_participants.grid(row=2, column=0, padx=5, pady=5)
entry_participants = tk.Entry(root, justify='center')
entry_participants.grid(row=2, column=1, padx=5, pady=5)

submit_button = tk.Button(root, text="Add manga", command=submit_data)
submit_button.grid(row=3, column=1, padx=5, pady=5)

tree = ttk.Treeview(root, columns=('ID', 'Title', 'Date started', 'Participants'), show='headings')
tree.heading('ID', text='ID')
tree.heading('Title', text='Title')
tree.heading('Date started', text='Date started')
tree.heading('Participants', text='Participants')
tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

update_list()

delete_button = tk.Button(root, text="Delete selected", command=delete_selected)
delete_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
