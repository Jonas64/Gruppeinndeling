import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import random, csv

# Setup
r = tk.Tk()
r.title("Gruppeinndeling")
r.geometry("520x820")
r.tk.call("source", "azure.tcl")
r.tk.call("set_theme", "dark")
r.resizable(False, False)

# Variabler
names = []
current_name = tk.StringVar()
num_groups = tk.IntVar()
num_groups.set(2)
num_ppl_per_group = tk.IntVar()
num_ppl_per_group.set(2)
num_groups_num_ppl = tk.IntVar()
num_groups_num_ppl.set(0)
file_name = tk.StringVar()
disabled_color = "#666"
normal_color = "#fff"
folder_directory = ""
groups = []
advanced_btn_text = ["Avanserte alternativer v", "Avanserte alternativer ^"]
separated = []


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

def import_names():
    global names
    file_path = filedialog.askopenfilename(filetypes=[("Comma-separated Values", "*.csv")])
    temp_names = []
    with open(file_path, "r") as f:
        temp_names = f.readlines()
    
    names = []
    for n in temp_names:
        a = n.strip().split(",")
        while "" in a:
            a.remove("")
        for name in a:
            names.append(name.replace(" ", ""))
    
    name_list.delete(0, tk.END)
    i = 0
    for n in names:
        name_list.insert(i, n)
        i += 1
    
def change_num_groups_num_ppl(): # Bytte mellom å velg antall folk i hver gruppe og antall grupper
    if num_groups_num_ppl.get():
        num_groups_spinbox.config(state=tk.DISABLED)
        num_ppl_per_group_spinbox.config(state=tk.NORMAL)
        num_ppl_per_group_lbl.config(foreground=normal_color)
        num_groups_lbl.config(foreground=disabled_color)
        num_groups_num_ppl_lbl1.config(foreground=disabled_color)
        num_groups_num_ppl_lbl3.config(foreground=normal_color)
        r.update_idletasks()
    else:
        num_groups_spinbox.config(state=tk.NORMAL)
        num_ppl_per_group_spinbox.config(state=tk.DISABLED)
        num_ppl_per_group_lbl.config(foreground=disabled_color)
        num_groups_lbl.config(foreground=normal_color)
        num_groups_num_ppl_lbl1.config(foreground=normal_color)
        num_groups_num_ppl_lbl3.config(foreground=disabled_color)
        r.update_idletasks()

