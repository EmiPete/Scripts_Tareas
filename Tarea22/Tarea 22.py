import requests
import json
import logging
import getpass
import six
import argparse

# Verificación si está siendo ejecutado en Python 3
try:
    if not six.PY3:
        raise EnvironmentError("Este script requiere Python 3 para ejecutarse.")
except EnvironmentError as e:
    print(f"Error: {e}")
    exit(1)  #Sale del script si no se está ejecutando en Python 3

logging.basicConfig(filename='hibp.log',
                    format="%(asctime)s %(message)s",
                    datefmt="%m/%d/%Y %I:%M:%S %p",
                    level=logging.INFO)

#Mensajes de ayuda y guarda el correo en args
parser = argparse.ArgumentParser(description="Consulta la API de Have I Been Pwned para verificar correos filtrados")
parser.add_argument("email", help="El correo electrónico que deseas investigar")
args = parser.parse_args()

#Solicita la API key de forma segura usando el módulo getpass
key = getpass.getpass("Ingrese su API key de Have I Been Pwned: ")

#Configuración de los headers para la solicitud
headers = {
    'content-type': 'application/json',
    'api-version': '3',
    'User-Agent': 'python',
    'hibp-api-key': key
}

#Url
url = f'https://haveibeenpwned.com/api/v3/breachedaccount/{args.email}?truncateResponse=false'

try:
    #Solicitar información a la API
    r = requests.get(url, headers=headers)
    r.raise_for_status()  #En caso de fallar el request, hace una excepción

    data = r.json()
    encontrados = len(data)

    if encontrados > 0:
        print(f"Los sitios en los que se ha filtrado el correo {args.email} son:")
        report_filename = f'reporte_{args.email}.txt'
        
        #Abre el archivo para poder escribir el reporte
        with open(report_filename, 'w') as report_file:
            for filtracion in data:
                nombre = filtracion.get("Name", "N/A")
                dominio = filtracion.get("Domain", "N/A")
                fecha = filtracion.get("BreachDate", "N/A")
                descripcion = filtracion.get("Description", "N/A")
                
                print(f"Nombre: {nombre}")
                print(f"Dominio: {dominio}")
                print(f"Fecha de filtración: {fecha}")
                print(f"Descripción: {descripcion}\n")
                
                #Escribe en el archivo de reporte
                report_file.write(f"Nombre: {nombre}\n")
                report_file.write(f"Dominio: {dominio}\n")
                report_file.write(f"Fecha de filtración: {fecha}\n")
                report_file.write(f"Descripción: {descripcion}\n")
                report_file.write("\n")
        
        msg = f"{args.email} - Filtraciones encontradas: {encontrados}"
        logging.info(msg)
        print(f"Reporte guardado en {report_filename}")
    else:
        print(f"El correo {args.email} no ha sido filtrado.")
        logging.info(f"{args.email} - No se encontraron filtraciones.")
    
except requests.exceptions.HTTPError as http_err:
    msg = f"Error HTTP: {http_err}"
    print(msg)
    logging.error(msg)

except requests.exceptions.RequestException as req_err:
    msg = f"Error en la solicitud: {req_err}"
    print(msg)
    logging.error(msg)

except Exception as err:
    msg = f"Error inesperado: {err}"
    print(msg)
    logging.error(msg)

else:
    print(f"Solicitud completada con éxito para {args.email}.")

finally:
    print("Proceso finalizado.")
    logging.info("El proceso ha finalizado.")
