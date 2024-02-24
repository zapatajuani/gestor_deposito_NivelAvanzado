import sys
import os

dir_path = os.path.dirname(os.path.abspath(__file__))
main_path = dir_path[0:(len(dir_path)-4)]
sys.path.append(main_path)

from datetime import datetime
from server.client import Cliente

class LogInObserver:
    def update(self, user):
        actual_time = datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
        Cliente.connection(f"{actual_time} | Se logeo el usuario {user}")

class LogOutObserver:
    def update(self, user):
        actual_time = datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
        Cliente.connection(f"{actual_time} | Se deslogeo el usuario {user}")

class CreateObserver:
    def update(self, user, item_id, table):
        actual_time = datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
        Cliente.connection(f"{actual_time} | El usuario {user} CREO el elemento {item_id} en la tabla {table}")

class DeleteObserver:
    def update(self, user, item_id, table):
        actual_time = datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
        Cliente.connection(f"{actual_time} | El usuario {user} ELIMINO el elemento {item_id} en la tabla {table}")

class UpdateObserver:
    def update(self, user, item_id, table):
        actual_time = datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
        Cliente.connection(f"{actual_time} | El usuario {user} CAMBIO el elemento {item_id} en la tabla {table}")

class ReadObserver:
    def update(self, user, item_id, table):
        actual_time = datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
        Cliente.connection(f"{actual_time} | El usuario {user} CONSULTO por el elemento {item_id} en la tabla {table}")

if __name__ == "__main__":
    pass
