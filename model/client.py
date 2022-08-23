"""Modelo cliente"""
class Person:
    """
        Clase persona con atributos, nombré, apellido y DNI
        igualmente diferentes métodos para obtener y modificar los datos
    """
    def __init__(self,name,last_name,dni):
        self.__name = name
        self.__last_name = last_name
        self.__dni = dni
    
    def get_name(self):
        return self.__name
    
    def set_name(self,name):
        self.__name = name

    def get_last_name(self):
        return self.__last_name

    def set_last_name(self,last_name):
        self.__last_name = last_name

    def get_dni(self):
        return self.__dni
    
    def set_dni(self,dni):
        self.__dni = dni

class Client(Person):
    """
        Clase Clientes que hereda de la clase persona agregando los atributos
        habitación fecha de entrada y fecha de salida
        además de los métodos para modificar y obtener estos datos
    """
    def __init__(self,name,last_name,dni,room,entry_date,exit_date):
        super().__init__(name,last_name,dni)
        self.__room = room
        self.__entry_date = entry_date
        self.__exit_date = exit_date
    
    def get_room(self):
        return self.__room
    
    def set_room(self,room):
        self.__room = room
    
    def get_entry_date(self):
        return self.__entry_date
    
    def set_entry_date(self,entry_date):
        self.__entry_date = entry_date
    
    def get_exit_date(self):
        return self.__exit_date
    
    def set_exit_date(self,exit_date):
        self.__exit_date = exit_date
