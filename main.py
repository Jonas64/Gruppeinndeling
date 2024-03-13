import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Setup
r = tk.Tk()
r.title("Gruppeinndeling")
r.geometry("420x720")
r.tk.call("source", "azure.tcl")
r.tk.call("set_theme", "dark")

# Variabler
names = []
current_name = tk.StringVar()
num_groups = tk.IntVar()
num_groups.set(2)
num_groups_num_ppl = tk.IntVar()
num_groups_num_ppl.set(0)

# Functions
def add_name(): # Legg til et navn
    if current_name.get() == "": # Hvis brukere ikke har skrevet noe
        messagebox.showerror("Feil", "Skriv et navn.")
    elif current_name.get() in names: # Hvis navnet allerede er i lista
        messagebox.showerror("Feil", "Navnet er allerde i lista.")
    else: # Ingen problemer
        names.append(current_name.get()) # Legg til navnet som en string i names lista
        name_list.insert(names.index(current_name.get()), current_name.get()) # Legg til navnet i lista som vises

def delete_names(): # Slett de valgte navnene
    selected_item = name_list.curselection()
    for item in selected_item[::-1]:
        name_list.delete(item)
        del names[item]

def change_num_groups_num_ppl(): # Bytte mellom å velg antall folk i hver gruppe og antall grupper
    if num_groups_num_ppl.get():
        num_groups_spinbox.config(state=tk.NORMAL)
    else:
        num_groups_spinbox.config(state=tk.DISABLED)


# Frames
add_name_frame = ttk.Frame(r)
num_groups_frame = ttk.Frame(r)
num_groups_num_ppl_check_frame = ttk.Frame(r)


# Lage alle widgetsa
name_list = tk.Listbox(r, selectmode=tk.EXTENDED, font=("TkDefaultFont", 14))

add_name_entry = ttk.Entry(add_name_frame, textvariable=current_name) # Skrive inn navn
add_name_btn = ttk.Button(add_name_frame, text="Legg til", command=add_name)

remove_name_btn = ttk.Button(r, text="Slett valgte", command=delete_names)

num_groups_num_ppl_check = tk.Checkbutton(num_groups_num_ppl_check_frame, variable=num_groups_num_ppl, onvalue=1, offvalue=0, command=change_num_groups_num_ppl)
num_groups_num_ppl_lbl = tk.Label(num_groups_num_ppl_check_frame, text="Antall grupper / Antall per gruppe")

num_groups_lbl = ttk.Label(num_groups_frame, text="Antall grupper:")
num_groups_spinbox = ttk.Spinbox(num_groups_frame, textvariable=num_groups, from_=2, to=999, increment=1, state=tk.DISABLED)


# Pack alle tingene
add_name_frame.pack(side=tk.TOP, pady=20)
name_list.pack(fill="x", padx=30)
remove_name_btn.pack(pady=10)
add_name_entry.pack(side=tk.LEFT, padx=10)
add_name_btn.pack(side=tk.RIGHT, padx=10)

num_groups_num_ppl_check_frame.pack()
num_groups_num_ppl_check.pack(side=tk.RIGHT)
num_groups_num_ppl_lbl.pack(side=tk.LEFT)

num_groups_frame.pack()
num_groups_lbl.pack(side=tk.LEFT, padx=10)
num_groups_spinbox.pack(side=tk.RIGHT, padx=10)


r.mainloop()
