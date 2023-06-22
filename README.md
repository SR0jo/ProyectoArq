# Proyecto de Arquitectura
## Integrantes
Lucas Nievas y Santiago Rojo

## Descripcion
Este programa esta diseñado para detectar pendrives, a la vez que puede crear, eliminar y mostrar archivos y carpetas mediante comandos

## Instalación

### Linux

Para ejecutar este programa en Linux, necesitas tener Python 3 instalado en tu sistema. También necesitas instalar la biblioteca `psutil` usando `pip`. Abre una terminal e introduce el siguiente comando:

```sh
pip install psutil
```

### Windows

Para ejecutar este programa en Windows, necesitas tener Python 3 instalado en tu sistema. También necesitas instalar la biblioteca `psutil` usando pip. Abre un símbolo del sistema e introduce el siguiente comando:

```sh
pip install psutil
```

## Como Usar

Para usar el programa, escribe en la consola los comandos que quieras ejecutar. Esta es la lista:
```sh
help: Muestra los comandos
close: cerrar programa
pens: lista de pendrives
open: pide la direccion a usar
create txt: crea un archivo de texto
create dir: crea una carpeta
back: quita la direccion actual
list: da una lista de los archivos y carpetas con su informacion
list all: da la lista de todos los archivos que hay incluyendo los que estan adentro de carpetas
delete: borra un archivo o carpeta
```
Ten en cuenta que la mayoria de comandos requieren que selecciones una direccion correspondiente a la de un pendrive con el comando `open`
