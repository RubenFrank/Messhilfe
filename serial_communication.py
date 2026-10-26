#-------------------------------------------------------------------------------------------------
#-----------------------------------Messhilfe Unterprogramm: Serielle Kommunikation---------------
#-------------------------------------------------------------------------------------------------
# Beschreibung: die Serielle Ansteuerung der Messgeräte (Agilent 34401A und 34410A) 
#               wird in diesem Unterprogramm realisiert
# -------------------------------------------------------------------------------------------------
# Autor:        Ruben Frank (et24014), Tobias Pfau (et24068)
# -------------------------------------------------------------------------------------------------
# Datum:        2026-10-20
# ------------------------------------------------------------------------------------------------- 
import serial as ser
import serial.tools.list_ports as sertool
import time as t

PORT1 = 0
PORT2 = 1 
WAIT = 0.5

class SerialCommunication:
    def __init__(self):
        self.port=[ser.Serial(), ser.Serial()] 
        self.measure_data=[None, None]
        self.measure_type=[None, None]
        self.unit=[None, None]
        self.avail_ports = sertool.comports()
        for p in self.avail_ports:
            print(p.device, p.description)

    def refresh_avail_ports(self):
        self.avail_ports = sertool.comports()
    
    def config_port(self, port_nr, port_name, baudrate=9600, bytesize=7, parity=ser.PARITY_EVEN, stopbits=2, timeout=1, xonxoff=False, rtscts=False, dsrdtr=False):
        self.port[port_nr].port=port_name
        self.port[port_nr].baudrate=baudrate
        self.port[port_nr].bytesize=bytesize
        self.port[port_nr].parity=parity
        self.port[port_nr].stopbits=stopbits
        self.port[port_nr].timeout=timeout
        self.port[port_nr].xonxoff=xonxoff
        self.port[port_nr].rtscts=rtscts
        self.port[port_nr].dsrdtr=dsrdtr

        print(f"Port {port_name} initialisiert.")

    def open_port(self, port_nr):
        if self.port[port_nr].is_open:
            print(f"Port {self.port[port_nr].port} ist bereits geöffnet.")
            self.port[port_nr].write(b"*IDN?\n")
            t.sleep(WAIT)
            return self.port[port_nr].readline().decode().strip() 
        
        try:
            self.port[port_nr].open()
            print(f"Port {self.port[port_nr].port} geöffnet.")
            t.sleep(WAIT)
            self.port[port_nr].write(b"*IDN?\n")
            t.sleep(WAIT)
            return self.port[port_nr].readline().decode().strip()

        except Exception as e:
            print(f"Fehler beim Öffnen des Ports {self.port[port_nr].port}: {e}")
            return "Fehler beim Öffnen des Ports"

    def close_ports(self):
        for n in range(len(self.port)):
            if self.port[n].is_open:
                self.port[n].write(b"SYSTem:LOCal\n")
                t.sleep(WAIT)
                self.port[n].close()
                t.sleep(WAIT)
                print(f"Port {n + 1} ({self.port[n].port})wurde geschlossen.")
        

    def config_measurement(self, port_nr, measurement_type):
        if measurement_type == "Spannung (DC)":
            self.measure_type[port_nr]=b"CONF:VOLT:DC\n"
            self.unit[port_nr]="V"
        elif measurement_type == "Spannung (AC)":
            self.measure_type[port_nr]=b"CONF:VOLT:AC\n"
            self.unit[port_nr]="V"    
        elif measurement_type == "Strom (DC)":
            self.measure_type[port_nr]=b"CONF:CURR:DC\n"
            self.unit[port_nr]="A"
        elif measurement_type == "Strom (AC)":
             self.measure_type[port_nr]=b"CONF:CURR:AC\n"
             self.unit[port_nr]="A"    
        elif measurement_type == "Widerstand (2W)":
            self.measure_type[port_nr]=b"CONF:RES\n"
            self.unit[port_nr]="\u03A9"
        #elif measurement_type == "Widerstand (4W)":
        #    self.measure_type[port_nr]=(b"CONF:RES?\n")
        else:
            print("Ungültiger Messungstyp.")
    
    def init_measurement(self, port_nr):
        if not self.port[port_nr].is_open:
            print("Port ist nicht geöffnet.")
            return
        try:           
            self.port[port_nr].write(self.measure_type[port_nr])
            t.sleep(WAIT)
            self.port[port_nr].write(b"SYSTem:REMote\n")
            t.sleep(WAIT)
        except Exception as e:
            print(f"Fehler bei der Initialisierung der Messung: {e}")

    def conf_and_init_meas(self, port_nr, measurement_type):
        self.config_measurement(port_nr, measurement_type)
        self.init_measurement(port_nr)


    def start_measurement(self, port_nr):
        if not self.port[port_nr].is_open:
            print("Port ist nicht geöffnet.")
            return None
        # Hier wird die Messung gestartet und die Daten gelesen
        try:
            self.port[port_nr].write(b"READ?\n")
            t.sleep(WAIT)
            self.measure_data[port_nr]=self.port[port_nr].readline().decode().strip()
            return self.measure_data[port_nr]
        except Exception as e:
            print(f"Fehler beim Messen: {e}")
            return None


    def read_error(self, port_nr):
        if not self.port[port_nr].is_open:
            print("Port ist nicht geöffnet.")
            return
        try:
            self.port[port_nr].write(b"SYST:ERR?\n")
            t.sleep(WAIT)
            return self.port[port_nr].readline().decode().strip()
        except Exception as e:
            print(f"Fehler beim Lesen der Fehlermeldung: {e}")