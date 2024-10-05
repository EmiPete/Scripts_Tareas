#Santiago Bautsita Salazar
#Emilio Rafael Puente Cardona

import pyautogui
import subprocess
import datetime
import os

# Función para capturar la pantalla
def capturar_pantalla():
    try:
        # Obtener la fecha y hora actual
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        
        # Definir el nombre del archivo con fecha y hora
        nombre_imagen = f"captura_{timestamp}.png"
        
        # Capturar la imagen de la pantalla
        screenshot = pyautogui.screenshot()
        
        # Guardar la imagen en la carpeta actual
        screenshot.save(nombre_imagen)
        
        print(f"Captura de pantalla guardada como: {nombre_imagen}")
    except Exception as e:
        print(f"Error al capturar la pantalla: {e}")

# Función para registrar los procesos en ejecución
def registrar_procesos():
    try:
        # Obtener la fecha y hora actual
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        
        # Definir el nombre del archivo de registro con fecha y hora
        nombre_registro = f"procesos_{timestamp}.txt"
        
        # Ejecutar el comando de listados de procesos (Windows: 'tasklist')
        result = subprocess.run(["tasklist"], capture_output=True, text=True, shell=True)
        
        # Guardar la salida en un archivo de texto
        with open(nombre_registro, "w") as archivo:
            archivo.write(f"Registro de procesos - {now}\n\n")
            archivo.write(result.stdout)
        
        print(f"Registro de procesos guardado como: {nombre_registro}")
    except Exception as e:
        print(f"Error al registrar los procesos: {e}")

# Función principal que integra ambas funcionalidades
def main():
    try:
        capturar_pantalla()
        registrar_procesos()
    except Exception as e:
        print(f"Se produjo un error en la ejecución del script: {e}")

if __name__ == "__main__":
    main()
