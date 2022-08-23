import peewee
"""
    Modelo encargado únicamente para la parte del ORM de la aplicación.
    Para esta aplicación se utilizó la librería peewee
    Se crea el nombre que tendrá la base de datos
"""
db = peewee.SqliteDatabase('Hotel_Teressita.db')
class BaseModel(peewee.Model):
    class Meta:
        database = db
class Client(BaseModel):
    """
        Se crea la clase cliente que tendrá la base de datos, se crean los datos 
        con su respectivo tipo de valor.
    """
    name =  peewee.CharField()
    last_name = peewee.CharField()
    DNI = peewee.IntegerField()
    room = peewee.CharField()
    date_entry = peewee.DateField()
    date_exit = peewee.DateField()

class CRUD:
    """
        Se crea esta clase para la creación, lectura
        actualización y borrado de datos de la base de datos
    """
    def __init__(self):
        pass
    
    def create_table(self):
        """
            se crea la tabla clientes
            se utiliza un with para que en caso de error cierre la base de datos
        """
        with db :
            db.create_tables([Client])
    
    def create_client(self,**kwargs):
        """
            Método para la creación de clientes
        """
        client = Client(
                    name = kwargs['name'],
                    last_name = kwargs['last_name'],
                    DNI = kwargs['DNI'],
                    room = kwargs['room'],
                    date_entry = kwargs['date_entry'],
                    date_exit = kwargs['date_exit'])
        client.save()
    def read_clients(self):
        """
            Método para la lectura de todos los clientes
        """
        return Client.select()
    
    def search_client(self,**kwargs):
        """
            Método para la búsqueda de clientes según los datos
            ingresados en los formularios
        """
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
        """
            Método para la actualización de clientes
        """
        client = Client.update(
                    name = kwargs['name'],
                    last_name = kwargs['last_name'],
                    DNI = kwargs['DNI'],
                    room = kwargs['room'],
                    date_entry = kwargs['date_entry'],
                    date_exit = kwargs['date_exit']).where(Client.id == kwargs['id'])
        client.execute()
    
    def delete_client(self,id):
        """
            Método para la eliminación de clientes
        """
        client = Client.get(Client.id == id)
        client.delete_instance()
    
    def occupied_rooms(self,date):
        """
            Método para obtener las habitaciones ocupadas en el día actual
        """
        rooms=[]
        query = Client.select(Client.room).where((Client.date_exit >= date) & (Client.date_entry <= date))
        for client in query:
            rooms.append(client.room)
        return rooms
    def occupied_rooms_between(self,date_one,date_two):
        """
            Método para obtener las habitaciones ocupadas en las fechas de entrada y salida seleccionada
        """
        rooms=[]
        query = Client.select(Client.room).where((Client.date_exit>=date_one) & (Client.date_entry<=date_two))
        for client in query:
            rooms.append(client.room)
        return rooms