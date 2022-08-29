from datetime import datetime
import re
import model.client as client_mode

class Hotel_model :
    """
        Este modelo es exclusivamente para el uso de formatos básicos del hotel, igualmente se utiliza
        la librará re, para validar los campos de nombre, apellido y DNI
    """
    def __init__(self):
        """
            Se declara atributos con las habitaciones del hotel
        """
        self.__hotel_rooms = ["101", "102", "103", "104", "201", "202",
                    "203", "204", "301", "302", "303", "304"]

    def get_hotel_rooms(self):
        """
            Se retorna el atributo hotel_rooms
        """
        return self.__hotel_rooms

    def date_model(self,date):
        """
            Se formatea la fecha para que no haya errores en el programa
        """
        return datetime.strptime(date, '%Y-%m-%d').date()
    
    def avalible_rooms(self,data):
        """
            Este método es encargado de enviar las habitaciones que estén disponibles,
            se utiliza el método set entre el argumento y las habitaciones del
            hotel, para eliminar las habitaciones que estén ocupadas y retorna una lista
        """
        occupied_rooms = []
        free_rooms = []
        if len(data) == 0:
            return self.__hotel_rooms
        else:
            for room in data:
                occupied_rooms.append(room)
                free_rooms = sorted(list(
                    set(self.__hotel_rooms) - set(occupied_rooms)))
            return free_rooms

    def validate_number(self,*args):
        """
            Regex para validar números se utiliza para validar el DNI y además para que el usuario
            solo pueda ingresar valores numéricos
        """
        if not re.match(args[1] if len(args) > 1 else "^[0-9]{0,8}$", args[0]):
            return False
        return True

    def validate_string(self,*args):
        """
            Regex para validar caracteres, se utiliza para validar el nombre y apellido
            e igualmente solo permite ingresar valores alfabéticos
        """
        if not re.match(args[1] if len(args) > 1 else "^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]{0,30}$", args[0]):
            return False
        return True
        