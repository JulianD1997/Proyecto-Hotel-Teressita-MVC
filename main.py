import controller.control as controller
"""
    Esta aplicación fue creada con el fin de darle una optimización a la 
    administración de un hotel donde se puede crear, leer,
    actualizar y borrar una reserva de un cliente.

    Cuenta con tres apartados dentro:
    Espacio de formularios: 
        Acá se puede realizar diferentes tipos de consultas:
            podemos ingresar
                Nombre, apellido, DNI, habitación, fecha de entrada y
                fecha de salida para darle la reserva al cliente.
            Para poder generar un nuevo cliente.
            Igualmente, este espacio nos permite actualizar los datos de una
            reserva, ya que automáticamente envía los datos del cliente que deseemos
            actualizar.
            También nos permite ejecutar la búsqueda de clientes por medio
            de los formularios, podemos buscar por:
                nombre, apellido, DNI, habitación
                fecha de entrada y fecha de salida.
            Por último tenemos un botón multifuncional que nos permite guardar, buscar
            y actualizar según su valor(Este valor es el nombre que tiene que el botón en el momento)
    Espacio de lectura de clientes:
        Este nos brinda la facilidad de ver todos los clientes registrados hasta 
        el momento igualmente se podrá visualizar los clientes que coinciden con la búsqueda.
        Este espacio también los brinda seleccionar un cliente para posterior darle al botón 
        Update o Delete situados en la caja de herramientas y también para más facilidad, darle doble al cliente 
        que se quiera modificar para que envíe los datos a los formularios y este cambie el valor del botón multifuncional a "Update".
    Espacio de Herramientas:
        Llamada caja de herramientas, ya que nos ofrece 5 tipos de botones:
            botón Created:
                borrar los formularios y actualiza el valor del botón multifuncional situado en el espacio formulario
                con el valor "Save"
            botón Clients
                borrar formularios y actualizar la vista del treeview con todos los datos de los clientes registrados
                hasta el momento
            botón Search
                borrar todos los formularios para que el cliente pueda realizar una búsqueda, esta búsqueda se puede realizar
                ingresando un solo campo o varios. Igualmente, cambia el valor del botón multifuncional a "Search"
            botón Update
                Esté nos permite enviar todos los datos del cliente seleccionado en el espacio client list
            botón Delete
                por último el botón Delete que nos permite borrar un cliente seleccionado en el espacio client list
                este mismo debe estar seleccionado de no estarlo se mostrara un aviso de alerta que indicara que seleccione el 
                cliente igualmente para la eliminación completa de este cliente saldrá un cuadro de confirmación que preguntara si está seguro de eliminarlo
                el cliente
    cada acción tiene un mensaje de alerta que nos informara si fue correcta operación.
"""
if __name__ == "__main__":
    main = controller.Controller()
    main.run_window()