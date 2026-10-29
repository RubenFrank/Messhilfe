#-------------------------------------------------------------------------------------------------
#-------------------------------------------Messhilfe---------------------------------------------
#-------------------------------------------------------------------------------------------------
# Beschreibung: Programm zum Auslesen der Tischmultimeter von Agilent (34401A und 34410A);
#               Speicherung der Messwerte in einer csv-Datei;
#               Darstellung der ausgewählten Messwerte in einem Diagramm
# -------------------------------------------------------------------------------------------------
# Autor:        Ruben Frank (et24014), Tobias Pfau (et24068)
# -------------------------------------------------------------------------------------------------
# Datum:        2026-10-19
# ------------------------------------------------------------------------------------------------- 

#eigene Imports
from serial_communication import *
from file_handle import *
from popup import *

#eingebundene Bibliothekens
import atexit
import tkinter as tk
from tkinter import ttk 
import matplotlib.pyplot as plt

#globale Variablen für die Messung und Speicherung der Messwerte
val_meas1=[]  
val_meas2=[]
cnt_meas = 0
save_idx = 0
save_path = None

#das Objekt für die Serielle Datenübertragung wird erstellt. (eigene Klasse)
com = SerialCommunication()

#Beim Beenden des Programms werden die Ports gesclossen und die Messgeräte auf "LOCAL" gesetzt
atexit.register(com.close_ports)

#-------------------------------------------------------------------------------------------------
#--------------------------------- GUI  Grund-Frame-----------------------------------------------
#-------------------------------------------------------------------------------------------------
root=tk.Tk()
root.title("Messhilfe")
root.geometry("700x700")

#Style für Label (ohne Hintergrundfarbe)
style=ttk.Style()
style.configure("TLabel", background="lightgray")

#Strukturierung des Fensters in Frames
frame_connection=tk.Frame(root, bg="lightgray",width=300)
frame_measurement=tk.LabelFrame(root,text="Messung", bg="lightgray",width=400,height=150)
frame_plot=tk.LabelFrame(root,text="Diagramm", bg="lightgray",width=400,height=350)

#Anzeigen der Elemente im passenden Frame
frame_connection.pack(side="left", fill="y")
frame_measurement.pack(side="top", fill="x")
frame_plot.pack(side="bottom", fill="both", expand=True)

#-------------------------------------------------------------------------------------------------
#----------------------------------Frame Verbiundung----------------------------------------------
#-------------------------------------------------------------------------------------------------
def refresh_ports():
    com.refresh_avail_ports()
    dropdown_ports_1['values']=[port.device for port in com.avail_ports]
    dropdown_ports_2['values']=[port.device for port in com.avail_ports]

button_refresh_ports=ttk.Button(frame_connection, text="Ports aktualisieren", command=refresh_ports)
frame_port1=tk.LabelFrame(frame_connection, text="Port 1", bg="lightgray", width=300)
frame_port2=tk.LabelFrame(frame_connection, text="Port 2", bg="lightgray", width=300)
frame_error=tk.LabelFrame(frame_connection, text="Error-Status", bg="lightgray", width=300)

def init_and_open_ports():
    if dropdown_ports_1.current() >= 0:
        com.config_port(PORT1, com.avail_ports[dropdown_ports_1.current()].device)
        dev1=com.open_port(PORT1)
        com.conf_and_init_meas(PORT1, dropdown_measurement_1.get())
        label_device1.config(text=dev1)
    else: 
        print("Bitte einen Port für Port 1 auswählen.")
    if dropdown_ports_2.current() >= 0:
        com.config_port(PORT2, com.avail_ports[dropdown_ports_2.current()].device)
        dev2=com.open_port(PORT2)
        com.conf_and_init_meas(PORT2, dropdown_measurement_2.get())
        label_device2.config(text=dev2)
    else: 
        print("Bitte einen Port für Port 2 auswählen.")

        # Button zum Verbinden mit dem gewählten Port
button_connect=ttk.Button(frame_connection, text="Verbinden", command=init_and_open_ports)

#-------------------------------------------------------------------------------------------------
#--------------------------------- Frame Connection Port 1 -----------------------------------------------
#-------------------------------------------------------------------------------------------------
# Dropdown-Menü für COM Ports
dropdown_ports_1=ttk.Combobox(frame_port1, values=[port.device for port in com.avail_ports],state="readonly")
dropdown_ports_1.set("Bitte COM Port wählen")
def port_selected_1(event):
    label_portinfo_1.config(text=com.avail_ports[dropdown_ports_1.current()].description)

