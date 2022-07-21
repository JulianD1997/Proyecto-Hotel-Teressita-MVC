import tkinter
from tkinter import ttk
from tkcalendar import DateEntry

#interface 
class Interface():
    __name = tkinter.StringVar()
    __last_name = tkinter.StringVar()
    __dni = tkinter.StringVar()
    __room = tkinter.StringVar()
    __entry_date = tkinter.StringVar()
    __exit_date = tkinter.StringVar()
    __variable_button = tkinter.StringVar()
    __name_error = tkinter.StringVar()
    __last_name_error = tkinter.StringVar()
    __dni_error = tkinter.StringVar()
    __room_error = tkinter.StringVar()

    def __init__(self,root):
        self.root = root
        self.root.resizable(False, False)
        self.__room.set("Seleccionar")
        self.__variable_button.set("Guardar")
        self.__frames()
        self.__labels()
        self.__forms()
        self.__buttons()
        self.__tree_view()
        
    def __frames(self):
        self.main_frame = ttk.Frame(self.root,padding=10)
        self.forms_frame = ttk.LabelFrame(self.main_frame,text="Formulario cliente",padding=10)
        self.data_list_frame = ttk.LabelFrame(self.main_frame,text="Lista de clientes",padding=10)
        self.tools_frame = ttk.LabelFrame(self.main_frame,text="Herramientas",padding=10)

        self.main_frame.grid(column=0, row=0)
        self.forms_frame.grid(column=0, row=0)
        self.data_list_frame.grid(column=0, row=1,pady=5)
        self.tools_frame.grid(column=0, row=2, pady=5)

    def __labels(self):
        self.label_name = ttk.Label(self.forms_frame, text="Nombre")
        self.label_last_name = ttk.Label(self.forms_frame, text="Apellido")
        self.label_dni = ttk.Label(self.forms_frame, text="DNI")
        self.label_room = ttk.Label(self.forms_frame, text="Habitacion")
        self.label_entry_date = ttk.Label(self.forms_frame, text="Fecha de Ingreso")
        self.label_exit_date = ttk.Label(self.forms_frame, text="Fechas de salida")
        
        self.label_name_error = ttk.Label(self.forms_frame, textvariable=self.__name_error,
                                    foreground="Red")
        self.label_last_name_error = ttk.Label(self.forms_frame, textvariable=self.__last_name_error,
                                    foreground="Red")
        self.label_dni_error = ttk.Label(self.forms_frame, textvariable=self.__dni_error,
                                    foreground="Red")
        self.label_room_error = ttk.Label(self.forms_frame, textvariable=self.__room_error,
                                            foreground="Red")
        
        self.label_name.grid(column=0, row=0, sticky="W E", padx=5)
        self.label_last_name.grid(column=1, row=0, sticky="W E", padx=5)
        self.label_dni.grid(column=2, row=0, sticky="W E", padx=5)
        self.label_room.grid(column=3, row=0, sticky="W E", padx=5)
        self.label_entry_date.grid(column=4, row=0, sticky="W E", padx=5)
        self.label_exit_date.grid(column=5, row=0, sticky="W E", padx=5)

        self.label_name_error.grid(column=0, row=2, sticky='W N', padx=5)
        self.label_last_name_error.grid(column=1, row=2, sticky='W N', padx=5)
        self.label_dni_error.grid(column=2, row=2, sticky='W N', padx=5)
        self.label_room_error.grid(column=3, row=2, sticky='W N', padx=5)

    def __forms(self):
        self.name_form = ttk.Entry(self.forms_frame, validate="all",
                            validatecommand=(self.forms_frame.register(
                                validar_caracteres), '%P'),
                            textvariable=self.__name)
        self.last_name_form = ttk.Entry(self.forms_frame,validate="all",
                            validatecommand=(self.forms_frame.register(
                                validar_caracteres), '%P'),
                            textvariable=self.__last_name)
        self.dni_form = ttk.Entry(self.forms_frame, validate="all",
                            validatecommand=(self.forms_frame.register(
                               validar_numeros), '%P'),
                            textvariable=self.__dni)
        self.room_form = ttk.Combobox(self.forms_frame, textvariable=self.__room,
                                    state="readonly")
        self.entry_date_form = DateEntry(self.forms_frame, selectmode="dia",
                                        date_pattern='yyyy-MM-dd',
                                        textvariable=self.__entry_date,
                                        state="readonly")
        self.exit_date_form = DateEntry(self.forms_frame, selectmode="dia",
                                        date_pattern='yyyy-MM-dd',
                                        textvariable=self.__exit_date,
                                        state="readonly")

        self.name_form.grid(column=0, row=1, sticky="W", padx=5)
        self.last_name_form.grid(column=1, row=1, sticky="W", padx=5)
        self.dni_form.grid(column=2, row=1, sticky="W", padx=5)
        self.room_form.grid(column=3, row=1, sticky="W", padx=5)
        self.entry_date_form.grid(column=4, row=1, sticky="W", padx=5)
        self.exit_date_form.grid(column=5, row=1, sticky=W, padx=5)

    def __buttons(self):
        self.action_button = ttk.Button(self.forms_frame, textvariable=self.__variable_button,
                        padding="10 5 10 5", command=accion_boton)
        self.create_button = ttk.Button(self.tools_frame, text="Crear", padding="10 5 10 5",
                        command=setear_forms)
        self.clients_button = ttk.Button(self.tools_frame, text="Clientes", padding="10 5 10 5",
                        command=leer_cliente)
        self.query_button = ttk.Button(self.tools_frame, text="Consultar",
                            padding="10 5 10 5",
                            command=lambda: setear_forms("Consultar"))
        self.update_button = ttk.Button(self.tools_frame, text="Actualizar",
                            padding="10 5 10 5",
                            command=mostrar_datos)
        self.delete_button = ttk.Button(self.tools_frame, text="Borrar",
                        padding="10 5 10 5", command=borrar_cliente)
        
        self.action_button.grid(column=5, row=2, sticky="W", pady=10)
        self.create_button.grid(column=0, row=0, sticky="W", padx=20)
        self.clients_button.grid(column=1, row=0, sticky="W", padx=20)
        self.query_button.grid(column=2, row=0, sticky="W", padx=20)
        self.update_button.grid(column=3, row=0, sticky="W", padx=20)
        self.delete_button.grid(column=4, row=0, sticky="W", padx=20)

    def __tree_view(self):
        self.__tree = ttk.Treeview(self.data_list_frame)
        self.__scrol = ttk.Scrollbar(self.data_list_frame, orient="vertical", command=self.__tree.yview)
        self.__tree.configure(yscrollcommand = self.__scrol)
        self.__tree['yscrollcommand'] = self.__scrol.set
        self.__tree['columns'] = ('nombre', 'apellido', 'DNI', 'habitacion',
                                    'fecha ingreso', 'fecha salida')
        self.__tree.grid(column=0,row=0)
        self.__scrol.grid(column=1,row=0,sticky=("N,S"))
        self.__tree.column('#0', width=50, minwidth=10)
        self.__tree.heading('#0', text='ID')
        self.__tree.column('nombre', width=120, minwidth=10)
        self.__tree.heading('nombre', text='Nombre')
        self.__tree.column('apellido', width=120, minwidth=10)
        self.__tree.heading('apellido', text='Apellido')
        self.__tree.column('DNI', width=100, minwidth=10)
        self.__tree.heading('DNI', text='DNI')
        self.__tree.column('habitacion', width=100, minwidth=10)
        self.__tree.heading('habitacion', text='Habitacion')
        self.__tree.column('fecha ingreso', width=100, minwidth=10)
        self.__tree.heading('fecha ingreso', text='Fecha ingreso')
        self.__tree.column('fecha salida', width=100, minwidth=10)
        self.__tree.heading('fecha salida', text='Fecha Salida')
        self.__tree.bind("<B1-Motion>", no_redimensionar)
