from datetime import datetime
from gc import set_debug
import tkinter
import model.client as client_model
import model.database as db
import model.hotel_model as hotel_model
import view.gui as view

class Controller :

    def __init__(self):
        self.control_db = db.Database("Hotel Teressita")
        self.control_hotel_model = hotel_model.Hotel_model()
        self.create_table()
        self.root = tkinter.Tk()
        self.control_view = view.Interface(self.root,self)
        
    def run_window(self):
        self.control_view.run_window()  
                    
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

    def create_client(self):
        entry = self.control_hotel_model.date_model(self.control_view.entry_date.get())
        exit = self.control_hotel_model.date_model(self.control_view.exit_date.get())
        self.client = client_model.Client(self.control_view.name_client.get(),self.control_view.last_name.get(),
                self.control_view.dni.get(),self.control_view.room.get(),entry,exit)
        query = """--sql
            INSERT INTO Clientes
            values(NULL, ?, ?, ?, ?, ?, ?);
            """
        parameters = (self.client.get_last_name(), self.client.get_last_name(), 
                self.client.get_dni(),self.client.get_room(), self.client.get_entry_date(), 
                self.client.get_exit_date())
        try : 
            self.control_db.create(query, parameters)
            return ("Crear Cliente",
                    "EL cliente fue creado correctamente")
        except :
            return ("Crear Cliente",
                    "Hubo un error, el cliente no fue guardado")
    
    def read_clients(self,tree):
        clients = tree.get_children()
        for client in clients:
            tree.delete(client)
        query = """--sql
            SELECT * FROM Clientes  ORDER BY apellido ASC;
            """
        data = self.control_hotel_model.clients_data_estructure(self.control_db.read(query))
        for key in data.keys():
            tree.insert("", "end", text=key,
                     values=(data[key][0], data[key][1], data[key][2],
                             data[key][3], data[key][4], data[key][5]))
    
    def query_client(self,tree):
        
        clients = tree.get_children()
        for client in clients:
            tree.delete(client)

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
        if len(self.control_view.name_client.get()) != 0:
                search_name = "%" + self.control_view.name.get() + "%"
        if len(self.control_view.last_name.get()) != 0:
                search_last_name = "%" + self.control_view.last_name.get() + "%"
        if len(self.control_view.dni.get()) != 0:
                search_dni = "%" + self.control_view.dni.get() + "%"
        if self.control_view.room.get() != "Seleccionar":
                search_room = self.control_view.room.get()
        if len(self.control_view.entry_date.get()) != 0:
                search_entry_date = self.control_hotel_model.date_model(self.control_view.entry_date)
        if len(self.control_view.entry_date.get()) != 0:
                search_exit_date = self.control_hotel_model.date_model(self.control_view.exit_date)
        parametros = (search_name, search_last_name, search_dni, search_room, 
                search_entry_date,search_exit_date)
        data = self.control_db.read(query, parametros) 
        if len(data) == 0:
            return ("Consultar","El cliente no existe")
        else:
            self.control_hotel_model.clients_data_estructure(data)
            for key in data.keys():
                tree.insert("", "end", text=key,
                     values=(data[key][0], data[key][1], data[key][2],
                             data[key][3], data[key][4], data[key][5]))
    
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
    
    def avalible_rooms(self,event,variable_button,room_form,entry_date,exit_date):
        if variable_button.get() == "Buscar":
            room_form["values"] = self.control_hotel_model.get_hotel_rooms()
            return room_form
        elif event != "" and (self.control_hotel_model.date_model(entry_date.get())\
                            <= self.control_hotel_model.date_model(exit_date.get())):
            query = """--sql
                SELECT habitacion 
                FROM Clientes 
                WHERE fechaDeSalida BETWEEN ? and ?;"""
            date_one = self.control_hotel_model.date_model(entry_date.get())
            date_two = self.control_hotel_model.date_model(exit_date.get())
            parameters = (date_one, date_two)
            data = self.control_db.read(query, parameters)
            room_form["values"] = self.control_hotel_model.avalible_rooms(data)
            return room_form
        else:
            query = """--sql
                SELECT habitacion 
                FROM Clientes 
                WHERE fechaDeSalida >= ?;
            """
            today = datetime.now()
            date = today.strftime("%Y-%m-%d")
            parameters = (date,)
            data = self.control_db.read(query, parameters)
            room_form["values"] = self.control_hotel_model.avalible_rooms(data)
            return room_form

    def validate_string(self, text):
        return self.control_hotel_model.validate_string(text)
    
    def validate_number(self, text):
        return self.control_hotel_model.validate_number(text)

    def action_press(self, action):
        if action == 'Guardar':
            print(action)
            self.create_client()

        elif action == 'Clientes':
            #self.read_clients()
            print(action)
            self.control_view.variable_button.set("guudfudar")
        elif action == 'Buscar':
            #self.query_client()
            print(action)
            self.control_view.variable_button.set("guudfudar")
        elif action == 'Actualizar':
            #self.update_client()
            print(action)
            self.control_view.variable_button.set("guudfudar")
        elif action ==  'Borrar':
            #self.delete_client()
            print(action)

    def validate_date(self):
        validate = True
        if not self.control_hotel_model.validate_string(self.control_view.name_client.get()):
            self.control_view.name_error.set("Ingrese el nombre")
            validate = False
        if not self.control_hotel_model.validate_string(self.control_view.last_name.get()):
            self.control_view.last_name_error.set("Ingrese el apellido")
            validate = False
        if not self.control_hotel_model.validate_number(self.control_view.dni.get(),"^[0-9]{8}$"):
            self.control_view.dni_error.set("Ingrese un DNI valido")
        if self.control_view.room.get() == "Seleccionar":
            self.control_view.room_error.set("Sin Seleccionar")
