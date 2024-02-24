"""
El modulo Vista es el encargado de armar la ventana interactiva e
interactuar con el usuario para poder brindar al controlador los comandos
que este quiere realizar
"""
import sys
import os

dir_path = os.path.dirname(os.path.abspath(__file__))
main_path = dir_path[0:(len(dir_path)-4)]
sys.path.append(main_path)

from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from widgets.widgets import Ventana, BotonRadio, Boton, Texto, Entrada, Combobox, Tabla

class Login(Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        abs_path = str(__file__)[:-len("bin/view.py")]
        ico_path = fr"{abs_path}src\img\icono.ico"

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.configure(background="#DCDAD5")
        self.resizable(False, False)
        self.title("Login")
        self.iconbitmap(ico_path)

        self.user = StringVar()
        self.passw = StringVar()

        # label(master, col.num, row.num, columspan, rowspan, texto_de_label)
        # entry(master, col.num, row.num, columspan, rowspan, variable_de_entry)

        self.texto_itemid = Texto(self, 0, 0, 1, 1, "Usuario")
        self.entry_itemid = Entrada(self, 1, 0, 2, 1, self.user)

        self.texto_nombre = Texto(self, 0, 1, 1, 1, "Contraseña")
        self.entry_nombre = Entrada(self, 1, 1, 2, 1, self.passw)
        self.entry_nombre.config(show='*')

        # boton(master, col.num, row.num, columspan, rowspan, texto_de_boton, funcion_linkeada)

        self.boton_login = Boton(self, 0, 2, 2, 1, "LOGIN", controller.login)
        self.boton_registro = Boton(self, 0, 3, 2, 1, "REGISTRO", controller.register)

    def login_error(
            self
    ):
        mb.showerror("Error Login", "Usuario o password erroneo")

class Register(Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        # self.tablas = self.controller.db_admin.get_tables()

        abs_path = str(__file__)[:-len("bin/view.py")]
        ico_path = fr"{abs_path}src\img\icono.ico"

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.configure(background="#DCDAD5")
        self.resizable(False, False)
        self.title("Registro")
        self.iconbitmap(ico_path)

        self.registration_state = BooleanVar()
        self.registration_state.set(True)
        
        self.table = StringVar()

        self.usuario = StringVar()
        self.passw = StringVar()
        self.rpassw = StringVar()
        self.skey = StringVar()
        self.rskey = StringVar()

        self.table.set("")
        self.usuario.set("")
        self.passw.set("")
        self.rpassw.set("")
        self.skey.set("")
        self.rskey.set("")

        # label(master, col.num, row.num, columspan, rowspan, texto_de_label)

        text = """
        Bienvenido al registro de usuarios de la aplicaicion Gestor de Deposito.

        Si desea registrar un usuario nuevo a una tabla ya esxistente, le pediremos que complete
        los campos indicando la tabla y la Security Key* de la misma.

        Por el contrario si desea registrar una tabla nueva, se le pedira el nombre que quiera
        indicar a la misma y la security key asociada.

            *La security Key es un codigo asociado a la talba, cualquier otro usuario que quiera
            regustrarse debe proveer la misma.
        """

        self.texto_desc = Texto(self, 0, 0, 4, 1, text)

        # boton(master, col.num, row.num, columspan, rowspan, texto_de_boton, valor, variable)

        self.boton_login = BotonRadio(self, 0, 2, 2, 1, "Tabla Existente", False, self.registration_state, self.regist_state)
        self.boton_registro = BotonRadio(self, 2, 2, 2, 1, "Nueva Tabla", True, self.registration_state, self.regist_state)

        # combobox(master, col.num, row.num, columspan, rowspan, lista_de_cbox, variable_de_entry)

        self.texto_tabla = Texto(self, 0, 3, 1, 1, "Tabla")
        self.entry_tabla = Entrada(self, 1, 3, 1, 1, self.table)
        self.combo_tabla = Combobox(self, 3, 3, 1, 1, self.controller.db_admin.get_tables(), self.table)
        self.combo_tabla.config(state=DISABLED)

        # label(master, col.num, row.num, columspan, rowspan, texto_de_label)
        # entry(master, col.num, row.num, columspan, rowspan, variable_de_entry)

        self.texto_usuario = Texto(self, 0, 4, 1, 1, "Usuario")
        self.entry_usuario = Entrada(self, 1, 4, 3, 1, self.usuario)

        self.texto_pass = Texto(self, 0, 5, 1, 1, "Password")
        self.entry_pass = Entrada(self, 1, 5, 3, 1, self.passw)
        self.entry_pass.config(show='*')

        self.texto_repetpass = Texto(self, 0, 6, 1, 1, "Repetir Password")
        self.texto_repetpass.config(width=25)
        self.entry_repetpass = Entrada(self, 1, 6, 3, 1, self.rpassw)
        self.entry_repetpass.config(show='*')

        self.texto_skey = Texto(self, 0, 7, 1, 1, "Security Key")
        self.entry_skey = Entrada(self, 1, 7, 3, 1, self.skey)
        self.entry_skey.config(show='*')

        self.texto_repetskey = Texto(self, 0, 8, 1, 1, "Repetir Security Key")
        self.entry_repetskey = Entrada(self, 1, 8, 3, 1, self.rskey)
        self.entry_repetskey.config(show='*')

        # boton(master, col.num, row.num, columspan, rowspan, texto_de_boton, funcion_linkeada)

        self.boton_registro = Boton(self, 0, 9, 2, 2, "REGISTRO", self.controller.user_create)
        self.boton_registro.config(width=20)
        self.boton_cancelar = Boton(self, 2, 9, 2, 2, "CANCELAR", self.controller.register_cancel)
        self.boton_cancelar.config(width=20)

    def regist_state(
            self
    ):
        if self.registration_state.get():
            self.combo_tabla.config(state=DISABLED)
            self.entry_tabla.config(state=NORMAL)
            self.entry_repetskey.config(state=NORMAL)
            self.rskey.set("")
            self.entry_repetskey.config(show='*')
        else:
            self.combo_tabla.config(state="readonly")
            self.entry_tabla.config(state=DISABLED)
            self.entry_repetskey.config(state=DISABLED)
            self.rskey.set(" --- Unused --- ")
            self.entry_repetskey.config(show='')

    def error_messages(
            self, titulo, mensaje
    ):
        mb.showerror(titulo, mensaje)

    def registro_existoso(
            self
    ):
        mb.showinfo("Registro exitoso", "Se registro correctamente.\nPorfavor, inicia el programa nuevamente")

class View(Tk):
    """
    La clase Vista se contruye heredando de la libreria
    `Tkinter <https://docs.python.org/es/3/library/tkinter.html>`_
    el moudlo `Tk <https://docs.python.org/es/3/library/tk.html>`_.
    El controlador llama a la clase Vista y cuando se crea el objeto de
    la clase Controlador se genera el mainloop de la aplicacion.
    """
    
    def __init__(self, controlador):
        """
        En el constructor de la clase se pide como parametro la clase Controlador,
        para poder linkear las instancias de la clase Controlador, con las acciones de los
        botones de la aplicacion.

        Como primer paso se utiliza la intancia *super()* para invocar al constructor de
        la clase `Tk <https://docs.python.org/es/3/library/tk.html>`_.

        Luego se configura el estilo y atributos de la ventana principal, se definen las
        variables de la aplicacion y se invoca al metodo  *_insertar_widgets()*, que se
        encarga de incertar todos los widgets en la ventana.

        Args:
            controlador (clase): Clase Controlador que se cruza con la de Vista para poder utilizar las instancias de Controlador
        """
        super().__init__()
        self.controlador = controlador

        abs_path = str(__file__)[:-len("bin/view.py")]
        ico_path = fr"{abs_path}src\img\icono.ico"

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.configure(background="#DCDAD5")
        self.resizable(False, False)
        self.title(f"Gestor de Deposito - {self.controlador.tabla}")
        self.iconbitmap(ico_path)

        self.valor_item_id = StringVar()
        self.valor_nombre = StringVar()
        self.valor_precio = DoubleVar()
        self.valor_stock = IntVar()
        self.valor_categoria = StringVar()

        self.estado_consulta = BooleanVar()
        self.estado_consulta.set(False)

        #   (id_de_elemento, heading, ancho, justificacion)
        self.contenido_tabla = [
            ("itemid", "Item ID", 70, CENTER),
            ("nombre", "Nombre", 220, W),
            ("precio", "Precio", 150, W),
            ("stock", "Stock", 150, W),
            ("categoria", "Categoria", 200, W),
            ("fecha", "Fecha", 150, W),
        ]

        self.lista_categoria = self.controlador.model.extract_categoria()

        self.__insertar_widgets()

    def __insertar_widgets(
            self
    ):
        """
        Instancia interna que se encarga del diseño y colocacion de los widgets en la
        ventana. 
        """

        # ventana(master, col.num, row.num, columspan, rowspan, texto_de_cuadro)
        self.ventana_datos = Ventana(self, 0, 0, 1, 1, "Datos")
        self.ventana_botones = Ventana(self, 1, 0, 1, 1, "Acciones")
        self.ventana_tabla = Ventana(self, 0, 1, 2, 1, "Tabla")

        # label(master, col.num, row.num, columspan, rowspan, texto_de_label)
        # entry(master, col.num, row.num, columspan, rowspan, variable_de_entry)

        self.texto_itemid = Texto(self.ventana_datos, 0, 0, 1, 1, "Item ID")
        self.entry_itemid = Entrada(self.ventana_datos, 1, 0, 2, 1, self.valor_item_id)

        self.texto_nombre = Texto(self.ventana_datos, 0, 1, 1, 1, "Nombre")
        self.entry_nombre = Entrada(self.ventana_datos, 1, 1, 2, 1, self.valor_nombre)

        self.texto_precio = Texto(self.ventana_datos, 0, 2, 1, 1, "Precio")
        self.entry_precio = Entrada(self.ventana_datos, 1, 2, 2, 1, self.valor_precio)

        self.texto_stock = Texto(self.ventana_datos, 0, 3, 1, 1, "Stock")
        self.entry_stock = Entrada(self.ventana_datos, 1, 3, 2, 1, self.valor_stock)

        # combobox(master, col.num, row.num, columspan, rowspan, lista_de_cbox, variable_de_entry)

        self.texto_categoria = Texto(self.ventana_datos, 0, 4, 1, 1, "Categoria")
        self.entry_categoria = Entrada(self.ventana_datos, 1, 4, 1, 1, self.valor_categoria)
        self.combo_categoria = Combobox(self.ventana_datos, 2, 4, 1, 1, self.lista_categoria, self.valor_categoria)

        # boton(master, col.num, row.num, columspan, rowspan, texto_de_boton, funcion_linkeada)

        self.boton_alta = Boton(self.ventana_botones, 0, 0, 1, 1, "ALTA", self.controlador.alta)
        self.boton_baja = Boton(self.ventana_botones, 1, 0, 1, 1, "ELIMINAR", self.controlador.baja)
        self.boton_actualizar = Boton(self.ventana_botones, 0, 1, 1, 1, "ACTUALIZAR", self.controlador.actualizar)
        self.boton_consulta = Boton(self.ventana_botones, 1, 1, 1, 1, "CONSULTA", self.controlador.consulta)
        self.boton_buscar = Boton(self.ventana_botones, 0, 2, 1, 1, "BUSCAR", self.controlador.buscar)
        self.boton_limpiar = Boton(self.ventana_botones, 1, 2, 1, 1, "LIMPIAR", self.controlador.limpiar)
        self.boton_generar_id = Boton(self.ventana_botones, 0, 3, 1, 1, "GENERAR ID", self.controlador.genid)
        self.boton_exportar = Boton(self.ventana_botones, 1, 3, 1, 1, "EXPORTAR", self.controlador.exportar)

        # (master, contenido_de_tabla)

        self.tabla_principal = Tabla(self.ventana_tabla, self.contenido_tabla)

    def error(
            self, codigo
    ):
        """
        En este metodo el controlador envia un codigo de error predeterminado y segun cual sea el
        codigo se displaya un mensaje de error puntual para cada caso.

        Args:
            codigo (str): Codigo predefinido en el controlador que se envia en el caso de que ocurra algun errot en la aplicacion.
        """

        mensajes = {
            "ERROR.ACTUALIZAR": ["Error de Actualizar", "Realice previamente una consulta de algun dato"],
            "ERROR.GENID": ["Error en Generar ID", "Completar los campos para generar un id automaticamente"],
            "ERROR.CONSULTA": ["Error de Consulta", "Seleccione un elemento para consultar"],
            "ERROR.BAJA": ["Error en Eliminar", "Seleccione un elemento para eliminar"],
            "ERROR.ALTA.2ITEMID": ["Error en Item-ID", "Valor duplicado"],
            "ERROR.ALTA.ITEMID": ["Error en Item-ID",
                                  "Ingrese un valor correcto de Item-ID.\
                                   Utilice el fomrato de dos mayusculas y 6 digitos. Ej: AA-123456"],
            "ERROR.ALTA.INVALIDVALUE": ["Error en dato",
                                        "Ingrese un valor correcto"],
        }

        mb.showerror(mensajes[codigo][0], mensajes[codigo][1])

    def aviso_exportacion(
            self, codigo
    ):
        """
        Metodo que displaya un mensaje hacia donde se exporto la tabla.

        Args:
            codigo (int): Codigo predefinido en el controlador que se envia para informar donde se realizo la exportacion de la tabla.
        """
        
        mensajes = {
            0: "Se exporto con exito la tabla hacia la carpeta Documentos",
            1: "Se exporto con exito la tabal hacia el Escritorio",
            2: "Se exporto con exito la tabla hacia la ubicacion del programa"
        }

        mb.showinfo("Exportacion de tabla", mensajes[codigo])

def _main():
    pass

if __name__ == "__main__":
    _main()
