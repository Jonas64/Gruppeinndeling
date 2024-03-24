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
together = []


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

def check_name(name, group, names, group_size): # Sjekke om en person kan være i en gruppe
    name_sep = [] # Navn som personen ikke kan være med
    for sep in separated:
        if name in sep:
            if name == sep[0]:
                name_sep.append(sep[1])
            else:
                name_sep.append(sep[0])
    name_t = [] # Navn som personen må være med
    for t in together:
        if name in t:
            if name == t[0]:
                name_t.append(t[1])
            else:
                name_t.append(t[0])
    
    for sep in name_sep:
        if sep in group: # Hvis et av navnene som personen ikke kan være med er i gruppa
            return False
    for t in name_t:
        if t in names:
            return False
        else:
            if t not in group: # Hvis et av navnene som personen må være med ikke er i gruppa
                return False
    if len(group) == group_size:
        return False
    return True

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
        together_dict = {} # Alle navnene som skal være sammen med noen og hvem de skal være sammen med
        for t in together:
            for n in t:
                together_dict[n] = []
        for name in together_dict:
            for t in together:
                if name in t:
                    if name == t[0]:
                        together_dict[name].append(t[1])
                    else:
                        together_dict[name].append(t[0])
        
        separated_dict = {} # Alle navnene som skal være separert med noen og hvem de skal være separert med
        for sep in separated:
            for n in sep:
                separated_dict[n] = []
        for name in separated_dict:
            for sep in separated:
                if name in sep:
                    if name == sep[0]:
                        separated_dict[name].append(sep[1])
                    else:
                        separated_dict[name].append(sep[0])
        
        names_shuffle = [1]

        outer_loop_count = 0
        while len(names_shuffle) > 0 and outer_loop_count < 100: # Hvis det ikke gikk å generere grupper, lag ny names_shuffle og prøv igjen
            names_shuffle = names.copy() # Lag ny names_shuffle hvis det ikke gikk
            random.shuffle(names_shuffle)

            groups = []
            for i in range(num_groups_):
                groups.append([])

            i = 0
            loop_count = 0
            while len(names_shuffle) > 0 and loop_count < 100: # Generere grupper med names_shuffle
                to_remove = []
                for name in names_shuffle: # Sett folk inn i grupper
                    separated_ok = True
                    if name in separated_dict:
                        for sep_name in separated_dict[name]:
                            if sep_name in groups[i]:
                                separated_ok = False

                    together_ok = True
                    if name in together_dict:
                        for t_name in together_dict[name]:
                            groups_empty = True
                            for g_i, group in enumerate(groups):
                                for t in together_dict[name]:
                                    if t in group and g_i != i: # Hvis den som navnet må være med er i en annen gruppe
                                        together_ok = False
                                if group != []:
                                    groups_empty = False
                            
                            if t_name not in groups[i] and not groups_empty: # Hvis navnet ikke er i gruppa og gruppene ikke er tomme
                                together_ok = False

                    if separated_ok and together_ok: # Sjekke om navnet går i gruppa
                        groups[i].append(name)
                        to_remove.append(name)
                        i += 1
                        i %= num_groups_
                
                if len(to_remove) == 0:
                    i += 1
                    i %= num_groups_

                for n in to_remove:
                    if n in names_shuffle:
                        names_shuffle.remove(n)
                loop_count += 1
            outer_loop_count += 1
        
    groups_listboxes_frame.destroy() # Destroy frame og alle listboxes i den (fjerne forrige grupper som ble generert)
    groups_listboxes = []
    groups_listboxes_frame = ttk.Frame(r)

    i = 0
    for g in groups:
        groups_listboxes.append(tk.Listbox(groups_listboxes_frame, width=int((r.winfo_width()//len(groups))//7.2))) # Legg til listbox
        j = 0
        for n in g: # Legg til alle navnene i riktig listbox
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

    if selected_names in separated or [selected_names[1], selected_names[0]] in separated: # Hvis navnene allerede er separert
        messagebox.showerror("Feil", f"Navnene er allerede separert. ({''.join(selected_names)})")
        return
    
    if selected_names in together or [selected_names[1], selected_names[0]] in together: # Hvis navnene allerede er sammen
        messagebox.showerror("Feil", f"Du kan ikke både separere og sette sammen to navn.")
        return
    
    separated.append(selected_names)
    sep_string = ""
    for sep in separated: # Konverter separated lista til en string som skal vises på en Label
        sep_string += " | ".join(sep)
        sep_string += ",  "
    sep_string = sep_string[:-3] # Fjern siste komma siden det ikke er noe etter det
    not_in_group_lbl.config(text=sep_string) # Oppdater Label

def set_in_group():
    global together
    selected_names_i = []
    for i in name_list.curselection():
        selected_names_i.append(i)

    if len(selected_names_i) != 2:
        messagebox.showerror("Feil", f"Velg to navn. (du har valgt {len(selected_names_i)})")
        return

    selected_names = []
    for i in selected_names_i:
        selected_names.append(names[i])

    if selected_names in together or [selected_names[1], selected_names[0]] in together: # Hvis navnene allerede er separert
        messagebox.showerror("Feil", f"Navnene er allerede sammen. ({''.join(selected_names)})")
        return
    
    if selected_names in separated or [selected_names[1], selected_names[0]] in separated: # Hvis navnene allerede er separert
        messagebox.showerror("Feil", f"Du kan ikke både separere og sette sammen to navn.")
        return
    
    together.append(selected_names)
    together_string = ""
    for sep in together: # Konverter separated lista til en string som skal vises på en Label
        together_string += " - ".join(sep)
        together_string += ",  "
    together_string = together_string[:-3] # Fjern siste komma siden det ikke er noe etter det
    set_in_group_lbl.config(text=together_string) # Oppdater Label

def reset_advanced(): # Reset alle avanserte alternativer
    global separated, together
    together = []
    separated = []
    not_in_group_lbl.config(text="")
    set_in_group_lbl.config(text="")



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
not_in_group_frame = ttk.Frame(advanced_options_frame)
set_in_group_frame = ttk.Frame(advanced_options_frame)

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
not_in_group_btn = ttk.Button(not_in_group_frame, text="Separer", command=set_not_in_group)
not_in_group_lbl = ttk.Label(not_in_group_frame, text="")
set_in_group_btn = ttk.Button(set_in_group_frame, text="Sett sammen", command=set_in_group)
set_in_group_lbl = ttk.Label(set_in_group_frame, text="")
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
add_name_frame.pack(side=tk.TOP, pady=10)
name_list.pack(fill="x", padx=30)
remove_name_btn.pack(side=tk.LEFT, padx=5)
import_names_btn.pack(side=tk.RIGHT, padx=5)
remove_name_import_name_frame.pack(pady=5)
add_name_entry.pack(side=tk.LEFT, padx=10)
add_name_btn.pack(side=tk.RIGHT, padx=10)

num_groups_num_ppl_check_frame.pack(pady=5)
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

not_in_group_btn.pack()
not_in_group_lbl.pack()
set_in_group_btn.pack()
set_in_group_lbl.pack()
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
export_btn.pack(pady=5)

r.mainloop()
