import tkinter
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
import traceback
import re
class Interface():
    def __init__(self,root):
        pass

root = tkinter.Tk()
root.title("Hotel Teressitta")
root.resizable(False, False)
crear_tabla()

# Variables
nombre = tkinter.StringVar()
apellido = tkinter.StringVar()
dni = tkinter.StringVar()
habitacion = tkinter.StringVar()
fecha_ingreso = tkinter.StringVar()
fecha_salida = tkinter.StringVar()
boton_variable = tkinter.StringVar()
habitacion.set("Seleccionar")
boton_variable.set("Guardar")
nombre_error = tkinter.StringVar()
apellido_error = tkinter.StringVar()
dni_error = tkinter.StringVar()
habitacion_error = tkinter.StringVar()

# Se declaran los Frames
marco = ttk.Frame(root, padding=10)
formulario = ttk.LabelFrame(
    marco, height=700, text="Formulario cliente", padding=10)
lista_datos = ttk.LabelFrame(
    marco, height=700, text="Lista de clientes", padding=10)
herramientas = ttk.LabelFrame(
    marco, height=700, text="Herramientas", padding=10)

# ComboBox
comboBox_Habitaciones = ttk.Combobox(formulario, textvariable=habitacion,
                                     state="readonly")

# Formularios
formulario_nombre = ttk.Entry(formulario, validate="all",
                              validatecommand=(formulario.register(
                                  validar_caracteres), '%P'),
                              textvariable=nombre)
formulario_apellido = ttk.Entry(formulario, validate="all",
                                validatecommand=(formulario.register(
                                    validar_caracteres), '%P'),
                                textvariable=apellido)
formulario_DNI = ttk.Entry(formulario, validate="all",
                           validatecommand=(formulario.register(
                               validar_numeros), '%P'),
                           textvariable=dni)
formulario_habitacion = ttk.Entry(formulario, textvariable=habitacion)
formulario_fecha_ingreso = DateEntry(formulario, selectmode="dia",
                                     date_pattern='yyyy-MM-dd',
                                     textvariable=fecha_ingreso,
                                     state="readonly")
formulario_fecha_salida = DateEntry(formulario, selectmode="dia",
                                    date_pattern='yyyy-MM-dd',
                                    textvariable=fecha_salida,
                                    state="readonly")

# Botones
boton_accion = ttk.Button(formulario, textvariable=boton_variable,
                          padding="10 5 10 5", command=accion_boton)
boton_crear = ttk.Button(herramientas, text="Crear", padding="10 5 10 5",
                         command=setear_forms)
boton_clientes = ttk.Button(herramientas, text="Clientes", padding="10 5 10 5",
                            command=leer_cliente)
boton_consultar = ttk.Button(herramientas, text="Consultar",
                             padding="10 5 10 5",
                             command=lambda: setear_forms("Consultar"))
boton_actualizar = ttk.Button(herramientas, text="Actualizar",
                              padding="10 5 10 5",
                              command=mostrar_datos)
boton_borrar = ttk.Button(herramientas, text="Borrar",
                          padding="10 5 10 5", command=borrar_cliente)

# Etiquetas
etiqueta_nombre = ttk.Label(formulario, text="Nombre")
etiqueta_apellido = ttk.Label(formulario, text="Apellido")
etiqueta_DNI = ttk.Label(formulario, text="DNI")
etiqueta_habitacion = ttk.Label(formulario, text="Habitacion")
etiqueta_fecha_ingreso = ttk.Label(formulario, text="Fecha de Ingreso")
etiqueta_fecha_salida = ttk.Label(formulario, text="Fechas de salida")
etiqueta_nombre_error = ttk.Label(formulario, textvariable=nombre_error,
                                  foreground="Red")
etiqueta_apellido_error = ttk.Label(formulario, textvariable=apellido_error,
                                    foreground="Red")
