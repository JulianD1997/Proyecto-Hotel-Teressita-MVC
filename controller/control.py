from datetime import datetime
import tkinter
import model.client as client_model
import model.database as db
import model.hotel_model as hotel_model
import view.gui as view
"""
    Módulo encargado de todo el control de esta aplicación

"""
class Controller :

    def __init__(self):
        """
            Se inicializa todas las variables creando instancias en las diferentes clases de modelo
            y la vista
        """
        self.control_db = db.CRUD()
        self.control_hotel_model = hotel_model.Hotel_model()
        self.create_table() 
        self.root = tkinter.Tk()
        self.control_view = view.Interface(self.root,self)
        
    def run_window(self):
        """
            Ejecuta la aplicación
        """
        self.control_view.run_window()  
                    
    def create_table(self):
        """
            crea la tabla cliente en la base de datos
        """
        self.control_db.create_table()

    def create_client(self,client_data):
        """
            Este apartado se encarga de crear el cliente nuevo, recibe todos los datos
            del cliente a crear, organiza estos datos en el modelo cliente, convierte
            las fechas tipos date, luego envía todos los datos organizados al módulo 
            database para que este se encargue de crear el cliente en la tabla de base
            de datos, este módulo está entre un bloque try except en dado caso en que 
            suceda un error, retornando un aviso que indique si el cliente fue creado 
            o no
        """
        try : 
            entry = self.control_hotel_model.date_model(client_data['entry_date'])
            exit = self.control_hotel_model.date_model(client_data['exit_date'])
            self.client = client_model.Client(client_data['name'],client_data['last_name'],
                    client_data['dni'],client_data['room'],entry,exit)
            self.control_db.create_client(
                                name= self.client.get_name(),
                                last_name = self.client.get_last_name(),
                                DNI = self.client.get_dni(),
                                room = self.client.get_room(),
                                date_entry = self.client.get_entry_date(),
                                date_exit = self.client.get_exit_date())
            self.control_view.set_variables()
            return ("Create client",
                    "The Client was created successfully")
        except :
            return ("Create client",
                    "Error, the client was not created successfully")
    
    def read_clients(self,tree):
        """
            Este método se encarga de leer todos los clients que estén registrados.
            Recibe un parámetro el cual es el treeview para proceder a eliminar todos 
            los datos que estén dentro del él y luego insertar los registros recibidos
            del modelo database (read_clients). 
        """
        clients = tree.get_children()
        for client in clients:
            tree.delete(client)
        for client in self.control_db.read_clients():
            tree.insert("", "end", text=client.id,
                     values=(client.name, client.last_name, client.DNI,
                             client.room, client.date_entry, client.date_exit))

    def query_client(self,tree,client_data):
        """
            En este método sucede la búsqueda de clientes por medio de los parámetros
            que el usuario ingrese, recibe dos parámetros que el treeview actualizar 
            la visualización de los clientes filtrados y el segundo argumento los datos 
            a filtrar.
            Se inicializan variables de caracteres que corresponden a la búsqueda donde estás, son 
            modificadas cuando la longitud de algún dato es mayor a 0. Se utiliza condicionales 
            para longitudes mayores a 0 modificando así la búsqueda filtrada de los clientes
        """
        search_client = False
        search_name = search_last_name = search_dni = search_room = ""
        search_entry_date = "0000-01-01"
        search_exit_date = "9999-12-31"
        if len(client_data['name']) != 0:
            search_client = True
            search_name = client_data['name']
        if len(client_data['last_name']) != 0:
            search_client = True
            search_last_name = client_data['last_name']
        if len(client_data['dni']) != 0:
            search_client = True
            search_dni = client_data['dni']
        if client_data['room'] != "Select":
            search_client = True
            search_room = client_data['room']
        if len(client_data['entry_date']) != 0:
            search_client = True
            search_entry_date = self.control_hotel_model.date_model(client_data['entry_date'])
        if len(client_data['exit_date']) != 0:
            search_client = True
            search_exit_date = self.control_hotel_model.date_model(client_data['entry_date'])
        """
            Al finalizar la comprobación y a su vez la modificación de los variables de búsqueda, 
            se procede a ejecutar search_client del módulo database donde este método nos retorna
            los datos encontrados en la base de datos.
        """
        data = self.control_db.search_client(
                                name= search_name,
                                last_name = search_last_name,
                                DNI = search_dni,
                                room = search_room,
                                date_entry = search_entry_date,
                                date_exit = search_exit_date)
        """
            A continuación se procede a realizar una condición de longitud de la variable (data) para conocer 
            que haya datos en ella y un booleano(search_client) para conocer que se ingresó un dato para la búsqueda.
            De no haber datos o de no haber ingresado parámetros para la búsqueda, se ejecuta un aviso de diálogo donde 
            nos informara si el cliente no fue encontrado o de en el caso de no ingresar un valor a filtrar nos indicara 
            inténtelo de nuevo.
            Por último, si la variable (data) tiene valores, se procede a actualizar la vista del treeview cargando estos valores
            de clientes filtrados
        """
        if len(data) == 0 or not search_client:
            self.control_view.message_box(("Query","The client is not exist") if search_client else ("Query","try again"))
        else:
            clients = tree.get_children()
            for client in clients:
                tree.delete(client)
            for client in data:
                tree.insert("", "end", text=client.id,
                     values=(client.name, client.last_name, client.DNI,
                             client.room, client.date_entry, client.date_exit))
    
    def update_client(self,client_data):
        """
            Se encarga de actualizar el cliente recibiendo los datos del cliente
            se estructura estos datos en el modelo client se modela la fecha a tipo date
            y se procede a la ejecución del update_client del modelo database.
            Este proceso está envuelto entre un try except, que nos retornara un diálogo de texto
            correcto o incorrecto.
        """
        try:
            entry = self.control_hotel_model.date_model(client_data['entry_date'])
            exit = self.control_hotel_model.date_model(client_data['exit_date'])
            self.client = client_model.Client(client_data['name'],client_data['last_name'],
                    client_data['dni'],client_data['room'],entry,exit)
            self.control_db.update_client(
                                name= self.client.get_name(),
                                last_name = self.client.get_last_name(),
                                DNI = self.client.get_dni(),
                                room = self.client.get_room(),
                                date_entry = self.client.get_entry_date(),
                                date_exit = self.client.get_exit_date(),
                                id = client_data['id_client'])
            self.control_view.set_variables()
            return ("Update client",
                    "the client was updated successfully")
        except :
            return ("Update client",
                    "Error, the client was not updated successfully")

    def delete_client(self):
        """
            Eliminación de un cliente, 
            se procede a seleccionar el ID del cliente enfocado en el treeview
            donde se ejecuta un cuadro de texto que permite validar si realmente desea
            borrar ese cliente, cuando esté la confirmación sea verdadera procede a 
            eliminarlo y enviar un mensaje de satisfacción, si llega a ocurrir algún 
            error este será notificado. 
            Si la confirmación es falsa, se envía un mensaje de texto informando que 
            seleccione el cliente a eliminar.
        """
        client = self.control_view.tree.item(self.control_view.tree.focus())
        self.control_view.id_client = client['text']
        if self.control_view.id_client !='':
            if self.control_view.message_box():
                try:
                    self.control_db.delete_client(self.control_view.id_client)
                    self.control_view.message_box(("Delete Client","The client was deleted successfully"))
                    self.read_clients(self.control_view.tree)
                except :
                    self.control_view.message_box(("Delete Client",
                            "Error, the client was not deleted successfully"))
        else :
            self.control_view.message_box(("Delete client","please, You select the client want delete"))
        self.control_view.set_variables()
    
    def avalible_rooms(self,event,variable_button,room_form,entry_date,exit_date):
        """
            Se encarga de mostrar las habitaciones disponibles en el momento, recibe 5 argumentos
            event: para conocer que se seleccionó una fecha del calendario
            variable_button: este mostrara todas las habitaciones cuando el valor botón multifuncional
            sea (Search)
            room_form: comboBox de modelo vista
            entry_date y exit_date = las fechas en las cuales se desea realizar un reserva
        """
        if variable_button.get() == "Search":
            """
                Muestra todas las habitaciones del hotel
            """
            room_form["values"] = self.control_hotel_model.get_hotel_rooms()
            return room_form
        elif event != "" and (self.control_hotel_model.date_model(entry_date.get())\
                            <= self.control_hotel_model.date_model(exit_date.get())):
            """
                Si se seleccionó una fecha y la fecha de entrada es menor a la de salida, 
                se procede a encontrar la habitación que estén disponibles entre esas fecha por medio
                de la consulta de occupied_rooms_between del modelo database.
            """
            date_one = self.control_hotel_model.date_model(entry_date.get())
            date_two = self.control_hotel_model.date_model(exit_date.get())
            data = self.control_db.occupied_rooms_between(date_one, date_two)
            room_form["values"] = self.control_hotel_model.avalible_rooms(data)
            return room_form
        else:
            """
                De no haber un evento o si la fecha de salida es mayor que la de entrada, se muestra las
                habitaciones que están disponibles en el día actual.
            """
            today = datetime.now()
            date = today.strftime("%Y-%m-%d")
            data = self.control_db.occupied_rooms(date)
            room_form["values"] = self.control_hotel_model.avalible_rooms(data)
            return room_form

    def validate_string(self, text):
        """
            Válida que el valor que se está ingresando sea alfabético
        """
        return self.control_hotel_model.validate_string(text)
    
    def validate_number(self, text):
        """
            Válida que el valor que se esté ingresando sea numérico
        """
        return self.control_hotel_model.validate_number(text)

    def validate_data(self,name_error,last_name_error,dni_error,room_error,client_data):
        """
            Método para la validación de datos ingresados en la parte de formularios de la vista
            permite que solo se ingrese datos alfabéticos en los formularios nombre, apellido y solo números
            en el apartado de DNI a su vez que solo se estén ingresando un máximo de 8 dígitos
            de no ser correcto o en caso de uno ingresar valores se mostraran etiquetas abajo de los formularios
            indicando que estos son requeridos. Retornando un booleano para que el método action_press realice
            el debido flujo del programa.
        """
        self.control_view.set_labels()
        validate = True
        if not self.control_hotel_model.validate_string(client_data['name'],'^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]+$'):
            name_error.set("This is required")
            validate = False
        if not self.control_hotel_model.validate_string(client_data['last_name'],'^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]+$'):
            last_name_error.set("This is required")
            validate = False
        if not self.control_hotel_model.validate_number(client_data['dni'],'^[0-9]{8}$'):
            dni_error.set("Invalid DNI")
            validate = False
        if client_data['room'] == "Select":
            room_error.set("Not Selected")
            validate = False
        return validate
     
    def action_press(self,client_data):
        """
            Flujo de control del botón multifuncional donde dependiendo de su valor
            tomara un método de esta clase.
        """
        if self.control_view.variable_button.get() == 'Save':
            """
                Si el botón multifuncional es Save y la validación de los datos son correctos, procede
                a llamar el método create_client enviando los argumentos que este necesite y a la vez
                acciona el método message_box de la vista para mostrar los mensajes de alerta que sean 
                necesarios.
            """
            if self.validate_data(self.control_view.name_error,self.control_view.last_name_error,\
                self.control_view.dni_error,self.control_view.room_error,client_data):
                result = self.create_client(client_data)
                self.read_clients(self.control_view.tree)
                self.control_view.message_box(result)
        elif self.control_view.variable_button.get() == 'Search':
            """
                Si el botón multifuncional es Search procede a llamar el método query_client enviando los 
                argumentos que este necesite(treeview, client_data)
            """
            self.query_client(self.control_view.tree,client_data)
        elif self.control_view.variable_button.get() == 'Update':
            """
                Si el botón multifuncional es Update y la validación de los datos es correcta, procede a llamar 
                el método update_client enviando los argumentos que este necesite(client_data) y a su vez 
                mostrar los mensajes de alerta.
            """
            if self.validate_data(self.control_view.name_error,self.control_view.last_name_error,\
                self.control_view.dni_error,self.control_view.room_error,client_data):
                result = self.update_client(client_data)
                self.read_clients(self.control_view.tree)
                self.control_view.message_box(result)
   
    

