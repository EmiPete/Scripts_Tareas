#Emilio Rafael Puente Cardona
#Santiago Bautista Salazar
import subprocess
import re

#Define los puertos estándar
PUERTOS_ESTANDAR = {22, 25, 80, 465, 587, 8080}

#Función para ejecutar el script de Bash
def ejecutar_script_bash(script_path):
    try:
        #Ejecuta el script de Bash usando subprocess.run
        resultado = subprocess.run(["bash", script_path], capture_output=True, text=True)
        #Verifica si el script se ejecutó correctamente
        resultado.check_returncode()
        
        return resultado.stdout  #Retorna la salida estándar del script
        
    except subprocess.CalledProcessError as e:
        print(f"Error en la ejecución del script de Bash: {e}")
        return None

#Función para analizar las conexiones y encontrar las sospechosas
def analizar_conexiones(conexiones):
    conexiones_sospechosas = []
    #Expresión regular para extraer el puerto de la salida de netstat
    regex_puerto = re.compile(r':(\d+)')  #Encuentra los puertos numéricos

    for linea in conexiones.splitlines():
        #Busca todos los puertos en la línea
        puertos_encontrados = regex_puerto.findall(linea)
        
        if puertos_encontrados:
            #Comprueba si alguno de los puertos no es estándar
            for puerto in puertos_encontrados:
                if int(puerto) not in PUERTOS_ESTANDAR:
                    conexiones_sospechosas.append(linea)
                    break  # Si ya es sospechosa, no sigue analizando la línea
                
    return conexiones_sospechosas

#Función para guardar el reporte en un archivo
def generar_reporte(conexiones_sospechosas, archivo_salida):
    with open(archivo_salida, "w") as f:
        if conexiones_sospechosas:
            f.write("Conexiones sospechosas encontradas:\n")
            for conexion in conexiones_sospechosas:
                f.write(conexion + "\n")
        else:
            f.write("No se encontraron conexiones sospechosas.\n")
    print(f"Reporte generado en {archivo_salida}")

def main():
    #Ejecuta el script de Bash y capturar la salida
    script_bash = "./monitor_conexiones.sh"
    salida_conexiones = ejecutar_script_bash(script_bash)

    if salida_conexiones:
        #Analiza las conexiones para detectar las sospechosas
        conexiones_sospechosas = analizar_conexiones(salida_conexiones)
        
        #Genera el reporte de conexiones sospechosas
        archivo_reporte = "reporte_conexiones_sospechosas.txt"
        generar_reporte(conexiones_sospechosas, archivo_reporte)
    else:
        print("No se pudo obtener la salida del script de Bash.")

if __name__ == "__main__":
    main()