etiqueta_DNI_error = ttk.Label(formulario, textvariable=dni_error,
                               foreground="Red")
etiqueta_habitacion_error = ttk.Label(formulario,
                                      textvariable=habitacion_error,
                                      foreground="Red")

# Se empaquetan los elementos
marco.grid(column=0, row=0)
formulario.grid(column=0, row=0)
lista_datos.grid(column=0, row=1, pady=5)
herramientas.grid(column=0, row=2)

etiqueta_nombre.grid(column=0, row=0, sticky=SW, padx=5)
formulario_nombre.grid(column=0, row=1, sticky=W, padx=5)
etiqueta_nombre_error.grid(column=0, row=2, sticky='W N', padx=5)
etiqueta_apellido.grid(column=1, row=0, sticky=W, padx=5)
formulario_apellido.grid(column=1, row=1, sticky=W, padx=5)
etiqueta_apellido_error.grid(column=1, row=2, sticky='W N', padx=5)
etiqueta_DNI.grid(column=2, row=0, sticky=W, padx=5)
formulario_DNI.grid(column=2, row=1, sticky=W, padx=5)
etiqueta_DNI_error.grid(column=2, row=2, sticky='W N', padx=5)
etiqueta_habitacion.grid(column=3, row=0, sticky=W, padx=5)
comboBox_Habitaciones.grid(column=3, row=1, sticky=W, padx=5)
etiqueta_habitacion_error.grid(column=3, row=2, sticky='W N', padx=5)
etiqueta_fecha_ingreso.grid(column=4, row=0, sticky=W, padx=5)
formulario_fecha_ingreso.grid(column=4, row=1, sticky=W, padx=5)
etiqueta_fecha_salida.grid(column=5, row=0, sticky=W, padx=5)
formulario_fecha_salida.grid(column=5, row=1, sticky=W, padx=5)

boton_accion.grid(column=5, row=2, sticky=W, pady=10)
boton_crear.grid(column=0, row=0, sticky=W, padx=20)
boton_actualizar.grid(column=1, row=0, sticky=W, padx=20)
boton_clientes.grid(column=2, row=0, sticky=W, padx=20)
boton_consultar.grid(column=3, row=0, sticky=W, padx=20)
boton_borrar.grid(column=4, row=0, sticky=W, padx=20)

# Lista de clientes
arbol = ttk.Treeview(lista_datos)

# Scrollbar
scrol = ttk.Scrollbar(lista_datos, orient="vertical", command=arbol.yview,)
arbol.configure(yscrollcommand=scrol)
arbol['yscrollcommand'] = scrol.set
leer_cliente()
habitaciones_disponibles()
formulario_fecha_ingreso.bind("<<DateEntrySelected>>",
                              habitaciones_disponibles)
formulario_fecha_salida.bind("<<DateEntrySelected>>",
                             habitaciones_disponibles)

arbol['columns'] = ('nombre', 'apellido', 'DNI', 'habitacion',
                    'fecha ingreso', 'fecha salida',)
arbol.grid(column=0, row=0)
scrol.grid(column=1, row=0, sticky=(N, S))
arbol.column('#0', width=50, minwidth=10)
arbol.heading('#0', text='ID')
arbol.column('nombre', width=120, minwidth=10)
arbol.heading('nombre', text='Nombre')
arbol.column('apellido', width=120, minwidth=10)
arbol.heading('apellido', text='Apellido')
arbol.column('DNI', width=100, minwidth=10)
arbol.heading('DNI', text='DNI')
arbol.column('habitacion', width=100, minwidth=10)
arbol.heading('habitacion', text='Habitacion')
arbol.column('fecha ingreso', width=100, minwidth=10)
arbol.heading('fecha ingreso', text='Fecha ingreso')
arbol.column('fecha salida', width=100, minwidth=10)
arbol.heading('fecha salida', text='Fecha Salida')
arbol.bind("<B1-Motion>", no_redimensionar)

root.mainloop()