def generate_groups():
    global groups, groups_listboxes, groups_listboxes_frame
    if not num_groups_num_ppl.get(): # Hvis brukeren valgte antall grupper
        num_groups_ = num_groups.get()
        group_size = len(names) // num_groups_
    else: # Hvis brukeren valgte antall per gruppe
        group_size = num_ppl_per_group.get()
        num_groups_ = len(names)//group_size
        if len(names)%group_size != 0:
            num_groups_ += 1

    if len(names) < num_groups_: # Feilmeldinger
        messagebox.showerror("Feil", f"Skriv minst {num_groups_}(antall grupper) navn.")
        return
    elif len(names) < group_size:
        messagebox.showerror("Feil", f"Skriv minst {group_size}(antall per gruppe) navn.")
        return
    else:
        names_shuffle = names.copy()
        separated_bool = False # Anta at de ikke er separert
        while not separated_bool:
            random.shuffle(names_shuffle) # Tilfeldig rekkefølge på navn liste
            groups = []
            if len(names)%num_groups_ == 0: # Hvis antall personer kan deles på antall grupper
                start = 0
                for i in range(num_groups_): # Velg en del av names_shuffle og lag en gruppe av de
                    end = min(start+group_size, len(names_shuffle))
                    group = names_shuffle[start:end]
                    groups.append(group)
                    start = end
            else: # Hvis antall personer og antall grupper ikke går opp
                start = 0
                for i in range(num_groups_):
                    end = min(start+group_size, len(names_shuffle))
                    group = names_shuffle[start:end]
                    groups.append(group)
                    start = end
                not_in_group = [] # Legge til navnene som ikke ble inkludert (blir ujevne grupper)
                in_group = []
                for g in groups: # For group in groups:
                    for n in g: # For name in group:
                        in_group.append(n)
                for n in names:
                    if n not in in_group:
                        not_in_group.append(n)
                i = 0
                for n in not_in_group: # Legge til navnene som ikke ble med
                    i = i%num_groups_
                    groups[i].append(n)
                    i += 1
            if separated != []: # Hvis brukeren vil separere to personer
                for group in groups:
                    if separated[0] in group and separated[1] in group: # Hvis begge er i samme gruppe
                        separated_bool = False
                    else:
                        separated_bool = True
            else:
                separated_bool = True
            print(separated)

    groups_listboxes_frame.destroy() # Destroy frame og alle listboxes i den (fjerne forrige grupper som ble generert)
    groups_listboxes = []
    groups_listboxes_frame = ttk.Frame(r)

    i = 0
    for g in groups:
        groups_listboxes.append(tk.Listbox(groups_listboxes_frame, width=int((r.winfo_width()//len(groups))//7.2))) # Legg til listbox
        j = 0
        for n in g: # LEgg til alle navnene i riktig listbox
            groups_listboxes[i].insert(j, n)
            j += 1
        i += 1
    for listbox in groups_listboxes: # Pack alle listboxene
        listbox.pack(side=tk.LEFT)
    groups_listboxes_frame.pack()

def select_directory():
    global folder_directory
    folder_directory = filedialog.askdirectory()+"/"
    directory_lbl.config(text=folder_directory)

def export_groups():
    file_nm = file_name.get()
    if file_nm == "" or folder_directory == "":
        messagebox.showerror("Feil", "Velg en mappe og filnavn.")
        return
    if file_nm[len(file_nm)-4:len(file_nm)-1] != ".csv": # Legg til .csv hvis filnavnet ikke har det
        file_nm += ".csv"

    with open(folder_directory+file_nm, "w") as f: # Skriv alle gruppene til csv fil
        writer = csv.writer(f)
        writer.writerows(groups)
        f.close()

def open_advanced():
    if advanced_options_btn.cget("text") == advanced_btn_text[0]:
        advanced_options_btn.config(text=advanced_btn_text[1]) # Bytt tekst (pil) på knapp
        for child in advanced_options_frame.winfo_children(): # Vis avanserte alternativer
            child.pack(pady=5)
    else:
        advanced_options_btn.config(text=advanced_btn_text[0]) # Bytt tekst (pil) på knapp
        for child in advanced_options_frame.winfo_children(): # Fjern avanserte alternativer
            child.pack_forget()

def set_not_in_group(): # Velg to personer som ikke skal være i samme gruppe
    global separated
    selected_names_i = []
    for i in name_list.curselection():
        selected_names_i.append(i)

    if len(selected_names_i) != 2:
        messagebox.showerror("Feil", f"Velg to navn. (du har valgt {len(selected_names_i)})")
        return

    selected_names = []
    for i in selected_names_i:
        selected_names.append(names[i])
    
    separated = selected_names

def reset_advanced(): # Reset alle avanserte alternativer
    global separated
    separated = []



# Frames
add_name_frame = ttk.Frame(r)
remove_name_import_name_frame = ttk.Frame(r)
num_groups_frame = ttk.Frame(r)
num_ppl_per_group_frame = ttk.Frame(r)
num_groups_num_ppl_check_frame = ttk.Frame(r)
groups_listboxes_frame = ttk.Frame(r)
choose_directory_frame = ttk.Frame(r)
directory_lbl_frame = ttk.Frame(r)
advanced_options_frame = ttk.Frame(r)

# Widgets
name_list = tk.Listbox(r, selectmode=tk.EXTENDED, font=("TkDefaultFont", 14))

add_name_entry = ttk.Entry(add_name_frame, textvariable=current_name)
add_name_btn = ttk.Button(add_name_frame, text="Legg til", command=add_name)

remove_name_btn = ttk.Button(remove_name_import_name_frame, text="Slett valgte", command=delete_names)
import_names_btn = ttk.Button(remove_name_import_name_frame, text="Importer navn", command=import_names)

num_groups_num_ppl_check = ttk.Checkbutton(num_groups_num_ppl_check_frame, variable=num_groups_num_ppl, onvalue=1, offvalue=0, command=change_num_groups_num_ppl)
num_groups_num_ppl_lbl1 = ttk.Label(num_groups_num_ppl_check_frame, text="Antall grupper", foreground=normal_color)
num_groups_num_ppl_lbl2 = ttk.Label(num_groups_num_ppl_check_frame, text=" / ")
num_groups_num_ppl_lbl3 = ttk.Label(num_groups_num_ppl_check_frame, text="Antall per gruppe", foreground=disabled_color)

num_groups_lbl = ttk.Label(num_groups_frame, text="Antall grupper:")
num_groups_spinbox = ttk.Spinbox(num_groups_frame, textvariable=num_groups, from_=2, to=999, increment=1, state=tk.NORMAL)

num_ppl_per_group_lbl = ttk.Label(num_ppl_per_group_frame, text="Antall per gruppe:", foreground=disabled_color)
num_ppl_per_group_spinbox = ttk.Spinbox(num_ppl_per_group_frame, textvariable=num_ppl_per_group, from_=2, to=999, increment=1, state=tk.DISABLED)

advanced_options_btn = ttk.Button(r, text=advanced_btn_text[0], command=open_advanced)
not_in_group_btn = ttk.Button(advanced_options_frame, text="Separer", command=set_not_in_group)
reset_advanced_btn = ttk.Button(advanced_options_frame, text="Reset avanserte alternativer", command=reset_advanced)

generate_groups_btn = ttk.Button(r, text="Generer grupper", command=generate_groups)
groups_listboxes = []

choose_directory_btn = ttk.Button(choose_directory_frame, text="Velg plassering", command=select_directory)
file_name_lbl = ttk.Label(choose_directory_frame, text="Filnavn: ")
file_name_entry = ttk.Entry(choose_directory_frame, textvariable=file_name)
directory_lbl = ttk.Label(directory_lbl_frame, text="")
file_name_directory_lbl = ttk.Label(directory_lbl_frame, textvariable=file_name)
export_btn = ttk.Button(r, text="Eksporter", command=export_groups)


# Pack alle tingene
add_name_frame.pack(side=tk.TOP, pady=20)
name_list.pack(fill="x", padx=30)
remove_name_btn.pack(side=tk.LEFT, padx=5)
import_names_btn.pack(side=tk.RIGHT, padx=5)
remove_name_import_name_frame.pack(pady=10)
add_name_entry.pack(side=tk.LEFT, padx=10)
add_name_btn.pack(side=tk.RIGHT, padx=10)

num_groups_num_ppl_check_frame.pack(pady=10)
num_groups_num_ppl_check.pack(side=tk.RIGHT)
num_groups_num_ppl_lbl1.pack(side=tk.LEFT)
num_groups_num_ppl_lbl2.pack(side=tk.LEFT)
num_groups_num_ppl_lbl3.pack(side=tk.LEFT)

num_groups_frame.pack()
num_groups_lbl.pack(side=tk.LEFT, padx=10)
num_groups_spinbox.pack(side=tk.RIGHT, padx=10)

num_ppl_per_group_frame.pack(pady=5)
num_ppl_per_group_lbl.pack(side=tk.LEFT, padx=10)
num_ppl_per_group_spinbox.pack(side=tk.RIGHT, padx=10)


advanced_options_btn.pack(pady=5)
advanced_options_frame.pack()

generate_groups_btn.pack(pady=10)
groups_listboxes_frame.pack()

choose_directory_btn.pack(side=tk.LEFT, padx=20)
file_name_lbl.pack(side=tk.LEFT)
file_name_entry.pack(side=tk.RIGHT)
choose_directory_frame.pack()
directory_lbl.pack(pady=5, side=tk.LEFT)
file_name_directory_lbl.pack(side=tk.RIGHT)
directory_lbl_frame.pack()
export_btn.pack()

r.mainloop()
