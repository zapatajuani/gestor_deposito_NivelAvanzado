"""
El modulo Modelo es el encargado de interactuar con la
base de datos, generar la conexion y las request que pida el
controlador.
"""
import sys
import os
from sqlite3 import connect, IntegrityError

dir_path = os.path.dirname(os.path.abspath(__file__))
main_path = dir_path[0:(len(dir_path)-4)]
sys.path.append(main_path)

from bin.custom_errors import ErrorSkeyNotValid, UserOrPassNotValid

ref = main_path + r"\src\db\main.db"

def db_con_noargs(f):
    def wraper(inst):
        con = connect(inst.db)
        cursor = con.cursor()
        rta = f(inst, con, cursor)
        con.close()
        return rta
    return wraper

def db_con_args(f):
    def wraper(inst, arg):
        con = connect(inst.db)
        cursor = con.cursor()
        rta = f(inst, con, cursor, arg)
        con.close()
        return rta
    return wraper

class DbModel:
    def __init__(self):
        self.con = connect(ref)
        self.cursor = self.con.cursor()
        self.db = ref

    @db_con_noargs
    def get_tables(
            self, con, cursor
    ):
        cursor.execute("SELECT tabla FROM tables_skey")

        tablas = []
        
        for i in cursor.fetchall():
            tablas.append(i[0])
        con.commit()

        return tablas
    
    @db_con_args
    def access(
            self, con, cursor, data_querry
    ):
        querry = "SELECT tabla FROM usuarios WHERE user = ? AND passw = ?"

        cursor.execute(querry, data_querry)

        tabla = cursor.fetchall()

        con.commit()

        if tabla:
            return tabla
        else:
            raise UserOrPassNotValid

    @db_con_args
    def skey_comprobation(
            self, con, cursor, data_querry
    ):
        query = "SELECT * FROM tables_skey WHERE skey = ? AND tabla = ?"

        cursor.execute(query, data_querry)

        tabla = cursor.fetchall()

        con.commit()

        if tabla:
            return True
        else:
            raise ErrorSkeyNotValid
        
    @db_con_args
    def add_new_user_to_table(
            self, con, cursor, data_querry
    ):
        try:
            querry = """INSERT INTO usuarios
                        (user, passw, tabla)
                        VALUES (?, ?, ?)"""

            cursor.execute(querry, data_querry)
            con.commit()
            return True
        except IntegrityError:
            return False
    
    @db_con_args
    def comprobation_of_unique_skey(
            self, con, cursor, skey
    ):
        querry = f"""SELECT EXISTS (
                    SELECT 1 FROM tables_skey
                    WHERE skey = '{skey}')"""

        cursor.execute(querry)

        con.commit()

        if cursor.fetchone()[0]:
            return True
        else:
            return False
        
    @db_con_args
    def comprobation_of_unique_table(
            self, con, cursor, tabla
    ):
        querry = f"""SELECT EXISTS (
                    SELECT 1 FROM tables_skey
                    WHERE tabla = '{tabla}')"""

        cursor.execute(querry)

        con.commit()

        if cursor.fetchone()[0]:
            return True
        else:
            return False

    @db_con_args
    def new_table(
            self, con, cursor, data_querry
    ):
        try:
            querry = """INSERT INTO tables_skey
                        (skey, tabla)
                        VALUES (?, ?)"""

            cursor.execute(querry, data_querry)
            con.commit()
            return True
        except IntegrityError:
            return False

