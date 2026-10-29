#-------------------------------------------------------------------------------------------------
#-----------------------------------Messhilfe Unterprogramm: File Handling -----------------------
#-------------------------------------------------------------------------------------------------
# Beschreibung: die Speicherung der Messwerte in einer csv-Datei wird in diesem Unterprogramm realisiert
# -------------------------------------------------------------------------------------------------
# Autor:        Ruben Frank (et24014), Tobias Pfau (et24068)
# -------------------------------------------------------------------------------------------------
# Datum:        2026-10-20
# ------------------------------------------------------------------------------------------------- 

from tkinter import filedialog, messagebox
import pandas as pd
#import numpy as np
import datetime 
import re
#import os

def save_data_to_csv(save_path,save_idx, measure_data1, measure_data2, unit1, unit2 ):
    if save_path is None:
        filepath, file_exist = choose_file()
        print(f"Speicherpfad: {filepath}")

        if filepath is None:
            return None
        if file_exist:
            #df = pd.read_csv(filepath)
            df = pd.DataFrame([measure_data1, measure_data2]).T
            df.to_csv(filepath, mode='a', header=False, index=False)
        else:
            df = pd.DataFrame({f"Messwert Port 1 [{unit1}]": measure_data1, f"Messwert Port 2 [{unit2}]": measure_data2})
            df.to_csv(filepath, mode='w', header=True, index=False)
        return filepath
    else:
        df = pd.DataFrame([measure_data1[save_idx:], measure_data2[save_idx:]])
        df.to_csv(save_path, mode='a', header=False, index=False)
        return save_path


def load_data_from_csv():
    filepath = open_file()
    if filepath:
        df = pd.read_csv(filepath)
        meas1=df.iloc[:,0].to_list()
        meas2=df.iloc[:,1].to_list()
        meas_cnt=len(meas1)
        #mit re die Einheit der Messung herausfinden
        units=df.columns.tolist()
        unit1=re.findall(r"\[(.*?)\]",units[0])
        unit2=re.findall(r"\[(.*?)\]",units[1])

        return filepath, meas1, meas2, meas_cnt, unit1[0], unit2[0]
    #else:
       # return #None#,None,None,0,None,None
    

def create_file():
    date=datetime.datetime.now().strftime("%Y%m%d")
    filepath=filedialog.asksaveasfile(title="Datei erstellen",defaultextension=".csv" , filetypes=[("CSV-Dateien", "*.csv")], initialfile=f"Messung_{date}")
    if filepath:
        return filepath.name
    else:
        return None
    
def open_file():
    filepath=filedialog.askopenfilename(title="Datei auswählen", filetypes=[("CSV-Datei","*.csv"), ("Alle Dateien", "*.*")])
    if filepath:
        return filepath
    else:
        return None
    
def choose_file():
    file_exist=messagebox.askyesno(title="Datei vorhanden", message="Existiert eine Datei, in die die Daten gespeichert werden soll?",icon="question")
    print(f"Datei vorhanden: {file_exist}")
    if file_exist:
        filepath = open_file()
    else:
        filepath = create_file()

    return filepath, file_exist


if __name__ == "__main__":
    #save_data_to_csv(0, [1,2,3], [4,5,6], "V", "A")
    filepath, meas1, meas2, cnt, unit1, unit2=load_data_from_csv()
    print(filepath, meas1[0], meas2[0], cnt, unit1, unit2)