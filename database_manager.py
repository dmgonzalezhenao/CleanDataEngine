import sqlite3
def create_tables(db_name = "clean_data.db"):

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clean_emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            source_file TEXT,
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dirty_emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            raw_data TEXT,
            reason TEXT,
            source_file TEXT,
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    #Tabla específica por si ocurre un error durante la limpieza de datos para no hacer
    #todo desde cero y para que no hayan procesos repetidos

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS processing_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT UNIQUE,
            total_records INTEGER,
            status TEXT,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def save_to_db(connection, data_to_save, original_data, source_file):
    cursor = connection.cursor()

    if data_to_save:
        query = "INSERT INTO clean_emails (email, source_file) VALUES (?, ?)"
        cursor.execute(query, (data_to_save, source_file))
                       
    else:
        query = "INSERT INTO dirty_emails (raw_data, reason, source_file) VALUES (?, ?, ?)"
        cursor.execute(query, (original_data, "Invalid Format", source_file))
    connection.commit()

def update_file_log(connection, file_name, total_rows, status):
    """
    Actualiza el estado del archivo. 
    Usa 'INSERT OR REPLACE' para evitar errores de duplicidad.
    """
    cursor = connection.cursor()
    query = """
        INSERT OR REPLACE INTO processing_log (file_name, total_records, status) 
        VALUES (?, ?, ?)
    """
    try:
        cursor.execute(query, (file_name, total_rows, status))
        connection.commit()
    except Exception as e:
        print(f"❌ Error interno en la base de datos: {e}")

def get_file_status(connection, file_name):
    """
    Consulta la base de datos para saber en qué estado quedó un archivo.
    Devuelve el estado (str) o None si el archivo es nuevo.
    """
    cursor = connection.cursor()
    query = "SELECT status FROM processing_log WHERE file_name = ?"
    
    cursor.execute(query, (file_name,))
    result = cursor.fetchone() # Trae la primera fila que coincida
    
    # Si existe el registro, devuelve el texto (ej: 'Completado'), si no, devuelve None
    return result[0] if result else None

# Ver un reporte de todos los archivos ya escaneados
def view_report(conexion):
    cursor = conexion.cursor()
    # Se leen los registros en la tabla processing_log para ver los procesos de cada archivo en el momento
    cursor.execute("SELECT file_name, total_records, status, completed_at FROM processing_log")
    filas = cursor.fetchall()

    # Si no hay reportes
    if not filas:
        print("\n📭 No hay historial todavía.")
        return
    # Diseño títulos
    print("\n" + "="*70)
    print(f"{'ARCHIVO':<25} | {'FILAS':<8} | {'ESTADO'}")
    print("-" * 70)

    # Imprimir cada registro de la tabla
    for f in filas:
        name, total, status, timestamp = f
        # f[0]=name, f[1]=total, f[2]=status
        if len(name) > 22:
            display_name = name[:22] + ".."
        else:
            display_name = name
        print(f"{display_name:<25} | {total:<8} | {status} ")
    print("="*70)