class ErrorPassNotEqual(Exception):
    def __init__(self, mensaje="Valor de pass no coincide"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class ErrorSkeyNotEqual(Exception):
    def __init__(self, mensaje="Valor de skey no coincide"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class ErrorSkeyNotValid(Exception):
    def __init__(self, mensaje="Valor de skey no valido"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class UserOrPassNotValid(Exception):
    def __init__(self, mensaje="Valor de pass o usuario erroneo"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class UserInExistance(Exception):
    def __init__(self, mensaje="Nombre de usuario en uso"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class TableInExistance(Exception):
    def __init__(self, mensaje="Tabla en existencia"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)
