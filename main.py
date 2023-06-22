import time
import shutil
import psutil
import os
import threading
import sys


# Comprobar que la direccion pertenece a un pendrive
def comparar_primeras_dos_letras(string, array):
    for elemento in array:
        if string[:2] == elemento[:2]:
            return True
    return False


# Comprobar si el disco es un pendrive
def is_pendrive(disk):
    return 'removable' in str(disk)


# Obtener la lista de pendrive
def get_pendrives():
    disks = psutil.disk_partitions()
    _pendrives = [disk.device for disk in disks if is_pendrive(disk)]
    return _pendrives


debe_detenerse = False
direccion = ""
pendrives = get_pendrives()


# Detectar los cambios del pendrive (conectado o desconectado)
def detection():
    pendrives_tamanio = -1
    global pendrives
    while not debe_detenerse:
        time.sleep(0.1)
        if pendrives_tamanio != len(get_pendrives()):
            print("ACTUALIZACION")
            if len(get_pendrives()) > 0:
                pendrives = get_pendrives()
                print("Hay pendrives conectados")
            if pendrives_tamanio > len(get_pendrives()):
                pendrives = get_pendrives()
                print("Se ha desconectado un pendrive")
                direccion = ""
            if pendrives_tamanio < len(get_pendrives()) and pendrives_tamanio != -1:
                pendrives = get_pendrives()
                print("Se ha conectado un pendrive")
            pendrives_tamanio = len(get_pendrives())


# Lista de comandos
def comandos():
    global debe_detenerse
    global pendrives
    global direccion

    while True:
        pendrives = get_pendrives()
        time.sleep(0.2)
        print("Escribe un comando")
        comand = input(direccion+" ")
        if comand == "close":
            debe_detenerse = True
            break
        elif comand == "help":
            print("close: cerrar programa")
            print("pens: lista de pendrives")
            print("open: pide la direccion a usar")
            print("create txt: crea un archivo de texto")
            print("create dir: crea una carpeta")
            print("back: quita la direccion actual")
            print("list: da una lista de los archivos y carpetas con su informacion")
            print("list all: da la lista de todos los archivos que hay incluyendo los que estan adentro de carpetas")
            print("delete: borra un archivo o carpeta")
        elif comand == "pens":
            if pendrives:
                print("Pendrives conectados:")
                for pendrive in pendrives:
                    print(pendrive)
            else:
                print("No hay pendrives conectados.")
        elif comand == "open":
            print("Escribe la direccion.")
            direccion = input()
            comparar = comparar_primeras_dos_letras(direccion, get_pendrives())
            if not os.path.exists(direccion) or not comparar:
                print("La direccion no existe.")
                direccion = ""
        elif comand == "create txt":
            if direccion != "":
                print("Escribe el nombre")
                file_name = ""
                file_name = input()
                pendrive_path = direccion
                file_path = os.path.join(pendrive_path, file_name + ".txt")
                if os.path.exists(file_path):
                    print(f"El archivo {file_path} ya existe.")
                else:
                    archi = open(file_path, "w")
                    archi.close()

                    escribir = ""
                    print("Escribir? Ingrese 'S'")
                    if input(escribir) == "S":
                        contenido = input()
                        with open(file_path, "w") as f:
                            f.write(contenido)

                    print(f"Archivo creado en {file_path}")
            else:
                print("No se ha dado una direccion")
        elif comand == "create dir":
            if direccion != "":
                print("Nombre de la carpeta:")
                nombre_carpeta = input()
                direccion_completa = os.path.join(direccion, nombre_carpeta)
                if os.path.exists(direccion_completa):
                    print(f"La carpeta {direccion_completa} ya existe.")
                else:
                    os.makedirs(direccion_completa)
                    print(f"Se ha creado la carpeta.")
            else:
                print("No se ha dado una direccion")
        elif comand == "back":
            direccion = ""
        elif comand == "list":
            if direccion != "":
                print("{:^10} {:^8} {:^9} {:^10} {:^10} {:^10}".format("Tamaño", "Lectura", "Escritura", "Ejecución", "Extensión", "Nombre"))
                with os.scandir(direccion) as entries:
                    for entry in entries:
                        if entry.is_file():
                            file_path = entry.path
                            size = os.path.getsize(file_path)
                            readable = os.access(file_path, os.R_OK)
                            writable = os.access(file_path, os.W_OK)
                            executable = os.access(file_path, os.X_OK)
                            extension = os.path.splitext(entry.name)[1]
                            print("{:^10} {:^8} {:^9} {:^10} {:^10} {}".format(size, readable, writable, executable, extension, entry.name))
                        elif entry.is_dir():
                            print("{:^10} {:^8} {:^9} {:^10} {:^10} {}".format("", "", "", "", "", entry.name))
            else:
                print("No se ha dado una direccion")
        elif comand == "list all":
            if direccion != "":
                print("{:^10} {:^8} {:^9} {:^10} {:^10} {:^10}".format("Tamaño", "Lectura", "Escritura", "Ejecución", "Extensión", "Nombre"))
                for root, dirs, files in os.walk(direccion):
                    print(f"Directorio: {root}")
                    for file in files:
                        file_path = os.path.join(root, file)
                        size = os.path.getsize(file_path)
                        readable = os.access(file_path, os.R_OK)
                        writable = os.access(file_path, os.W_OK)
                        executable = os.access(file_path, os.X_OK)
                        extension = os.path.splitext(file)[1]
                        print("{:^10} {:^8} {:^9} {:^10} {:^10} {}".format(size, readable, writable, executable, extension, file))
            else:
                print("No se ha dado una direccion")
        elif comand == "delete":
            if direccion != "":
                print("Nombre del archivo/carpeta:")
                nombre = input()
                direccion_completa = os.path.join(direccion, nombre)
                if os.path.exists(direccion_completa):
                    if os.path.isfile(direccion_completa):
                        os.remove(direccion_completa)
                        print(f"Se ha eliminado el archivo {direccion_completa}.")
                    elif os.path.isdir(direccion_completa):
                        shutil.rmtree(direccion_completa)
                        print(f"Se ha eliminado la carpeta {direccion_completa}.")
                else:
                    print(f"No se encontró {direccion_completa}.")
            else:
                print("No se ha dado una direccion")

        else:
            print("Comando invalido")


# Hilos del sistema
mi_hilo = threading.Thread(target=detection)
mi_hilo2 = threading.Thread(target=comandos)

mi_hilo.start()
mi_hilo2.start()

mi_hilo2.join()
sys.exit()
