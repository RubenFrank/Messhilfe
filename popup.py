import tkinter as tk
from tkinter import ttk

def show_data(array1,array2,unit1,unit2):
    root=tk._default_root
    popup=tk.Toplevel(root)
    popup.title("Messdaten")
    popup.geometry("400x500")

    popup.grab_set()

    # Erstellen eines Treeviews zur Anzeige der Messdaten
    tabel=ttk.Treeview(popup, columns=("Messung","Port 1", "Port 2"), show="headings")
    tabel.heading("Messung", text="Messung:")
    tabel.heading("Port 1", text=f"Port 1 [{unit1}]")
    tabel.heading("Port 2", text=f"Port 2 [{unit2}]")
    tabel.column("Messung", width=70,minwidth=70, anchor="center",stretch=False)
    tabel.column("Port 1", width=100,minwidth=100, anchor="center") 
    tabel.column("Port 2", width=100,minwidth=100, anchor="center")  

    # Hinzufügen der Daten zur Tabelle
    for i in range(len(array1)):
        tabel.insert("", "end", values=(i+1, array1[i], array2[i]))

    scrollbar=ttk.Scrollbar(popup, orient="vertical",command=tabel.yview )
    tabel.configure(yscrollcommand=scrollbar.set)
    
    scrollbar.pack(side="right", fill="y")
    tabel.pack(side="left" ,fill="both", expand=True)
    