"""
Modulo principal que se encarga de gestionar el programa, desde aqui se invocan las
otras clases (Modeloy Vista), y se realiza toda la logica de la aplicacion.
"""
from sys import path as sp
from os import path as op
from os import getlogin

dir_path = op.dirname(op.abspath(__file__))
main_path = dir_path[0:(len(dir_path)-4)]
sp.append(main_path)

from tkinter import TclError
from sqlite3 import IntegrityError, OperationalError
from threading import Thread
from time import sleep
from datetime import datetime
from random import randint
from re import fullmatch
from openpyxl import Workbook
from bin.custom_errors import ErrorPassNotEqual, ErrorSkeyNotEqual, ErrorSkeyNotValid
from bin.custom_errors import TableInExistance, UserOrPassNotValid
from bin.view import View, Login, Register
from bin.model import Model, DbModel
from bin.observer import LogInObserver, LogOutObserver, CreateObserver, ReadObserver, DeleteObserver, UpdateObserver
from server.server import Servidor

class Controlador():
    """
    La clase Controlador va a ser la que se encargue, con sus
    instancia, de llevar este control de la aplicacion. Desde su constructor va a
    utilizar a las otras dos clases (Vista y Modelo), y mediante sus instancias generara
    la logica para poder operar la aplicaion.
    """
    def __init__(self):
        """
        Como se dijo anteriormenete, desde el constructor se invocaran a las otras dos clases
        y se inicializarade forma correcta la aplicacion.
        """

        self.server = Servidor()

        t = Thread(target=self.server.run_server, daemon=False)
        t.start()
        sleep(1)

        self.db_admin = DbModel()
        self.tabla = ""
        self.actual_user = ""

        self.__o_login = LogInObserver()
        self.__o_logout = LogOutObserver()
        self.__o_create = CreateObserver()
        self.__o_update = UpdateObserver()
        self.__o_delete = DeleteObserver()
        self.__o_read = ReadObserver()

        self.loging_state = None

        self.login_view = Login(self)
        self.login_view.mainloop()

        if self.loging_state == "logged":
            self.__o_login.update(self.actual_user)
            self.model = Model(self.tabla)
            self.view = View(self)
            self.limpiar()
            self.refresh_table()
            self.view.mainloop()
            self.__o_logout.update(self.actual_user)
            sleep(0.2)
            self.server.shutdown()
        elif self.loging_state == "registration":
            self.server.shutdown()
            self.registration_view = Register(self)
            self.registration_view.mainloop()
        else:
            self.server.shutdown()

    def login(
            self
    ):
        datos = (
            self.login_view.user.get(),
            self.login_view.passw.get() 
        )

        try:
            self.tabla = self.db_admin.access(datos)[0][0]
            self.loging_state = "logged"
            self.actual_user = self.login_view.user.get()
            self.login_view.destroy()
        except UserOrPassNotValid:
            self.login_view.login_error()

    def register(
            self
    ):
        self.loging_state = "registration"
        self.login_view.destroy()

    def register_cancel(
            self
    ):
        self.registration_view.destroy()
    
    def user_create(
            self
    ):
        def user_creation(self):
            try:
                datos = (
                    self.registration_view.usuario.get(),
                    self.registration_view.passw.get(),
                    self.registration_view.table.get()
                )

                if self.registration_view.passw.get() == self.registration_view.rpassw.get():

                    if self.db_admin.add_new_user_to_table(datos):
                        self.registration_view.registro_existoso()
                        return True
                    else:
                        self.registration_view.error_messages("Error Usuario", "El usuario ya existe")
                else:
                    raise ErrorPassNotEqual
                
            except ErrorPassNotEqual:
                self.registration_view.error_messages("Error Password", "Las passwords no coinciden")

        try:

            datos = [
                self.registration_view.table.get(),
                self.registration_view.usuario.get(),
                self.registration_view.passw.get(),
                self.registration_view.rpassw.get(),
                self.registration_view.skey.get(),
                self.registration_view.rskey.get()
            ]

            for i in datos:
                if len(i) == 0:
                    raise AttributeError

            if self.registration_view.registration_state.get():
                try:
                    if self.registration_view.skey.get() == self.registration_view.rskey.get():

                        data = (
                            self.registration_view.skey.get(),
                            self.registration_view.table.get(),
                        )

                        if not self.db_admin.comprobation_of_unique_skey(self.registration_view.skey.get()) and \
                                not self.db_admin.comprobation_of_unique_table(self.registration_view.table.get()):
                            
                            if user_creation(self):
                                self.db_admin.new_table(data)
                                self.registration_view.destroy()

                        else:
                            raise ErrorSkeyNotValid
                        
                    else:
                        raise ErrorSkeyNotEqual

                except ErrorSkeyNotEqual:
                    self.registration_view.error_messages("Error Skey", "Las skey no coinciden")
                except TableInExistance:
                    self.registration_view.error_messages("Error de Tabla", "La tabla ya esxiste")
                except ErrorSkeyNotValid:
                    self.registration_view.error_messages("Error de Skey", "La skey o tabla ya existe")

            else:
                try:
                    datos = (
                        self.registration_view.skey.get(),
                        self.registration_view.table.get()
                    )
                    self.db_admin.skey_comprobation(datos)

                    datos = (
                        self.registration_view.usuario.get(),
                        self.registration_view.passw.get(),
                        self.registration_view.table.get()
                    )

                    user_creation(self)
                    self.registration_view.destroy()
                    
                except ErrorSkeyNotValid:
                    self.registration_view.error_messages("Error Skey", "La skey no coincide")
        
        except AttributeError:
            self.registration_view.error_messages("Error de registro", "Los campos no pueden ser nulos")

    def alta(
            self
    ):
        """
        Se da de alta los datos que proporciona el ususario hacia
        la base de datos.
        """
        try:
            if fullmatch(r"[A-Z]{2}-\d{6}", self.view.valor_item_id.get()):
                fecha_hoy = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
                datos = [
                    self.view.valor_item_id.get(),
                    self.view.valor_nombre.get(),
                    self.view.valor_precio.get(),
                    self.view.valor_stock.get(),
                    self.view.valor_categoria.get(),
                    fecha_hoy
                ]

                self.model.insert_row(datos)
                self.__o_create.update(self.actual_user,
                                       self.view.valor_item_id.get(),
                                       self.tabla)
                self.refresh_table()
                self.limpiar()
            else:
                self.view.error("ERROR.ALTA.ITEMID")
        except IntegrityError:
            self.view.error("ERROR.ALTA.2ITEMID")
        except TclError:
            self.view.error("ERROR.ALTA.INVALIDVALUE")

    def baja(
            self
    ):
        """
        Se dan de baja los datos que el usuario seleccione de la base de datos.
        """
        try:
            iid = self.view.tabla_principal.item(self.view.tabla_principal.focus())["text"]
            itemid = self.model.leer_fila(iid)[0][1]
            self.model.delete_row(iid)
            self.__o_delete.update(self.actual_user,
                                   itemid,
                                   self.tabla)
            self.refresh_table()
        except OperationalError:
            self.view.error("ERROR.BAJA")

    def refresh_table(
            self
    ):
        """
        Se actualiza la tabla. Es una instancia interna para poder visualizar los
        cambios cadavez que se realizan.
        """
        self.view.tabla_principal.delete(*self.view.tabla_principal.get_children())

        datos = self.model.leer_tabla()

        for dato in datos:

            iid = dato[0]
            lista_aux = []
            for i in range(1, 7):
                lista_aux.append(dato[i])
            valores = tuple(lista_aux)

            self.view.tabla_principal.insert("", "end", text=iid, values=valores)
        
        self.view.combo_categoria.config(values=self.model.extract_categoria())

    def actualizar(
            self
    ):
        """
        Se actualizan los datos en la base de datos que el usuario haya modificado.
        """
        if self.view.estado_consulta.get():
            iid = self.view.tabla_principal.item(self.view.tabla_principal.focus())["text"]

            fecha_hoy = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
            datos = (
                self.view.valor_item_id.get(),
                self.view.valor_nombre.get(),
                self.view.valor_precio.get(),
                self.view.valor_stock.get(),
                self.view.valor_categoria.get(),
                fecha_hoy,
                iid
            )

            self.model.update(datos)
            self.__o_update.update(self.actual_user,
                                   self.view.valor_item_id.get(),
                                   self.tabla)
            self.refresh_table()
            self.limpiar()
        else:
            self.view.error("ERROR.ACTUALIZAR")

    def limpiar(
            self
    ):
        """
        Pone todos los valores de los campos de toma de datos en un valor de *default*.
        """
        self.view.valor_item_id.set("")
        self.view.valor_nombre.set("")
        self.view.valor_precio.set(0)
        self.view.valor_stock.set(0)
        self.view.valor_categoria.set("")
        self.view.estado_consulta.set(False)
    
    def consulta(
            self
    ):
        """
        Setea los valores de los campos de entrada segun el valor de la tabla seleccionado.
        """
        try:
            iid = self.view.tabla_principal.item(self.view.tabla_principal.focus())["text"]
            datos = self.model.leer_fila(iid)

            self.view.valor_item_id.set(datos[0][1])
            self.view.valor_nombre.set(datos[0][2])
            self.view.valor_precio.set(datos[0][3])
            self.view.valor_stock.set(datos[0][4])
            self.view.valor_categoria.set(datos[0][5])

            self.view.estado_consulta.set(True)
            self.__o_read.update(self.actual_user,
                                 self.view.valor_item_id.get(),
                                 self.tabla)
        except IndexError:
            self.view.error("ERROR.CONSULTA")

    def buscar(
            self
    ):
        """
        Actualiza la tabla segun los valores que coincidan con los ingresados en los
        campos de entrada.
        """
        datos = (
            self.view.valor_item_id.get(),
            self.view.valor_nombre.get(),
            self.view.valor_precio.get(),
            self.view.valor_stock.get(),
            self.view.valor_categoria.get()
        )
        
        if datos == ("", "", 0.0, 0, ""):
            self.refresh_table()
        else:
            self.view.tabla_principal.delete(*self.view.tabla_principal.get_children())

            datos = self.model.buscar(datos)

            for dato in datos:

                iid = dato[0]
                lista_aux = []
                for i in range(1, 7):
                    lista_aux.append(dato[i])
                valores = tuple(lista_aux)

                self.view.tabla_principal.insert("", "end", text=iid, values=valores)

    def genid(
            self
    ):
        """
        Proporciona un valor de *Item-ID* con un valor aleatoreo teniendo en cuenta el
        resto de valores ingresado por el usuario. 
        """
        try:
            lista_ids = self.model.get_ids()

            a = self.view.valor_categoria.get()[0].upper()
            b = self.view.valor_nombre.get()[0].upper()

            while True:
                c = str(randint(1, 100000)).zfill(6)
                new_id = f"{a}{b}-{c}"
                if new_id not in lista_ids:
                    break

            self.view.valor_item_id.set(new_id)
        except IndexError:
            self.view.error("ERROR.GENID")

    def exportar(
            self
    ):
        """
        Exporta la tabla principal a un formato *.xlsx*
        hacia alguna de las siguientes ubicaicones:

          * **Documentos**
          
          * **Escritorio**

          * **Ubicacion del programa**

        Este es el orden que intentara de manera predeterminada.
        """
        wb = Workbook()
        ws = wb.active
        ws.title = f"{self.model.tabla}"

        ws.append(["ID", "Item ID", "Nombre", "Precio", "Stock", "Categoria", "Fecha de modificaicon"])
        for i in self.model.leer_tabla():
            ws.append(i)

        fecha_hoy = datetime.now().strftime("%d.%m.%Y - %H h %M m %S s")

        nombre_archivo_excel = f"{self.model.tabla} - {fecha_hoy}.xlsx"

        directorios = [
            f"C:\\Users\\{getlogin()}\\Documents\\{nombre_archivo_excel}",
            f"C:\\Users\\{getlogin()}\\Desktop\\{nombre_archivo_excel}",
            nombre_archivo_excel
        ]

        for i in directorios:
            try:
                wb.save(i)
                self.view.aviso_exportacion(directorios.index(i))
                break
            except FileNotFoundError:
                pass

def init_app():
    Controlador()
    

if __name__ == "__main__":
    init_app()
