#Santiago Bautista Salazar
#Emilio Rafael Puente Cardona
import subprocess
import csv
from openpyxl import Workbook
import os

def run_powershell_script(script_path):
    try:
        #Ejecuta el script de PowerShell
        result = subprocess.run(["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", script_path], capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Error al ejecutar el script: {result.stderr}")
        return "servicios.csv"
    except Exception as e:
        print(f"Ocurrió un error al ejecutar el script de PowerShell: {e}")
        return None

def csv_to_excel(csv_file, excel_file):
    try:
        #Crear el archivo de Excel
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Servicios"

        #Lee el archivo CSV y escribe en el archivo de Excel
        with open(csv_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                sheet.append(row)

        #Guardar el archivo de Excel
        workbook.save(excel_file)
        print(f"Los datos han sido exportados a {excel_file}.")
    except Exception as e:
        print(f"Ocurrió un error al procesar el archivo CSV o guardar el archivo Excel: {e}")

def main():
    powershell_script = "C:/Users/Emilio/Documents/Uni/Semestre 3/Porgra Ciberseguridad/Tarea 26/monitor_servicios.ps1"
    csv_file = run_powershell_script(powershell_script)
    
    if csv_file:
        excel_file = "servicios.xlsx"  #Nombre del archivo de Excel
        csv_to_excel(csv_file, excel_file)

        #Borra el archivo CSV
        if os.path.exists(csv_file):
            os.remove(csv_file)

if __name__ == "__main__":
    main()
