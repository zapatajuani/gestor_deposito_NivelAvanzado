# Gestor de Depósito

Este proyecto es la entrega final del Nivel Intermedio de la Diplomatura en Python de la Universidad Tecnológica Nacional (UTN). La aplicación 'Gestor de Depósito' se desarrolló siguiendo el paradigma MVC (Modelo-Vista-Controlador) y la Programación Orientada a Objetos (POO).

## Módulos

El código se divide en tres módulos principales:

1. **Modelo**: Define la estructura de los datos.
2. **Vista**: Se encarga de la interacción con el usuario.
3. **Controlador**: Coordina el Modelo y la Vista.

Cada módulo, diseñado bajo el paradigma POO, cumple con sus respectivas funciones dentro de la aplicación. Para más detalles sobre el funcionamiento de la aplicación, por favor consulte la documentación completa.

# Preparación

Antes de ejecutar la aplicación, es necesario instalar las dependencias requeridas. Esto se puede hacer utilizando el siguiente comando:

`pip install -r requirements.txt`

# Ejecución

Una vez instaladas las dependencias, el programa puede ser ejecutado a través de dos métodos.

Para hacerlo de manera local, simplemente se ejecuta alguno de los siguientes archivos:

`python controlador.py`

o

`python __main__.py`

Si se quiere ejecutar el programa de manera externa al fichero donde se descargaron los
archivos, ejecute el siguiente código:

`python <RUTA_DEL_FICHERO>`

Por favor, consulte la [documentación](https://zapatajuani.github.io/gestor_de_deposito_docs/) completa para obtener más detalles sobre la ejecución y el uso de la aplicación 'Gestor de Depósito'.

# Cambios para la Entrega Final del Nivel Avanzado

Para la entrega del nivel avanzado de la diplomatura, implemente una serie de cambios en el programa.

El funcionamiento del programa principal sigue siendo el mismo, por lo que la guia anterior sigue valiendo para eso.

Como novedad se implemento un sistema de registro, con ususario y contraseña. Tambien se habilito la creacion de nuevas tablas y la adicion de nuevos usuarios a las tablas ya existentes por el medio de una "Security Key".

Por el lado del codigo:

1. Se implementaron decoradores para el mejor manejo de la base de datos

2. Uso de observadores para un registro de LOG, en el cual se cargan los datos de los usuarios y sus actividades

3. Implementacion de un Cliente/Servidor para el manejo de esta ultima parte, los observadores toman el rol de Cliente y el Servidor se encarga de la parte del Log