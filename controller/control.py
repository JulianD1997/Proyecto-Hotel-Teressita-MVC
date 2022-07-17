from multiprocessing.connection import Client
import tkinter
from datetime import datetime
import model.database as db
import model.client as client_model
import model.hotel_model as hotel_model
import view.gui as view

class Controller :
    
    def __init__(self):
        self.root = tkinter.TK()
        self.control_hotel_model = hotel_model.Hotel_model()
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
        self.control_db.create_table(query)

    def create_client(self,name,last_name,dni,room,entry_date,exit_date):
        entry = self.control_hotel_model.date_model(entry_date)
        exit = self.control_hotel_model.date_model(exit_date)
        self.client = client_model.Client(name.get(),last_name.get(),
                dni.get(),room.get(),entry_date,exit_date)
        query = """--sql
            INSERT INTO Clientes
            values(NULL, ?, ?, ?, ?, ?, ?);
            """
        parameters = (self.client.get_last_name, self.client.get_last_name, 
                self.client.get_dni,self.client.get_room, self.client.get_entry_date, 
                self.client.get_exit_date)
        try : 
            self.control_db.create(query, parameters)
            return ("Crear Cliente",
                    "EL cliente fue creado correctamente")
        except :
            return ("Crear Cliente",
                    "Hubo un error, el cliente no fue guardado")
    
    def read_clients(self,name,last_name,dni,room,entry_date,exit_date):
        clients_dict = {}
        query = """--sql
            SELECT * FROM Clientes  ORDER BY apellido ASC;
            """
        data = self.control_db(query)
        for client in data:
            clients_dict[client[0]] = list(client_model.Client(
                client[1], client[2], client[3], client[4], client[5], client[6]))
        return clients_dict
    
    def query_client(self,name,last_name,dni,room,entry_date,exit_date):
        clients_dict={}
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
                search_entry_date = self.control_hotel_model.date_model(entry_date)
        if len(entry_date.get()) != 0:
                search_exit_date = self.control_hotel_model.date_model(exit_date)
        parametros = (search_name, search_last_name, search_dni, search_room, 
                search_entry_date,search_exit_date)
        data = self.control_db.read(query, parametros) 
        if len(data) == 0:
            return ("Consultar","El cliente no existe")
        else:
            for client in data:
                clients_dict[client[0]] = list(client_model.Client(
                client[1], client[2], client[3], client[4], client[5], client[6]))
            return clients_dict
    
    def update_client(self,id,name,last_name,dni,room,entry_date,exit_date):
        entry = self.control_hotel_model.date_model(entry_date)
        exit = self.control_hotel_model.date_model(exit_date)
        self.client = client_model.Client(name.get(),last_name.get(),
                dni.get(),room.get(),entry_date,exit_date)
        query = """--sql
            UPDATE Clientes
            SET nombre = ?,
                apellido = ?, 
                DNI = ?,
                habitacion = ?,
                fechaDeIngreso = ?,
                fechaDeSalida = ?
            WHERE ID = ?;"""
        parameters = (self.client.get_last_name, self.client.get_last_name, 
                self.client.get_dni,self.client.get_room, self.client.get_entry_date, 
                self.client.get_exit_date,id)
        try:
            self.control_db.create(query, parameters)
            return ("Modificar Cliente",
                    "El cliente fue modificado correctamente")
        except :
            return ("Crear Cliente",
                    "Hubo un error, el cliente no fue modificado")

    def delete_client(self,id):
        query = """--sql
            DELETE FROM Clientes
            WHERE ID = ?;"""
        parameters = (id,)
        try:
            self.control_db.delete(query, parameters)
            return ("Borrar Cliente",
                    "EL cliente fue borrado correctamente")
        except :
            return ("Borrar Cliente",
                    "Hubo un error,EL cliente no fue borrado")
    
    def avalible_rooms(self,event,variable_button,entry_date,exit_date):
        if variable_button.get() == "Consultar":
            return self.control_hotel_model.get_hotel_rooms()
        elif event != "" and (self.control_hotel_model.date_model(entry_date)\
                            <= self.control_hotel_model.date_model(exit_date)):
            query = """--sql
                SELECT habitacion 
                FROM Clientes 
                WHERE fechaDeSalida BETWEEN ? and ?;"""
            date_one = self.control_hotel_model.date_model(entry_date)
            date_two = self.control_hotel_model.date_model(exit_date)
            parameters = (date_one, date_two)
            data = self.control_db.read(query, parameters)
            return self.control_hotel_model.avalible_rooms(data)
        else:
            query = """--sql
                SELECT habitacion 
                FROM Clientes 
                WHERE fechaDeSalida >= ?;
            """
            today = datetime.now()
            date = today.strftime("%Y-%m-%d")
            parameters = (date,)
            datos = self.control_db.read(query, parameters)
            return self.control_hotel_model.avalible_rooms(data)
    