#-------------------------------------------------------------------------------------------------
#-----------------------------------Messhilfe Unterprogramm: Diagramm ----------------------------
#-------------------------------------------------------------------------------------------------
# Beschreibung: Darstellung der Messwerte in einem Diagramm im Hauptfenster;
#               der Nutzer wählt, welche Daten auf welcher Achse liegen,
#               sowie Titel, Achsenbeschriftung, Diagrammart und Gitter
# -------------------------------------------------------------------------------------------------
# Autor:        Ruben Frank (et24014), Tobias Pfau (et24068)
# -------------------------------------------------------------------------------------------------
# Datum:        2026-10-30
# -------------------------------------------------------------------------------------------------

import tkinter as tk
from tkinter import ttk, filedialog
import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

#Datenquellen, die auf die Achsen gelegt werden können
DATA_SOURCES=["Messungsnummer", "Port 1", "Port 2"]

#Diagrammart: (Linienstil, Marker)
PLOT_TYPES={"Linie": ("-", ""), "Punkte": ("", "o"), "Linie mit Punkten": ("-", "o")}

class PlotFrame:
    # get_data: Funktion, die (val_meas1, val_meas2, unit1, unit2) zurückgibt
    def __init__(self, parent, get_data):
        self.get_data=get_data

        #Einstellungen für das Diagramm
        frame_settings=tk.Frame(parent, bg="lightgray")

        ttk.Label(frame_settings, text="X-Achse:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.dropdown_x=ttk.Combobox(frame_settings, values=DATA_SOURCES, state="readonly", width=17)
        self.dropdown_x.set("Messungsnummer")
        self.dropdown_x.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(frame_settings, text="Y-Achse:").grid(row=0, column=2, padx=5, pady=2, sticky="w")
        self.dropdown_y=ttk.Combobox(frame_settings, values=DATA_SOURCES, state="readonly", width=17)
        self.dropdown_y.set("Port 1")
        self.dropdown_y.grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(frame_settings, text="Titel:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.entry_title=ttk.Entry(frame_settings, width=20)
        self.entry_title.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(frame_settings, text="Diagrammart:").grid(row=1, column=2, padx=5, pady=2, sticky="w")
        self.dropdown_type=ttk.Combobox(frame_settings, values=list(PLOT_TYPES), state="readonly", width=17)
        self.dropdown_type.set("Linie mit Punkten")
        self.dropdown_type.grid(row=1, column=3, padx=5, pady=2)

        #leere Beschriftung -> automatisch aus Datenquelle und Einheit
        ttk.Label(frame_settings, text="X-Beschriftung:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.entry_xlabel=ttk.Entry(frame_settings, width=20)
        self.entry_xlabel.grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(frame_settings, text="Y-Beschriftung:").grid(row=2, column=2, padx=5, pady=2, sticky="w")
        self.entry_ylabel=ttk.Entry(frame_settings, width=20)
        self.entry_ylabel.grid(row=2, column=3, padx=5, pady=2)

        self.grid_on=tk.BooleanVar(value=True)
        tk.Checkbutton(frame_settings, text="Gitter", variable=self.grid_on, bg="lightgray", command=self.update_plot).grid(row=3, column=0, padx=5, pady=2, sticky="w")

        ttk.Button(frame_settings, text="Als PNG speichern", command=self.save_png).grid(row=3, column=2, padx=5, pady=2, sticky="e")
        ttk.Button(frame_settings, text="In eigenem Fenster", command=self.open_window).grid(row=3, column=3, padx=5, pady=2, sticky="e")

        #bei jeder Änderung einer Einstellung wird das Diagramm automatisch aktualisiert
        for dropdown in (self.dropdown_x, self.dropdown_y, self.dropdown_type):
            dropdown.bind("<<ComboboxSelected>>", lambda event: self.update_plot())
        for entry in (self.entry_title, self.entry_xlabel, self.entry_ylabel):
            entry.bind("<KeyRelease>", lambda event: self.update_plot())

        frame_settings.pack(side="top", fill="x", padx=5, pady=5)

        #alle angezeigten Diagramme (Hauptfenster + eigene Fenster) als (figure, ax, canvas)
        self.figures=[]
        self.figure, self.ax, self.canvas=self.create_figure(parent)

        self.update_plot()

    #erstellt ein Matplotlib-Diagramm mit Werkzeugleiste (Zoom, Verschieben, Speichern) im master
    def create_figure(self, master):
        figure=Figure(figsize=(5,3), dpi=100)
        ax=figure.add_subplot()
        canvas=FigureCanvasTkAgg(figure, master=master)
        toolbar=NavigationToolbar2Tk(canvas, master, pack_toolbar=False)

        #Werkzeugleiste zuerst packen, damit sie beim Verkleinern sichtbar bleibt
        toolbar.pack(side="bottom", fill="x")
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True, padx=5, pady=5)

        self.figures.append((figure, ax, canvas))
        return figure, ax, canvas

    #öffnet das Diagramm in einem eigenen Fenster, das ebenfalls automatisch aktualisiert wird
    def open_window(self):
        window=tk.Toplevel(tk._default_root)
        window.title("Diagramm")
        window.geometry("700x500")
        entry=self.create_figure(window)

        def close_window():
            self.figures.remove(entry)
            window.destroy()

        window.protocol("WM_DELETE_WINDOW", close_window)
        self.update_plot()

    def save_png(self):
        date=datetime.datetime.now().strftime("%Y%m%d")
        filepath=filedialog.asksaveasfilename(title="Diagramm speichern", defaultextension=".png", filetypes=[("PNG-Dateien", "*.png")], initialfile=f"Diagramm_{date}")
        if filepath:
            self.figure.savefig(filepath, dpi=150)

    #gibt die Werte und die Achsenbeschriftung zur gewählten Datenquelle zurück
    def get_source(self, source):
        val_meas1, val_meas2, unit1, unit2=self.get_data()
        if source=="Port 1":
            return val_meas1, f"Port 1 [{unit1}]"
        elif source=="Port 2":
            return val_meas2, f"Port 2 [{unit2}]"
        else:
            return list(range(1, len(val_meas1)+1)), "Messungsnummer"

    def update_plot(self):
        x, xlabel=self.get_source(self.dropdown_x.get())
        y, ylabel=self.get_source(self.dropdown_y.get())
        linestyle, marker=PLOT_TYPES[self.dropdown_type.get()]

        for figure, ax, canvas in self.figures:
            ax.clear()
            ax.plot(x, y, linestyle=linestyle, marker=marker)
            ax.set_title(self.entry_title.get())
            ax.set_xlabel(self.entry_xlabel.get() or xlabel)
            ax.set_ylabel(self.entry_ylabel.get() or ylabel)
            ax.grid(self.grid_on.get())
            figure.tight_layout()
            canvas.draw()
