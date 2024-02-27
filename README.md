# rest API EY WEB SCRAPPING 

Esta API esta desarollada en Flask y se encarga de buscar en esta pagina https://sanctionssearch.ofac.treas.gov de acuerdo un query parameter de la misma api para encontrar entidades con un background posiblemente sospechoso.

## Table of Contents

- [Instalacion](#Instalacion)
- [Uso](#uso)


## Instalacion

Es necesario tener python instalado para poder correr esta API.
Instala el entorno virtual :pip install virtualenv
EN CMD...(recomendado)
Crea un entorno virtual : python -m venv venv
Activa el entorno virtual: venv\Scripts\activate.bat o venv\Scripts\activate (fijarse en el directorio del venv)
UNA VEZ ACTIVADO EL VENV...
Instalar los requerimientos usando el comando 'pip install -r requirements.txt'
El código por default corre en el puerto 5000 y solo tiene permitido el acceso de CORS por el puerto 3000. Si deseas cambiar estos accesos dirigete a las lineas 82 y 19 de codigo para configurar tanto el puerto donde va a correr como el puerto permitido para el acceso a la API.
Ahora puedes correr la aplicación con tan solo usar el comando Ctrl+Alt+N asegurandote que el codigo se corra en el entorno virtual. Para esto en la linea de comandos deberá aparecer algo asi : (venv) C:\TuDirectorio\proyecto >

## Uso
Recomiendo usarlo con la colección de POSTMAN que se encuentra en la carpeta de manera que solo se corran los querys seleccionados. 
Se gestionan dos errores , que el query sea nulo y que no el query no de ningun resultado en la página. Estos dos casos más un caso exitoso son los revisados en la colección.