# Label zur Anzeige des gewählten Ports
label_portinfo_1=ttk.Label(frame_port1, text="---")

#Dropdown-Menü für Messungsart
dropdown_measurement_1=ttk.Combobox(frame_port1,values=["Spannung (DC)","Spannung (AC)", "Strom (DC)","Strom (AC)", "Widerstand (2W)"], state="readonly")
dropdown_measurement_1.set("Bitte Messart wählen")

#Bei änderung des gewählten Ports wird das Label aktualisiert
dropdown_ports_1.bind("<<ComboboxSelected>>", port_selected_1)

#das Angeschlossene Messgerät wird nach verbindung hier angezeigt
device1_frame=tk.LabelFrame(frame_port1, bg="lightgray", text="Angeschlossenes Gerät")
label_device1=ttk.Label(device1_frame, text="---")

#Anzeigen der Elemente im passenden Frame
dropdown_ports_1.pack(pady=5)
label_portinfo_1.pack(pady=5)
dropdown_measurement_1.pack(pady=10)
device1_frame.pack(pady=10)
label_device1.pack(pady=5)

#-------------------------------------------------------------------------------------------------
#--------------------------------- Frame Connection Port 2 -----------------------------------------------
#-------------------------------------------------------------------------------------------------

# Dropdown-Menü für COM Ports
dropdown_ports_2=ttk.Combobox(frame_port2, values=[port.device for port in com.avail_ports],state="readonly")
dropdown_ports_2.set("Bitte COM Port wählen")
def port_selected_2(event):
    label_portinfo_2.config(text=com.avail_ports[dropdown_ports_2.current()].description)

# Label zur Anzeige des gewählten Ports
label_portinfo_2=ttk.Label(frame_port2, text="---")

#Dropdown-Menü für Messungsart
dropdown_measurement_2=ttk.Combobox(frame_port2,values=["Spannung (DC)","Spannung (AC)", "Strom (DC)","Strom (AC)", "Widerstand (2W)"], state="readonly")
dropdown_measurement_2.set("Bitte Messart wählen")

#Bei änderung des gewählten Ports wird das Label aktualisiert
dropdown_ports_2.bind("<<ComboboxSelected>>", port_selected_2)

#das Angeschlossene Messgerät wird nach verbindung hier angezeigt
device2_frame=tk.LabelFrame(frame_port2, bg="lightgray", text="Angeschlossenes Gerät")
label_device2=ttk.Label(device2_frame, text="---")

#Anzeigen der Elemente im passenden Frame
dropdown_ports_2.pack(pady=5)
label_portinfo_2.pack(pady=5)
dropdown_measurement_2.pack(pady=10)
device2_frame.pack(pady=10)
label_device2.pack(pady=5)

#-------------------------------------------------------------------------------------------------
#--------------------------------- Frame Error -----------------------------------------------
#-------------------------------------------------------------------------------------------------
def read_error():
    error1=com.read_error(PORT1)
    error2=com.read_error(PORT2)
    label_error1.config(text=f"Port 1: {error1}")
    label_error2.config(text=f"Port 2: {error2}")

button_readError=ttk.Button(frame_error, text="Fehler lesen", command=read_error)
label_error1=ttk.Label(frame_error, text="Port 1: ---")
label_error2=ttk.Label(frame_error, text="Port 2: ---")

#Anzeigen der Elemente im passenden Frame
button_readError.pack(pady=5, padx=5, fill="x")
label_error1.pack(pady=5)
label_error2.pack(pady=5)

#-------------------------------------------------------------------------------------------------
#--------------------------------- Frame Messung -----------------------------------------------
#-------------------------------------------------------------------------------------------------

def meas_start():
    global cnt_meas

    if com.port[PORT1].is_open or com.port[PORT2].is_open:
        
        if com.port[PORT1].is_open:
            val_meas1.append(float(com.start_measurement(PORT1)))    
        else:
            val_meas1.append(float('nan')) 
        
        if com.port[PORT2].is_open:
            val_meas2.append(float(com.start_measurement(PORT2)))
        else:
            val_meas2.append(float('nan')) 

        label_measure1.config(text=f"{val_meas1[cnt_meas]} {com.unit[PORT1]}")
        label_measure2.config(text=f"{val_meas2[cnt_meas]} {com.unit[PORT2]}")
        cnt_meas+=1
        label_meascnt.config(text=f"Messungen: {cnt_meas}")
        
    else:
        print("Bitte mindestens einen Port verbinden, um Messungen durchzuführen.")

