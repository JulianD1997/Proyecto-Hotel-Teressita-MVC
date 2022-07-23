from datetime import datetime
import re
import model.client as client_mode

class Hotel_model :

    def __init__(self):
        self.hotel_rooms = ["101", "102", "103", "104", "201", "202",
                    "203", "204", "301", "302", "303", "304"]

    def get_hotel_rooms(self):
        return self.hotel_rooms

    """Formato de fecha"""
    def date_model(self,date):
        return datetime.strptime(date, '%Y-%m-%d').date()
    
    """Modelo habitaciones del hotel"""
    def avalible_rooms(self,data):
        occupied_rooms = []
        free_rooms = []
        if len(data) == 0:
            return self.hotel_rooms
        else:
            for room in data:
                occupied_rooms.append(room[0])
                free_rooms = sorted(list(
                    set(self.hotel_rooms) - set(occupied_rooms)))
            return free_rooms

    """formato de datos del cliente """
    def clients_data_estructure(self,data):
        clients_dict = {}
        for client in data:
            one_client = client_mode.Client(client[1], client[2], client[3], client[4], client[5], client[6])
            clients_dict[client[0]] = [one_client.get_name(),one_client.get_last_name(),one_client.get_dni(),one_client.get_room(),one_client.get_entry_date(),one_client.get_exit_date()]
        return clients_dict

    """Metodos de validan string y enteros ingresado al sistema"""
    def validate_number(self,*args):
        if not re.match(args[1] if len(args) > 1 else "^[0-9]{0,8}$", args[0]):
            return False
        return True

    def validate_string(self,*args):
        if not re.match(args[1] if len(args) > 1 else "^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]{0,30}$", args[0]):
            return False
        return True