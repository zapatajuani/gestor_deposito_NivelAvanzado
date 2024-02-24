import socket
import sys
import os
import logging

dir_path = os.path.dirname(os.path.abspath(__file__))
main_path = dir_path[0:(len(dir_path)-7)]
sys.path.append(main_path)

ref = main_path + r'\log\LOG.log'

class Logger:
    logging.basicConfig(level=logging.INFO,
                        filename=ref,
                        filemode="a",
                        format="%(message)s")
    
    @classmethod
    def write(cls, msj):
        logging.info(msj)


class Servidor:
    def __init__(self):
        
        self.PORT = 65432
        self.SERVER = "127.0.0.1"
        self.ADDR = (self.SERVER, self.PORT)
        self.FORMAT = "utf-8"

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(self.ADDR)
        self.s.listen()

        self.loop_state = True

    def shutdown(self):
        self.loop_state = False
        self.s.close()

    def run_server(self):
        try:
            while self.loop_state:
                con, add = self.s.accept()

                if add[0] == self.SERVER:
                    while 1:
                        datos = con.recv(1024).decode(self.FORMAT)
                        if not datos:
                            break
                        
                        Logger.write(datos)

                con.close()
                
        except RuntimeError:
            pass
        except OSError:
            pass

if __name__ == "__main__":
    pass
