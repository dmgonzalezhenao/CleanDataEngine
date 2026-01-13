"""
CleanData Engine v1.0
Autor: Daniel Mitchel González Henao
Descripción: Herramienta de automatización para limpieza de CSV con validación Regex.
"""
import re
import csv
import sqlite3
from pathlib import Path

def main():
    inicializar_entorno()
    while True:
        archivos = [f for f in os.listdir("input") if f.endswith('.csv')]
        
        if not archivos:
            print("❌ No hay archivos .csv en 'input/'. Agrega archivos y presiona Enter.")
            input()
            continue # Vuelve a buscar archivos

        opcion = mostrar_menu(len(archivos))
        
        if opcion == "1":
            procesar_carpeta(archivos)
            print("\n✨ Proceso terminado.")
            input("Presiona Enter para volver al menú...")
        elif opcion == "2":
            print("👋 Saliendo..."); break
        else:
            print("✖️ Opción no válida.")

def inicializar_entorno():
    for carpeta in ["input", "output"]:
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
            print(f"📁 Carpeta '{carpeta}' creada.")

def limpiar_archivo(ruta_entrada, ruta_salida):
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    #Diccionario de contadores para analizar el porcentaje de pérdidas de datos

    estadisticas = {
        "totales": 0,
        "buenos": 0,
        "malos": 0,
    }
    try:
        with open(ruta_entrada, 'r', encoding='utf-8', errors='ignore') as f:
            total_lineas = sum(1 for linea in f)
        
        if total_lineas == 0: return

        # 2. Procesar con DictReader (para que no importe el orden de las columnas)
        with open(ruta_entrada, 'r', encoding='utf-8', errors='ignore') as f_in, \
             open(ruta_salida, 'w', encoding='utf-8', newline='') as f_out:
            
            lector = csv.DictReader(f_in)
            escritor = csv.DictWriter(f_out, fieldnames=lector.fieldnames)
            escritor.writeheader()

            print("█", end="", flush=True)
            
            longitud_barra = 20
            procesadas = 0

            for fila in lector:
                #Contamos cada línea analizada
                estadisticas["totales"] += 1
                # Buscamos la columna que contenga 'email' (sin importar mayúsculas)
                columna_email = next((k for k in fila if 'email' in k.lower()), None)
                
                if columna_email:
                    email_sucio = fila[columna_email].strip()
                    
                    if re.match(patron, email_sucio):
                        escritor.writerow(fila)
                        estadisticas["buenos"] += 1
                    else:
                        # Si no cumple el patron, es un registro malo
                        estadisticas["malos"] += 1

                # Actualizar barra
                procesadas += 1
                progreso = int((procesadas / total_lineas) * (longitud_barra - 1))
                pasado = int(((procesadas - 1) / total_lineas) * (longitud_barra - 1))
                if progreso > pasado:
                    print("█", end="", flush=True)

            #Imprimir las estadísticas de los datos totales analizados, los válidos, los descartados
            #y la efectividad
            total = estadisticas["totales"] if estadisticas["totales"] > 0 else 1
            print(f"\n\n--- REPORTE FINAL ---")
            print(f"✅ Válidos: {estadisticas['buenos']}")
            print(f"❌ Descartados: {estadisticas['malos']}")
            print(f"📊 Efectividad: {(estadisticas['buenos'] / total) * 100:.1f}%")
    except Exception as e:
        print(f"\n❌ Error crítico en archivo: {e}")

def procesar_carpeta(archivos):
    print(f"\n🚀 Procesando {len(archivos)} archivos...\n")
    for nombre in archivos:
        ruta_in = os.path.join("input", nombre)
        ruta_out = os.path.join("output", f"limpio_{nombre}")
        
        print(f"📄 {nombre}: ", end="")
        limpiar_archivo(ruta_in, ruta_out)
        print(" ✅")

def mostrar_menu(cantidad):
    print("\n" + "="*30 + "\n   CLEANDATA ENGINE v1.0\n" + "="*30)
    print(f"📂 Archivos en input: {cantidad}\n1. Iniciar\n2. Salir")
    return input("👉 Selecciona: ").strip()

if __name__ == "__main__":
    main()
