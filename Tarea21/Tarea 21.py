import requests
import json
import logging
import getpass

#Configuración de los logs
logging.basicConfig(filename='hibp.log',
                    format="%(asctime)s %(message)s",
                    datefmt="%m/%d/%Y %I:%M:%S %p",
                    level=logging.INFO)
#Solicita la API key de forma segura usnado el módulo getpass
key = getpass.getpass("Ingrese su API key de Have I Been Pwned: ")
headers = {
    'content-type': 'application/json',
    'api-version': '3',
    'User-Agent': 'python',
    'hibp-api-key': key
}
#Correo a investigar
email = input("Ingrese el correo a investigar: ")
#Url
url = f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}?truncateResponse=false'
try:
    # Solicitar información a la API
    r = requests.get(url, headers=headers)
    r.raise_for_status()  #En caso de fallar el request hace una excepción

    data = r.json()
    encontrados = len(data)

    if encontrados > 0:
        print(f"Los sitios en los que se ha filtrado el correo {email} son:")
        report_filename = f'reporte_{email}.txt'
        
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
                
                # Escribir en el archivo de reporte
                report_file.write(f"Nombre: {nombre}\n")
                report_file.write(f"Dominio: {dominio}\n")
                report_file.write(f"Fecha de filtración: {fecha}\n")
                report_file.write(f"Descripción: {descripcion}\n")
                report_file.write("\n")
        
        msg = f"{email} - Filtraciones encontradas: {encontrados}"
        logging.info(msg)
        print(f"Reporte guardado en {report_filename}")
    else:
        print(f"El correo {email} no ha sido filtrado.")
        logging.info(f"{email} - No se encontraron filtraciones.")
    
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
    print(f"Solicitud completada con éxito para {email}.")

finally:
    print("Proceso finalizado.")
    logging.info("El proceso ha finalizado.")