class Model:
    """
    La clase Modelo se construye pasandole dos parametros, la ruta de la base
    de datos y el nombre de la tabla (este se puede crear o cargar si ya existe).
    Esta clase se llama desde el controlador, en el constructor de su clase, para que
    pueda ejecutar las instacias del modelo y asi interactuar con la base de datos.

    Args:
        mi_database (str): Ruta de acceso a la base de datos

        nombre_tabla (str): Nombre de la tabla a la cual acceder o crear
    """
    def __init__(self, nombre_tabla):
        """
        En el conructor de la clase generaremos la conexion con la base de datos y
        con la instancia _crear_tabla crearemos la tabla si es que esta no existe. Ademas
        asignaremos las variables de clase:
        
          * **self.con**: La conexion a la base de datos.

          * **self.cursor**: El cursor para actuar sobre la abse de datos.
          
          * **self.tabla**: El nombre de la tabla asignado a una variable de clase.
        """
        self.db = ref
        self.tabla = nombre_tabla

        self._crear_tabla()

    # Se crea la tabla
    @db_con_noargs
    def _crear_tabla(
            self, con, cursor
    ):
        """
        Metodo de instancia interno del modulo que se utiliza para crear la
        tabla en el caso de que esta no exista.
        """
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS '{self.tabla}' (
            id integer PRIMARY KEY,
            itemid text UNIQUE,
            nombre text,
            precio float,
            stock integer,
            categoria text,
            fecha text
            )"""
        )
        con.commit()

    # incerta una nueva fila en la tabal seleccionada
    @db_con_args
    def insert_row(
            self, con, cursor, data_querry
    ):
        """
        Inserta una fila completa en la tabla con los datos proporcionados.
        
        Args:
            data_querry (tuple): Tupla que contiene en orden los datos de cada fila de la tabla que se quieren ingresar.
        """

        querry = f"""INSERT INTO '{self.tabla}'
                (itemid, nombre, precio, stock, categoria, fecha)
                VALUES (?, ?, ?, ?, ?, ?)"""

        cursor.execute(querry, data_querry)
        con.commit()

    # elimina una fila en la tabla seleccionada y con el id que corresponda
    @db_con_args
    def delete_row(
            self, con, cursor, iid
    ):
        """
        Se elimina la fila indicada con el *iid* correspondiente.

        Args:
            iid (int): Valor clave de la fila que se desea eliminar. 
        """

        cursor.execute(f"DELETE FROM '{self.tabla}' WHERE id = {iid}")
        con.commit()

    # devuelve los datos de la tabla que coincidan con la tupla pasada
    @db_con_args
    def buscar(
            self, con, cursor, data_querry
    ):
        """
        Funcion que devuelve los valores de la tabla que coincidan con los elementos pasados
        como argumentos.

        Args:
            data_querry (tuple): Tupla que contiene en orden los datos de busqueda.

        Returns:
            Todos los datos que coincidan con los pasados en el *data_querry*
        """

        querry = f"""SELECT * FROM '{self.tabla}'
                     WHERE itemid = ? OR nombre = ? OR precio = ? OR stock = ? OR categoria = ?
                     ORDER BY fecha DESC"""

        cursor.execute(querry, data_querry)

        datos = cursor.fetchall()

        con.commit()

        return datos
    
    # lee todos los datos de la tabla seleccionada
    @db_con_noargs
    def leer_tabla(
            self, con, cursor
    ):
        """
        Selecciona todos los elementos de la tabla y los devuelve ordenados de manera descendente
        por la ultima fecha de modificacicon de cada uno. 
        """

        querry = f"""SELECT * FROM '{self.tabla}' ORDER BY fecha DESC"""

        cursor.execute(querry)

        datos = cursor.fetchall()

        con.commit()

        return datos

    # entrega los datos especificos de una fila por medio de su id
    @db_con_args
    def leer_fila(
            self, con, cursor, iid
    ):
        """
        Retorna los datos de la fila que coincida con el id proporcionado.

        Args:
            iid (int): Valor clave de la fila que se desea extraer los datos.

        Returns:
            Se devuelve una tupla con los datos de la fila solicitada 
        """

        querry = f"SELECT * FROM '{self.tabla}' WHERE id = ?"

        data_querry = (iid,)

        cursor.execute(querry, data_querry)

        datos = cursor.fetchall()

        con.commit()

        return datos

    # actualiza los datos de una cierta fila con los datos pasados
    @db_con_args
    def update(
            self, con, cursor, data_querry
    ):
        """
        Actualiza toda una fila de la tabla.

        Args:
            data_querry (tuple): Tupla que contiene los datos de la fila que se quiere modificar
        """

        querry = f"""UPDATE '{self.tabla}' SET
                itemid = ?,
                nombre = ?,
                precio = ?,
                stock = ?,
                categoria = ?,
                fecha = ?

                WHERE id = ?
                """

        cursor.execute(querry, data_querry)
        con.commit()

    # extraer array con elementos de la categoria
    @db_con_noargs
    def extract_categoria(
            self, con, cursor
    ):
        """
        Extrae de los elementos de la columna CATEGORIA sin repertir.

        Returns:
            Devuele una **lista** con las categorias que la tabla posee, sin repetir.
        """
        
        querry = f"SELECT categoria FROM '{self.tabla}'"

        cursor.execute(querry)

        datos = []

        for a in cursor.fetchall():
            if a[0] in datos:
                pass
            else:
                datos.append(a[0])

        con.commit()

        return datos

    # retorna en una lista los ids de la tabla
    @db_con_noargs
    def get_ids(
            self, con, cursor
    ):
        cursor.execute(f"SELECT itemid FROM '{self.tabla}'")

        lista_ids = []
        
        for i in cursor.fetchall():
            lista_ids.append(i[0])
        con.commit()

        return lista_ids

def _main():
    pass

if __name__ == "__main__":
    _main()
