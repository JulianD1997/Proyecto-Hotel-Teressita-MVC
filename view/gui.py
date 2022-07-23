from datetime import datetime
from click import command
from tkcalendar import DateEntry
import tkinter
from tkinter import messagebox
from tkinter import ttk

class Interface ():
    """Se inicializa todas las variables que tendra nuestra interfaz"""
    def __init__(self,root,controller):
        self.controller = controller
        self.root = root
        self.id_client = None
        self.name_client = tkinter.StringVar()
        self.last_name = tkinter.StringVar()
        self.dni = tkinter.StringVar()
        self.room = tkinter.StringVar()
        self.entry_date = tkinter.StringVar()
        self.exit_date = tkinter.StringVar()
        self.variable_button = tkinter.StringVar()
        self.name_error = tkinter.StringVar()
        self.last_name_error = tkinter.StringVar()
        self.dni_error = tkinter.StringVar()
        self.room_error = tkinter.StringVar()
        self.room.set("Seleccionar")
        self.variable_button.set("Guardar")
        self.__frames()
        self.__labels()
        self.room_form = ttk.Combobox(self.__forms_frame, textvariable=self.room,
                                    state="readonly")
        self.__forms()
        self.__buttons()
        self.tree = ttk.Treeview(self.__data_list_frame)
        self.__tree_view()
               
    def run_window(self):
        self.root.resizable(False, False)
        self.root.title("Hotel teressitta")
        self.root.mainloop()

    def __frames(self):
        self.__main_frame = ttk.Frame(self.root,padding=10)
        self.__forms_frame = ttk.LabelFrame(self.__main_frame,text="Formulario cliente",padding=10)
        self.__data_list_frame = ttk.LabelFrame(self.__main_frame,text="Lista de clientes",padding=10)
        self.__tools_frame = ttk.LabelFrame(self.__main_frame,text="Herramientas",padding=10)

        self.__main_frame.grid(column=0, row=0)
        self.__forms_frame.grid(column=0, row=0)
        self.__data_list_frame.grid(column=0, row=1,pady=5)
        self.__tools_frame.grid(column=0, row=2, pady=5)

    def __labels(self):
        self.__label_name = ttk.Label(self.__forms_frame, text="Nombre")
        self.__label_last_name = ttk.Label(self.__forms_frame, text="Apellido")
        self.__label_dni = ttk.Label(self.__forms_frame, text="DNI")
        self.__label_room = ttk.Label(self.__forms_frame, text="Habitacion")
        self.__label_entry_date = ttk.Label(self.__forms_frame, text="Fecha de Ingreso")
        self.__label_exit_date = ttk.Label(self.__forms_frame, text="Fechas de salida")
        
        self.__label_name_error = ttk.Label(self.__forms_frame, textvariable=self.name_error,
                                    foreground="Red")
        self.__label_last_name_error = ttk.Label(self.__forms_frame, textvariable=self.last_name_error,
                                    foreground="Red")
        self.__label_dni_error = ttk.Label(self.__forms_frame, textvariable=self.dni_error,
                                    foreground="Red")
        self.__label_room_error = ttk.Label(self.__forms_frame, textvariable=self.room_error,
                                            foreground="Red")
        
        self.__label_name.grid(column=0, row=0, sticky="W E", padx=5)
        self.__label_last_name.grid(column=1, row=0, sticky="W E", padx=5)
        self.__label_dni.grid(column=2, row=0, sticky="W E", padx=5)
        self.__label_room.grid(column=3, row=0, sticky="W E", padx=5)
        self.__label_entry_date.grid(column=4, row=0, sticky="W E", padx=5)
        self.__label_exit_date.grid(column=5, row=0, sticky="W E", padx=5)

        self.__label_name_error.grid(column=0, row=2, sticky='W N', padx=5)
        self.__label_last_name_error.grid(column=1, row=2, sticky='W N', padx=5)
        self.__label_dni_error.grid(column=2, row=2, sticky='W N', padx=5)
        self.__label_room_error.grid(column=3, row=2, sticky='W N', padx=5)

    def __forms(self):
        self.__name_form = ttk.Entry(self.__forms_frame, validate="all",
                            validatecommand=(self.__forms_frame.register(
                                self.controller.validate_string), '%P'),
                            textvariable=self.name_client)
        self.__last_name_form = ttk.Entry(self.__forms_frame,validate="all",
                            validatecommand=(self.__forms_frame.register(
                               self.controller.validate_string), '%P'),
                            textvariable=self.last_name)
        self.__dni_form = ttk.Entry(self.__forms_frame, validate="all",
                            validatecommand=(self.__forms_frame.register(
                               self.controller.validate_number), '%P'),
                            textvariable=self.dni)
        self.entry_date_form = DateEntry(self.__forms_frame, selectmode="dia",
                                        date_pattern='yyyy-MM-dd',
                                        textvariable=self.entry_date,
                                        state="readonly")
        self.__exit_date_form = DateEntry(self.__forms_frame, selectmode="dia",
                                        date_pattern='yyyy-MM-dd',
                                        textvariable=self.exit_date,
                                        state="readonly")

        self.__name_form.grid(column=0, row=1, sticky="W", padx=5)
        self.__last_name_form.grid(column=1, row=1, sticky="W", padx=5)
        self.__dni_form.grid(column=2, row=1, sticky="W", padx=5)
        self.room_form.grid(column=3, row=1, sticky="W", padx=5)
        self.entry_date_form.grid(column=4, row=1, sticky="W", padx=5)
        self.__exit_date_form.grid(column=5, row=1, sticky="W", padx=5)
        self.controller.avalible_rooms('',self.variable_button,self.room_form,self.entry_date,self.exit_date)
        self.entry_date_form.bind("<<DateEntrySelected>>",self.__date_event)
        self.__exit_date_form.bind("<<DateEntrySelected>>",self.__date_event)

    def __buttons(self):
        self.__action_button = ttk.Button(self.__forms_frame, textvariable=self.variable_button,
                        padding="10 5 10 5", command=
                        lambda : self.controller.action_press(self.format_data_client()))
        self.__create_button = ttk.Button(self.__tools_frame, text="Crear", padding="10 5 10 5",
                        command= lambda : self.set_variables("Guardar"))
        self.__clients_button = ttk.Button(self.__tools_frame, text="Clientes", padding="10 5 10 5",
                        command= lambda : self.set_variables('Clientes'))
        self.__query_button = ttk.Button(self.__tools_frame, text="Consultar",
                            padding="10 5 10 5",
                            command=lambda: self.set_variables("Buscar"))
        self.__update_button = ttk.Button(self.__tools_frame, text="Actualizar",
                            padding="10 5 10 5",
                            command=lambda : self.__show_data(self))
        self.__delete_button = ttk.Button(self.__tools_frame, text="Borrar",
                        padding="10 5 10 5", command = lambda : self.controller.delete_client())
        
        self.__action_button.grid(column=5, row=2, sticky="W", pady=10)
        self.__create_button.grid(column=0, row=0, sticky="W", padx=20)
        self.__clients_button.grid(column=1, row=0, sticky="W", padx=20)
        self.__query_button.grid(column=2, row=0, sticky="W", padx=20)
        self.__update_button.grid(column=3, row=0, sticky="W", padx=20)
        self.__delete_button.grid(column=4, row=0, sticky="W", padx=20)

    def __tree_view(self):
        
        self.__scrol = ttk.Scrollbar(self.__data_list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand = self.__scrol)
        self.tree['yscrollcommand'] = self.__scrol.set
        self.tree['columns'] = ('nombre', 'apellido', 'DNI', 'habitacion',
                                    'fecha ingreso', 'fecha salida')
        self.tree.grid(column=0,row=0)
        self.__scrol.grid(column=1,row=0,sticky=("N,S"))
        self.tree.column('#0', width=50, minwidth=10)
        self.tree.heading('#0', text='ID')
        self.tree.column('nombre', width=120, minwidth=10)
        self.tree.heading('nombre', text='Nombre')
        self.tree.column('apellido', width=120, minwidth=10)
        self.tree.heading('apellido', text='Apellido')
        self.tree.column('DNI', width=100, minwidth=10)
        self.tree.heading('DNI', text='DNI')
        self.tree.column('habitacion', width=100, minwidth=10)
        self.tree.heading('habitacion', text='Habitacion')
        self.tree.column('fecha ingreso', width=100, minwidth=10)
        self.tree.heading('fecha ingreso', text='Fecha ingreso')
        self.tree.column('fecha salida', width=100, minwidth=10)
        self.tree.heading('fecha salida', text='Fecha Salida')
        self.tree.bind('<B1-Motion>', self.__recize_false)
        self.tree.bind('<Double-1>', self.__show_data)
        self.controller.read_clients(self.tree)

    """Establecer las variables de la clase (borrar formularios, control de habitacion y borrar etiquetas"""
    def set_variables(self,action=""):
        self.name_client.set("")
        self.last_name.set("")
        self.dni.set("")
        self.room.set("Seleccionar")
        if action == 'Clientes':
            self.controller.read_clients(self.tree)
        elif action == "Buscar":
            self.variable_button.set("Buscar")
            self.entry_date.set("")
            self.exit_date.set("")
        else:
            self.variable_button.set("Guardar")
            today = datetime.now()
            date = str(today.strftime("%Y-%m-%d"))
            self.entry_date.set(date)
            self.exit_date.set(date)
        self.controller.avalible_rooms('',self.variable_button,self.room_form,self.entry_date,self.exit_date)
        self.set_labels()

    def set_labels(self):
        self.name_error.set("")
        self.last_name_error.set("")
        self.dni_error.set("")
        self.room_error.set("")
    
    """Enviar datos elegidos del tree view a los formularios """
    def __show_data(self,event=''):
        try :
            self.variable_button.set("Actualizar")
            client = self.tree.item(self.tree.focus())
            self.id_client = client['text']
            self.name_client.set(client['values'][0])
            self.last_name.set(client['values'][1])
            self.dni.set(client['values'][2])
            self.room.set((client['values'][3]))
            self.entry_date.set(str(client['values'][4]))
            self.exit_date.set(str(client['values'][5]))
        except :
            self.message_box(('Actualizar','Seleccione el cliente que quiere actualizar'))
    
    """Eventos del tree view como doble clip y clip sostenido"""         
    def __recize_false(self,event):
        return "break"
    
    def __date_event(self,evevent):
        self.controller.avalible_rooms("date_selected",self.variable_button,self.room_form,self.entry_date,self.exit_date)
    
    """Estructura de datos de los formularios, que se enviaran al contralador para sus diferentes manipulaciones"""
    def format_data_client(self):
        data = {'id_client': self.id_client,
                'name': self.name_client.get().title(),
                'last_name': self.last_name.get().title(),
                'dni': self.dni.get(),
                'room': self.room.get(),
                'entry_date': self.entry_date.get(),
                'exit_date': self.exit_date.get()
                }
        return data
    
    """Metodo para enviar mensajes de alerta al usuario"""
    def message_box(self,message=''):
        if message != '':
            messagebox.showinfo(message[0],message[1])
        else:
            ask= messagebox.askyesno("Borrar cliente",
                                    "¿Desea borrar el cliente?")
            return ask