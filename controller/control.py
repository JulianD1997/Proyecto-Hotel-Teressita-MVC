from datetime import datetime
import tkinter
import model.client as client_model
import model.database as db
import model.hotel_model as hotel_model
import view.gui as view

class Controller :

    def __init__(self):
        """Se inicializa la clase con la creacion de objetos en los modulos modelo y vista"""
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

    def create_client(self,client_data):
        try : 
            entry = self.control_hotel_model.date_model(client_data['entry_date'])
            exit = self.control_hotel_model.date_model(client_data['exit_date'])
            self.client = client_model.Client(client_data['name'],client_data['last_name'],
                    client_data['dni'],client_data['room'],entry,exit)
            query = """--sql
                INSERT INTO Clientes
                values(NULL, ?, ?, ?, ?, ?, ?);
                """
            parameters = (self.client.get_name(), self.client.get_last_name(), 
                    self.client.get_dni(),self.client.get_room(), self.client.get_entry_date(), 
                    self.client.get_exit_date())
            self.control_db.create(query, parameters)
            self.control_view.set_variables()
            return ("Crear Cliente",
                    "EL cliente fue creado correctamente")
        except :
            return ("Crear Cliente",
                    "Hubo un error, el cliente no fue guardado")
    
    def read_clients(self,tree,ob=''):
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

    def query_client(self,tree,client_data,entry_date,exit_date):
        search_client = False
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
        if len(client_data['name']) != 0:
            search_client = True
            search_name = "%" + client_data['name'] + "%"
        if len(client_data['last_name']) != 0:
            search_client = True
            search_last_name = "%" + client_data['last_name'] + "%"
        if len(client_data['dni']) != 0:
            search_client = True
            search_dni = "%" + client_data['dni'] + "%"
        if client_data['room'] != "Seleccionar":
            search_client = True
            search_room = client_data['room']
        if len(client_data['entry_date']) != 0:
            search_client = True
            search_entry_date = self.control_hotel_model.date_model(client_data['entry_date'])
        if len(client_data['exit_date']) != 0:
            search_client = True
            search_exit_date = self.control_hotel_model.date_model(client_data['entry_date'])
        parameters = (search_name, search_last_name, search_dni, search_room, 
                    search_entry_date,search_exit_date)
        data = self.control_hotel_model.clients_data_estructure(self.control_db.read(query,parameters))
        if len(data) == 0 or not search_client:
            self.control_view.message_box(("Consultar","El cliente no existe") if search_client else ("Consultar","Ingrese un valor a buscar"))
        else:
            clients = tree.get_children()
            for client in clients:
                tree.delete(client)
            for key in data.keys():
                tree.insert("", "end", text=key,
                     values=(data[key][0], data[key][1], data[key][2],
                             data[key][3], data[key][4], data[key][5]))
    
    def update_client(self,client_data):
        try:
            entry = self.control_hotel_model.date_model(client_data['entry_date'])
            exit = self.control_hotel_model.date_model(client_data['exit_date'])
            self.client = client_model.Client(client_data['name'],client_data['last_name'],
                    client_data['dni'],client_data['room'],entry,exit)
            query = """--sql
                UPDATE Clientes
                SET nombre = ?,
                    apellido = ?, 
                    DNI = ?,
                    habitacion = ?,
                    fechaDeIngreso = ?,
                    fechaDeSalida = ?
                WHERE ID = ?;"""
            parameters = (self.client.get_name(), self.client.get_last_name(), 
                    self.client.get_dni(),self.client.get_room(), self.client.get_entry_date(), 
                    self.client.get_exit_date(),client_data['id_client'])
            self.control_db.create(query, parameters)
            return ("Modificar Cliente",
                    "El cliente fue modificado correctamente")
        except :
            return ("Crear Cliente",
                    "Hubo un error, el cliente no fue modificado")

    def delete_client(self):
        client = self.control_view.tree.item(self.control_view.tree.focus())
        self.control_view.id_client = client['text']
        if self.control_view.id_client !='':
            if self.control_view.message_box():
                query = """--sql
                    DELETE FROM Clientes
                    WHERE ID = ?;"""
                parameters = (self.control_view.id_client,)
                try:
                    self.control_db.delete(query, parameters)
                    self.control_view.message_box(("Borrar Cliente","EL cliente fue borrado correctamente"))
                    self.read_clients(self.control_view.tree)
                except :
                    self.control_view.message_box(("Borrar Cliente",
                            "Hubo un error,EL cliente no fue borrado"))
        else :
            self.control_view.message_box(("Borrar Cliente","Seleccione el cliente que quiere eliminar"))
        self.control_view.set_variables()
    
    """El siguiente metodo cumple con el control de la habitaciones del hotel este igualmente tiene un modelo que es fue estableciodo en el modulo modelo"""
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

    """Los siguientes metodos dan control a validez de las strings y enteros que se ingresen en la aplicación se utiliza un modelo con el modulo regex"""
    def validate_string(self, text):
        return self.control_hotel_model.validate_string(text)
    
    def validate_number(self, text):
        return self.control_hotel_model.validate_number(text)

    def validate_data(self,name_error,last_name_error,dni_error,room_error,client_data):
        self.control_view.set_labels()
        validate = True
        if not self.control_hotel_model.validate_string(client_data['name'],'^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]+$'):
            name_error.set("Ingrese el nombre")
            validate = False
        if not self.control_hotel_model.validate_string(client_data['last_name'],'^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]+$'):
            last_name_error.set("Ingrese el apellido")
            validate = False
        if not self.control_hotel_model.validate_number(client_data['dni'],'^[0-9]{8}$'):
            dni_error.set("Ingrese un DNI valido")
            validate = False
        if client_data['room'] == "Seleccionar":
            room_error.set("Sin Seleccionar")
            validate = False
        return validate
    
    """el siguiente metodo cumple con el control del boton que se situa en el frame de los formularios, 
    se controla el crear un clienmte, buscar un cliente o actualizar un cliente """    
    def action_press(self,client_data):
        if self.control_view.variable_button.get() == 'Guardar':
            if self.validate_data(self.control_view.name_error,self.control_view.last_name_error,\
                self.control_view.dni_error,self.control_view.room_error,client_data):
                result = self.create_client(client_data)
                self.read_clients(self.control_view.tree)
                self.control_view.message_box(result)
        elif self.control_view.variable_button.get() == 'Buscar':
            self.query_client(self.control_view.tree,client_data,self.control_view.entry_date,self.control_view.exit_date)
        elif self.control_view.variable_button.get() == 'Actualizar':
            if self.validate_data(self.control_view.name_error,self.control_view.last_name_error,\
                self.control_view.dni_error,self.control_view.room_error,client_data):
                result = self.update_client(client_data)
                self.read_clients(self.control_view.tree)
                self.control_view.message_box(result)
   
    

