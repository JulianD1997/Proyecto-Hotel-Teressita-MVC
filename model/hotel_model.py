from datetime import datetime
from typing_extensions import Self

class Hotel_model :
    __hotel_rooms = ["101", "102", "103", "104", "201", "202",
                    "203", "204", "301", "302", "303", "304"]
    def __init__(self):
        pass

    def get_hotel_rooms(self):
        return self.__hotel_rooms

    def date_model(self,date):
        return datetime.strptime(date.get(), '%Y-%m-%d').date()
    
    def avalible_rooms(self,data):
        occupied_rooms = []
        for room in data :
            occupied_rooms.append(room[0])
            free_rooms = sorted(list(
                set(self.__hotel_rooms) - set(occupied_rooms)))
            return free_rooms


