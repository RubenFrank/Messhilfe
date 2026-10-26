#-------------------------------------------------------------------------------------------------
#-----------------------------------Messhilfe Unterprogramm: File Handling -----------------------
#-------------------------------------------------------------------------------------------------
# Beschreibung: die Speicherung der Messwerte in einer XLSX-Datei (Excel) wird in diesem Unterprogramm realisiert
# -------------------------------------------------------------------------------------------------
# Autor:        Ruben Frank (et24014), Tobias Pfau (et24068)
# -------------------------------------------------------------------------------------------------
# Datum:        2026-10-20
# ------------------------------------------------------------------------------------------------- 

from tkinter import filedialog, messagebox
import pandas as pd
#import numpy as np
import datetime 
#import os

def save_data_to_csv(save_idx , measure_data1, measure_data2, unit1, unit2 ):
    filepath, file_exist = choose_file()
    print(f"Speicherpfad: {filepath}")

    if file_exist:
        #df = pd.read_csv(filepath)
        df = pd.DataFrame([measure_data1, measure_data2]).T
        df.to_csv(filepath, mode='a', header=False, index=False)
    else:
        df = pd.DataFrame({f"Messwert Port 1 [{unit1}]": measure_data1, f"Messwert Port 2 [{unit2}]": measure_data2})
        df.to_csv(filepath, mode='w', header=True, index=False)

    
    

def create_file():
    date=datetime.datetime.now().strftime("%Y%m%d")
    filepath=filedialog.asksaveasfile(title="Datei erstellen",defaultextension=".csv" , filetypes=[("CSV-Dateien", "*.csv")], initialfile=f"Messung_{date}")
    
    return filepath.name

def open_file():
    filepath=filedialog.askopenfilename(title="Datei auswählen", filetypes=[("CSV-Datei","*.csv"), ("Alle Dateien", "*.*")])
    return filepath

def choose_file():
    file_exist=messagebox.askyesno(title="Datei vorhanden", message="Existiert eine Datei, in die die Daten gespeichert werden soll?",icon="question")
    print(f"Datei vorhanden: {file_exist}")
    if file_exist:
        filepath = open_file()
    else:
        filepath = create_file()

    return filepath, file_exist


if __name__ == "__main__":
    save_data_to_csv(0, [1,2,3], [4,5,6], "V", "A")