def save_data():
    global save_path, save_idx
    save_path=save_data_to_csv(save_path,save_idx, val_meas1, val_meas2, com.unit[PORT1], com.unit[PORT2])
    save_idx=cnt_meas
    label_open_file.config(text=save_path)

def load_data():
    global save_path, cnt_meas, val_meas1, val_meas2, save_idx
    result=load_data_from_csv()
    #save_path, val_meas1, val_meas2, cnt_meas,com.unit[PORT1],com.unit[PORT2]=result
    if result is not None:
        save_path, val_meas1, val_meas2, cnt_meas,com.unit[PORT1],com.unit[PORT2]=result
        save_idx=cnt_meas
        label_meascnt.config(text=f"Messungen: {cnt_meas}")
        label_open_file.config(text=save_path)

def new_measure():
    global save_path, cnt_meas, val_meas1, val_meas2, save_idx
    ask_reset=messagebox.askyesno(title="Messwerte verwerfen", message="Wirklich eine neue Messung starten?\nAlle nicht gespeicherte Daten gehen verloren!",icon="warning")
    if ask_reset:
        save_path=None
        cnt_meas=0
        save_idx=0
        val_meas1.clear()
        val_meas2.clear()
        label_meascnt.config(text=f"Messungen: {cnt_meas}")
        label_open_file.config(text="")

button_measure=ttk.Button(frame_measurement, text="Messung starten", command=meas_start)
button_saveData=ttk.Button(frame_measurement, text="Messwerte speichern", command= save_data)
button_loadData=ttk.Button(frame_measurement, text="Messwerte laden", command=load_data)
button_newMeasure=ttk.Button(frame_measurement, text="Neue Messung", command=new_measure)
button_showData=ttk.Button(frame_measurement, text="Messungen anzeigen", command=lambda: show_data(val_meas1, val_meas2, com.unit[PORT1], com.unit[PORT2]))
measure_value1_frame=tk.LabelFrame(frame_measurement,bg="lightgray", text="Messwert Port 1", width=200)
measure_value2_frame=tk.LabelFrame(frame_measurement, bg="lightgray", text="Messwert Port 2", width=200)
label_measure1=ttk.Label(measure_value1_frame, text="---")
label_measure2=ttk.Label(measure_value2_frame, text="---")
label_meascnt=ttk.Label(frame_measurement, text=f"Messungen: {cnt_meas}", style="TLabel")
label_open_file=ttk.Label(frame_measurement, text=save_path, style="TLabel")

#Anzeigen der Elemente im passenden Frame, hier als grid
button_measure.grid(row=0, column=0, padx=10, pady=10)
button_saveData.grid(row=1, column=1, padx=10, pady=10)
button_loadData.grid(row=1, column=2, padx=10, pady=10)
button_newMeasure.grid(row=1, column=3, padx=10, pady=10)
label_open_file.grid(row=2, column=0,columnspan=3, padx=10, pady=10)
label_meascnt.grid(row=0, column=3, padx=10, pady=10)
button_showData.grid(row=1, column=0, padx=10, pady=10)
measure_value1_frame.grid(row=3, column=0, padx=10, pady=10)
measure_value2_frame.grid(row=3, column=1, padx=10, pady=10)
label_measure1.pack(fill="x", padx=10, pady=10)
label_measure2.pack(fill="x", padx=10, pady=10)

#-------------------------------------------------------------------------------------------------
#--------------------------------- Frame Diagramm -----------------------------------------------
#-------------------------------------------------------------------------------------------------


#-------------------------------------------------------------------------------------------------
#----------------------------------Packen der ROOT-Frames-----------------------------------------------
#-------------------------------------------------------------------------------------------------
button_refresh_ports.pack(pady=5, padx=5, fill="x")
button_connect.pack(pady=5, padx=5, fill="x")
frame_port1.pack(pady=10, padx=10, fill="both")
frame_port2.pack(pady=10, padx=10, fill="both")
frame_error.pack(pady=10, padx=10, fill="both")

root.mainloop()