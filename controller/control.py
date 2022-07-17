from multiprocessing.connection import Client
import tkinter
import datetime
import model.database as db
import model.client as client_model
import view.gui as view

class Controller():

    def __init__(self):
        self.root = tkinter.TK()
        self.control_db = db.Database("Hotel Teressita")
        self.control_view = view.Interface(self.root)
    def run_window(self):
        self.root.title("Hotel Teressita")
        self.root.deiconify()
        self.root.mainloop()   
    def create_table(self):
        query = '''--sql
            CREATE TABLE IF NOT EXISTS Clientes(
                ID  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                nombre VARCHAR(75) NOT NULL,
                apellido VARCHAR(75) NOT NULL,
                DNI VARCHAR(10) NOT NULL,
                habitacion VARCHAR(6) NOT NULL,
                fechaDeIngreso DATE NOT NULL,
                fechaDESalida DATE NOT NULL
            );'''
        self.control_db.action(query)

    def create_client(self,name,last_name,dni,room,entry_date,exit_date):
        entry = datetime.strptime(entry_date.get(), '%Y-%m-%d').date()
        exit = datetime.strptime(exit_date.get(), '%Y-%m-%d').date()
        self.client = client_model.Client(name.get(),last_name.get(),dni.get(),room.get(),entry_date,exit_date)
        query = """--sql
            INSERT INTO Clientes
            values(NULL, ?, ?, ?, ?, ?, ?);
            """
        parameters = (self.client.get_last_name, self.client.get_last_name.get(), self.client.get_dni,
                      self.client.get_room, self.client.get_entry_date, self.client.get_exit_date)
        datos = self.control_db(query, parameters)
        if datos is not False:
            return ("Crear Cliente",
                                "EL cliente fue creado correctamente")
        else:
            return("Crear Cliente",
                                "Hubo un error, el cliente no fue guardado")
    
    def read_clients(self,name,last_name,dni,room,entry_date,exit_date):
        self.clients_dict = {}
        query = """--sql
            SELECT * FROM Clientes  ORDER BY apellido ASC;
            """
        data = self.control_db(query)
        for client in data:
            self.clients_dict[client[0]] = list(client_model.Client(client[1],client[2],client[3],client[4],client[5],client[6]))
        return self.clients_dict
    
    def query_client(self,name,last_name,dni,room,entry_date,exit_date):
        search_name = search_last_name = search_dni = search_room = "%%"
        search_entry_date = "0000-01-01"
        search_exit_date = "9999-12-31"
        query="""--sql
            SELECT * FROM Clientes
            WHERE nombre LIKE ?
            AND apellido LIKE ?
            AND DNI LIKE ?
            AND habitacion LIKE ?
            AND fechaDeIngreso >= ?
            AND fechaDESalida <= ?
            ORDER BY apellido ASC;
            """
        if len(name.get()) != 0:
                search_name = "%" + name.get() + "%"
        if len(last_name.get()) != 0:
                search_last_name = "%" + last_name.get() + "%"
        if len(dni.get()) != 0:
                search_dni = "%" + dni.get() + "%"
        if room.get() != "Seleccionar":
                search_room = room.get()
        if len(entry_date.get()) != 0:
                search_entry_date = datetime.strptime(entry_date.get(),
                                                    '%Y-%m-%d').date()
        if len(entry_date.get()) != 0:
                search_exit_date = datetime.strptime(exit_date.get(),
                                                    '%Y-%m-%d').date()