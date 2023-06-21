import time

import psutil
import os
import threading
import sys

def is_pendrive(disk):
    return 'removable' in str(disk)

def get_pendrives():
    disks = psutil.disk_partitions()
    pendrives = [disk.device for disk in disks if is_pendrive(disk)]
    return pendrives
debe_detenerse = False
direccion = ""
def detection():
    pendrives_tamanio = -1

    while not debe_detenerse:
        time.sleep(0.1)
        if pendrives_tamanio != len(get_pendrives()):
            print("ACTUALIZACION")
            if len(get_pendrives()) > 0:
                print("Hay pendrives conectados")
            if pendrives_tamanio > len(get_pendrives()):
                print("Se ha desconectado un pendrive")
                direccion = ""
            if pendrives_tamanio < len(get_pendrives()):
                print("Se ha conectado un pendrive")
            pendrives_tamanio = len(get_pendrives())

def comandos():
    global debe_detenerse
    pendrives = get_pendrives()
    global direccion
    while True:
        time.sleep(0.2)
        print("Escribe un comando")

        comand = input(direccion+" ")

        if comand == "close":
            debe_detenerse = True
            break
        elif comand == "help":
            print("close: cerrar programa")
            print("pens: lista de pendrives")
        elif comand == "pens":
            if pendrives:
                print("Pendrives conectados:", pendrives)
            else:
                print("No hay pendrives conectados")
        elif comand == "open":
            print("Escribe la direccion")
            direccion = input()

            if os.path.exists(direccion) == False:
                print("La direccion no existe")
                direccion = ""
        elif comand == "create txt":
            if direccion != "":
                print("Escribe el nombre")
                file_name = ""
                file_name = input()
                pendrive_path = direccion  # Reemplaza "E:\\" con la ruta de tu pendrive
                archi = open(direccion + "\\" + file_name + ".txt", "w")
                archi.close()
                file_path = os.path.join(pendrive_path, file_name+".txt")
                escribir = ""
                print("Escribir? S o cualquier tecla")
                if input(escribir) == "S":
                    contenido = input()
                    with open(file_path, "w") as f:
                        f.write(contenido)

                print(f"Archivo creado en {file_path}")
        elif comand == "back":
            direccion = ""
        elif comand == "list":
            if direccion != "":
                print("{:<10} {:<8} {:<9} {:<10} {:<10} {:<10}".format("Tamaño", "Lectura", "Escritura", "Ejecución", "Extensión", "Nombre"))
                with os.scandir(direccion) as entries:
                    for entry in entries:
                        if entry.is_file():
                            file_path = entry.path
                            size = os.path.getsize(file_path)
                            readable = os.access(file_path, os.R_OK)
                            writable = os.access(file_path, os.W_OK)
                            executable = os.access(file_path, os.X_OK)
                            extension = os.path.splitext(entry.name)[1]
                            print("{:<10} {:<8} {:<9} {:<10} {:<10} {}".format(size, readable, writable, executable, extension, entry.name))
                        elif entry.is_dir():
                            print("{:<10} {:<8} {:<9} {:<10} {:<10} {}".format("", "", "", "", "", entry.name))
        elif comand == "list all":
            if direccion != "":
                print("{:<10} {:<8} {:<9} {:<10} {:<10}".format("Tamaño", "Lectura", "Escritura", "Ejecución", "Extensión", "Nombre"))
                for root, dirs, files in os.walk(direccion):
                    print(f"Directorio: {root}")
                    for file in files:
                        file_path = os.path.join(root, file)
                        size = os.path.getsize(file_path)
                        readable = os.access(file_path, os.R_OK)
                        writable = os.access(file_path, os.W_OK)
                        executable = os.access(file_path, os.X_OK)
                        extension = os.path.splitext(file)[1]
                        print("{:<10} {:<8} {:<9} {:<10} {:<10} {}".format(size, readable, writable, executable, extension, file))

        else:
            print("Comando invalido")

mi_hilo = threading.Thread(target=detection)
mi_hilo2 = threading.Thread(target=comandos)

mi_hilo.start()
mi_hilo2.start()

mi_hilo2.join()
sys.exit()

