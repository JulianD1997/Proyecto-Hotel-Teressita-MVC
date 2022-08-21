from datetime import datetime
import tkinter
import model.client as client_model
import model.database as db
import model.hotel_model as hotel_model
import view.gui as view

class Controller :

    def __init__(self):
        self.control_db = db.CRUD()
        self.control_hotel_model = hotel_model.Hotel_model()
        self.create_table() 
        self.root = tkinter.Tk()
        self.control_view = view.Interface(self.root,self)
        
    def run_window(self):
        self.control_view.run_window()  
                    
    def create_table(self):
        self.control_db.create_table()

    def create_client(self,client_data):
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
    
    def read_clients(self,tree,ob=''):
        clients = tree.get_children()
        for client in clients:
            tree.delete(client)
        for client in self.control_db.read_clients():
            tree.insert("", "end", text=client.id,
                     values=(client.name, client.last_name, client.DNI,
                             client.room, client.date_entry, client.date_exit))

    def query_client(self,tree,client_data,entry_date,exit_date):
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
        parameters = (search_name, search_last_name, search_dni, search_dni, 
                    search_entry_date,search_exit_date)
        data = self.control_db.search_client(
                                name= search_name,
                                last_name = search_last_name,
                                DNI = search_dni,
                                room = search_room,
                                date_entry = search_entry_date,
                                date_exit = search_exit_date)
        if len(data) == 0 or not search_client:
            self.control_view.message_box(("Consultar","El cliente no existe") if search_client else ("Consultar","Ingrese un valor a buscar"))
        else:
            clients = tree.get_children()
            for client in clients:
                tree.delete(client)
            for client in data:
                tree.insert("", "end", text=client.id,
                     values=(client.name, client.last_name, client.DNI,
                             client.room, client.date_entry, client.date_exit))
    
    def update_client(self,client_data):
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
        print((self.control_hotel_model.date_model(entry_date.get())\
                            <= self.control_hotel_model.date_model(exit_date.get())))
        if variable_button.get() == "Search":
            room_form["values"] = self.control_hotel_model.get_hotel_rooms()
            return room_form
        elif event != "" and (self.control_hotel_model.date_model(entry_date.get())\
                            <= self.control_hotel_model.date_model(exit_date.get())):
            print(event)
            date_one = self.control_hotel_model.date_model(entry_date.get())
            date_two = self.control_hotel_model.date_model(exit_date.get())
            data = self.control_db.occupied_rooms_between(date_one, date_two)
            print(data)
            room_form["values"] = self.control_hotel_model.avalible_rooms(data)
            return room_form
        else:
            today = datetime.now()
            date = today.strftime("%Y-%m-%d")
            data = self.control_db.occupied_rooms(date)
            print(data,"_____")
            room_form["values"] = self.control_hotel_model.avalible_rooms(data)
            return room_form

    def validate_string(self, text):
        return self.control_hotel_model.validate_string(text)
    
    def validate_number(self, text):
        return self.control_hotel_model.validate_number(text)

    def validate_data(self,name_error,last_name_error,dni_error,room_error,client_data):
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
        if self.control_view.variable_button.get() == 'Save':
            if self.validate_data(self.control_view.name_error,self.control_view.last_name_error,\
                self.control_view.dni_error,self.control_view.room_error,client_data):
                result = self.create_client(client_data)
                self.read_clients(self.control_view.tree)
                self.control_view.message_box(result)
        elif self.control_view.variable_button.get() == 'Search':
            self.query_client(self.control_view.tree,client_data,self.control_view.entry_date,self.control_view.exit_date)
        elif self.control_view.variable_button.get() == 'Update':
            if self.validate_data(self.control_view.name_error,self.control_view.last_name_error,\
                self.control_view.dni_error,self.control_view.room_error,client_data):
                result = self.update_client(client_data)
                self.read_clients(self.control_view.tree)
                self.control_view.message_box(result)
   
    

