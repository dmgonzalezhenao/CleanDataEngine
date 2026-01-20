"""
CleanData Engine v1.1
Autor: Daniel Mitchel González Henao
Descripción: Herramienta de automatización para limpieza de CSV con validación Regex.
"""

import csv
import sqlite3
from pathlib import Path
from cleaner import clean_file
from database_manager import create_tables, save_to_db, update_file_log, get_file_status, view_report

DB_NAME = "clean_data.db"

def main():
    # Crea las carpetas input y output y la base de datos
    inicializar_entorno()
    create_tables()

    # Conexión a la base de datos del programa, para que sólo se abra cuando se inicia el programa 
    # y solo se cierre cuando se termine de ejecutar el programa
    conn = sqlite3.connect("clean_data.db")
    # Mostramos el menú para que el usuario decida qué hacer


    while True:
        opcion = mostrar_menu()

        if opcion == "1":
            print("\n🚀 Iniciando procesamiento...")

            # Definir la lista de archivos en el input
            input_dir = Path("input")
            files = list(input_dir.glob("*.csv"))

            # Verificamos si no hay archivos antes de hacer cualquier proceso
            if not files:
                print("📭 No se encontraron archivos CSV en la carpeta 'input'.")
                print("Agrega archivos CSV y vuelve a intentarlo.\n")
            else:
                # Recorrer archivo por archivo para procesar y limpiar cada uno
                for route_file in files:

                    # Preguntamos a la base de datos si el archivo ya fue procesado o si se quedó a medio camino
                    estado = get_file_status(conn, route_file.name)

                    if estado == "Completado":
                        print(f"⏭️  Saltando {route_file.name} (Ya procesado)")
                        continue

                    # Definimos la salida
                    output_dir = Path("output")
                    output_file = output_dir / f"clean_{route_file.name}"
                    
                    # Llamamos a la función procesar para insertar los datos en la base de datos y en el csv
                    procesar_archivo(route_file, output_file, conn)
                print("🏁 ¡Todo el lote ha sido procesado!")

        elif opcion == "2":
            print("\n📊 Generando reporte de procesamiento...")
            view_report(conn)  # Llamamos a la función de lectura

        elif opcion == "3":
            print("Saliendo...")
            conn.close()
            break


def inicializar_entorno():
    for dir in ["input", "output"]:
        # Crea ambas carpetas
        route = Path(dir)
        # Comprueba si existen o no
        route.mkdir(parents=True, exist_ok=True)

def procesar_archivo(input_route, output_route, connection):
    # Llevamos registro de las líneas ya procesadas, en caso de que falle el programa a medio proceso
    procesadas = 0

    try:
        # Empezamos con el proceso: se actualiza el estado del archivo para llevar registro
        # de cuantas filas fueron limpiadas
        update_file_log(connection, input_route.name, 0, "En Proceso")

        # Se abren las dos rutas de archivos
        with open(input_route, 'r', encoding='utf-8', errors='ignore') as f_in, \
            open(output_route, 'w', encoding='utf-8', newline='') as f_out:
            
            # Se guardan las filas de entrada en un diccionario
            lector = csv.DictReader(f_in)
            # Se crea la variable para escribir en el diccinario y se crea el header automáticamente
            escritor = csv.DictWriter(f_out, fieldnames=lector.fieldnames)
            escritor.writeheader()

            for fila in lector:

                email_original = fila.get('email', '') # Cambia 'email' por el nombre de tu columna

                # Limpiar por fila
                email_limpio = clean_file(email_original)

                # Guardar en DB 
                save_to_db(connection, email_limpio, email_original, input_route.name)
            
                # Escribir en el nuevo f_out los archivos distinguiendo si son validos o no
                if email_limpio:
                    fila['email'] = email_limpio
                else:
                    fila['email'] = f"⚠️ INVALIDO ({email_original})"
                escritor.writerow(fila)
                procesadas += 1
                
                # Feedback visual de progreso
                if procesadas % 100 == 0:
                    print("█", end="", flush=True)

        # SI el bucle terminó sin errores, se actualiza a completado
        update_file_log(connection, input_route.name, procesadas, "Completado")
        print(f"\n ✅ {procesadas} líneas.")

    except Exception as e:
        # Si algo sale mal, marcamos el error y cuántas llegó a hacer
        mensaje_error = f"Error en línea {procesadas + 1}: {str(e)[:50]}"
        update_file_log(connection, input_route.name, procesadas, mensaje_error)
        print(f" ❌ Falló: {mensaje_error}")

def mostrar_menu():
    print("\n--- 📧 CleanData Engine v1.1 ---")
    print("1. Procesar archivos en carpeta /input")
    print("2. Ver reporte de procesamiento (Log)")
    print("3. Salir")
    return input("Selecciona una opción: ")

if __name__ == "__main__":
    main()
