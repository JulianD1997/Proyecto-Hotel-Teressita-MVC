import peewee

db = peewee.SqliteDatabase('Hotel_Teressita.db')
class BaseModel(peewee.Model):
    class Meta:
        database = db
class Client(BaseModel):
    name =  peewee.CharField()
    last_name = peewee.CharField()
    DNI = peewee.IntegerField()
    room = peewee.CharField()
    date_entry = peewee.DateField()
    date_exit = peewee.DateField()

class CRUD:
    def __init__(self):
        pass
    
    def create_table(self):
        with db :
            db.create_tables([Client])
    
    def create_client(self,**kwargs):
        client = Client(
                    name = kwargs['name'],
                    last_name = kwargs['last_name'],
                    DNI = kwargs['DNI'],
                    room = kwargs['room'],
                    date_entry = kwargs['date_entry'],
                    date_exit = kwargs['date_exit'])
        client.save()
    
    def read_clients(self):
        return Client.select()
    
    def search_client(self,**kwargs):
        query = Client.select().where(
                    Client.name.contains(kwargs['name'])&\
                    Client.last_name.contains(kwargs['last_name'])&\
                    Client.DNI.contains(kwargs['DNI'])&\
                    Client.room.contains(kwargs['room'])&\
                    (Client.date_entry >= kwargs['date_entry'])&\
                    (Client.date_exit <= kwargs['date_exit']))
        for client in query:
            if len(client.name) > 0 :
                return query
            else:
                return ''
    
    def update_client(self,**kwargs):
        client = Client.update(
                    name = kwargs['name'],
                    last_name = kwargs['last_name'],
                    DNI = kwargs['DNI'],
                    room = kwargs['room'],
                    date_entry = kwargs['date_entry'],
                    date_exit = kwargs['date_exit']).where(Client.id == kwargs['id'])
        client.execute()
    
    def delete_client(self,id):
        client = Client.get(Client.id == id)
        client.delete_instance()
    
    def occupied_rooms(self,date):
        rooms=[]
        query = Client.select(Client.room).where((Client.date_exit >= date) & (Client.date_entry <= date))
        for client in query:
            rooms.append(client.room)
        return rooms
    def occupied_rooms_between(self,date_one,date_two):
        rooms=[]
        query = Client.select(Client.room).where(Client.date_exit.between(date_one,date_two))
        for client in query:
            rooms.append(client.room)
        return rooms