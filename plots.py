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
import os
from matplotlib.figure import Figure
from file_handle import load_data_from_csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

#DAtenquellen, die auf die Achsen gelegt werden können
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

        #Legendentexte; leer -> "Aktuelle Messung" bzw. Dateiname der Vergleichsmessung
        ttk.Label(frame_settings, text="Legende Messung:").grid(row=3, column=0, padx=5, pady=2, sticky="w")
        self.entry_legend=ttk.Entry(frame_settings, width=20)
        self.entry_legend.grid(row=3, column=1, padx=5, pady=2)

        #Auswahl der Vergleichsmessung, die unten bearbeitet wird; + importiert, − entfernt
        ttk.Label(frame_settings, text="Vergleich:").grid(row=3, column=2, padx=5, pady=2, sticky="w")
        frame_cmp=tk.Frame(frame_settings, bg="lightgray")
        self.dropdown_cmp=ttk.Combobox(frame_cmp, state="readonly", width=11)
        self.dropdown_cmp.pack(side="left")
        ttk.Button(frame_cmp, text="+", width=2, command=self.import_comparison).pack(side="left", padx=(2,0))
        self.button_remove_cmp=ttk.Button(frame_cmp, text="−", width=2, command=self.remove_comparison)
        self.button_remove_cmp.pack(side="left", padx=(2,0))
        frame_cmp.grid(row=3, column=3, padx=5, pady=2)

        ttk.Label(frame_settings, text="Legende Vergleich:").grid(row=4, column=0, padx=5, pady=2, sticky="w")
        self.entry_legend_cmp=ttk.Entry(frame_settings, width=20)
        self.entry_legend_cmp.grid(row=4, column=1, padx=5, pady=2)

        #eigene Achsenwahl je Vergleichsmessung, z.B. falls dort die Ports vertauscht waren
        ttk.Label(frame_settings, text="Vergleich X:").grid(row=5, column=0, padx=5, pady=2, sticky="w")
        self.dropdown_x_cmp=ttk.Combobox(frame_settings, values=DATA_SOURCES, state="readonly", width=17)
        self.dropdown_x_cmp.grid(row=5, column=1, padx=5, pady=2)

        ttk.Label(frame_settings, text="Vergleich Y:").grid(row=5, column=2, padx=5, pady=2, sticky="w")
        self.dropdown_y_cmp=ttk.Combobox(frame_settings, values=DATA_SOURCES, state="readonly", width=17)
        self.dropdown_y_cmp.grid(row=5, column=3, padx=5, pady=2)

        self.grid_on=tk.BooleanVar(value=True)
        tk.Checkbutton(frame_settings, text="Gitter", variable=self.grid_on, bg="lightgray", command=self.update_plot).grid(row=6, column=0, padx=5, pady=2, sticky="w")

        ttk.Button(frame_settings, text="Als PNG speichern", command=self.save_png).grid(row=6, column=2, padx=5, pady=2, sticky="e")
        ttk.Button(frame_settings, text="In eigenem Fenster", command=self.open_window).grid(row=6, column=3, padx=5, pady=2, sticky="e")

        #bei jeder Änderung einer Einstellung wird das Diagramm automatisch aktualisiert
        for dropdown in (self.dropdown_x, self.dropdown_y, self.dropdown_type):
            dropdown.bind("<<ComboboxSelected>>", lambda event: self.update_plot())
        for entry in (self.entry_title, self.entry_xlabel, self.entry_ylabel, self.entry_legend):
            entry.bind("<KeyRelease>", lambda event: self.update_plot())

        #Einstellungen der Vergleichsmessung werden in der ausgewählten Messung gespeichert
        self.dropdown_cmp.bind("<<ComboboxSelected>>", lambda event: self.show_comparison())
        for dropdown in (self.dropdown_x_cmp, self.dropdown_y_cmp):
            dropdown.bind("<<ComboboxSelected>>", lambda event: self.store_comparison())
        self.entry_legend_cmp.bind("<KeyRelease>", lambda event: self.store_comparison())

        #importierte Vergleichsmessungen, nur für das Diagramm;
        #je Messung ein dict mit data=(val_meas1, val_meas2, unit1, unit2), legend, x, y
        self.comparisons=[]
        self.show_comparison()

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

    #lädt eine Messung aus einer CSV-Datei, die nur zum Vergleich im Diagramm angezeigt wird
    def import_comparison(self):
        result=load_data_from_csv()
        if result is not None:
            filepath, val_meas1, val_meas2, meas_cnt, unit1, unit2=result
            #Legende = Dateiname, Achsenwahl startet wie die der aktuellen Messung
            self.comparisons.append({"data": (val_meas1, val_meas2, unit1, unit2),
                                     "legend": os.path.splitext(os.path.basename(filepath))[0],
                                     "x": self.dropdown_x.get(), "y": self.dropdown_y.get()})
            self.show_comparison(len(self.comparisons)-1)

    def remove_comparison(self):
        idx=self.dropdown_cmp.current()
        if idx>=0:
            del self.comparisons[idx]
            self.show_comparison(min(idx, len(self.comparisons)-1))

    #Namen im Auswahl-Dropdown, nummeriert, damit gleiche Legenden unterscheidbar bleiben
    def comparison_names(self):
        return [f"{i+1}: {cmp['legend'] or 'Vergleich'}" for i, cmp in enumerate(self.comparisons)]

    #zeigt die Einstellungen der Vergleichsmessung idx (Standard: aktuelle Auswahl) in den Feldern an
    def show_comparison(self, idx=None):
        if idx is None:
            idx=self.dropdown_cmp.current()
        self.dropdown_cmp.config(values=self.comparison_names())
        #ein deaktiviertes Eingabefeld lässt sich nicht beschreiben -> erst aktivieren
        self.entry_legend_cmp.config(state="normal")
        self.entry_legend_cmp.delete(0, tk.END)

        if idx>=0 and self.comparisons:
            cmp=self.comparisons[idx]
            state="normal"
            self.dropdown_cmp.current(idx)
            self.entry_legend_cmp.insert(0, cmp["legend"])
            self.dropdown_x_cmp.set(cmp["x"])
            self.dropdown_y_cmp.set(cmp["y"])
        else:
            state="disabled"
            self.dropdown_cmp.set("")
            self.dropdown_x_cmp.set("")
            self.dropdown_y_cmp.set("")

        #ohne Vergleichsmessung gibt es nichts zu bearbeiten
        self.entry_legend_cmp.config(state=state)
        self.button_remove_cmp.config(state=state)
        for dropdown in (self.dropdown_cmp, self.dropdown_x_cmp, self.dropdown_y_cmp):
            dropdown.config(state="readonly" if state=="normal" else "disabled")

        #beim ersten Aufruf aus __init__ gibt es noch kein Diagramm
        if hasattr(self, "figures"):
            self.update_plot()

    #übernimmt Legende und Achsenwahl aus den Feldern in die ausgewählte Vergleichsmessung
    def store_comparison(self):
        idx=self.dropdown_cmp.current()
        if idx>=0:
            cmp=self.comparisons[idx]
            cmp["legend"]=self.entry_legend_cmp.get()
            cmp["x"]=self.dropdown_x_cmp.get()
            cmp["y"]=self.dropdown_y_cmp.get()
            self.dropdown_cmp.config(values=self.comparison_names())
            self.dropdown_cmp.current(idx)
            self.update_plot()

    #gibt die Werte und die Achsenbeschriftung zur gewählten Datenquelle zurück
    def get_source(self, source, data):
        val_meas1, val_meas2, unit1, unit2=data
        if source=="Port 1":
            return val_meas1, f"Port 1 [{unit1}]"
        elif source=="Port 2":
            return val_meas2, f"Port 2 [{unit2}]"
        else:
            return list(range(1, len(val_meas1)+1)), "Messungsnummer"

    def update_plot(self):
        data=self.get_data()
        x, xlabel=self.get_source(self.dropdown_x.get(), data)
        y, ylabel=self.get_source(self.dropdown_y.get(), data)
        linestyle, marker=PLOT_TYPES[self.dropdown_type.get()]

        #Kurven der Vergleichsmessungen als (x, y, Legende)
        curves_cmp=[]
        for cmp in self.comparisons:
            x_cmp, _=self.get_source(cmp["x"], cmp["data"])
            y_cmp, _=self.get_source(cmp["y"], cmp["data"])
            curves_cmp.append((x_cmp, y_cmp, cmp["legend"] or "Vergleichsmessung"))

        for figure, ax, canvas in self.figures:
            ax.clear()
            ax.plot(x, y, linestyle=linestyle, marker=marker, label=self.entry_legend.get() or "Aktuelle Messung")
            for x_cmp, y_cmp, legend in curves_cmp:
                ax.plot(x_cmp, y_cmp, linestyle=linestyle, marker=marker, label=legend)
            #Legende nur bei Vergleich oder eigenem Legendentext anzeigen
            if curves_cmp or self.entry_legend.get():
                ax.legend()
            ax.set_title(self.entry_title.get())
            ax.set_xlabel(self.entry_xlabel.get() or xlabel)
            ax.set_ylabel(self.entry_ylabel.get() or ylabel)
            ax.grid(self.grid_on.get())
            figure.tight_layout()
            canvas.draw()
