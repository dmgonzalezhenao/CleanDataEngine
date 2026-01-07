📂 CleanData Engine v1.0
CleanData Engine es una herramienta de automatización desarrollada en Python diseñada para la limpieza y validación masiva de bases de datos en formato CSV. El sistema procesa archivos de entrada, valida correos electrónicos mediante expresiones regulares (Regex) y genera archivos depurados de forma eficiente.

🚀 Características Principales
Validación con Regex: Implementa filtros avanzados para asegurar que solo los correos con formato legítimo sean procesados.

Procesamiento Inteligente (DictReader): El motor localiza la columna de "email" automáticamente, sin importar el orden de las columnas en el archivo original.

Barra de Carga en Tiempo Real: Interfaz visual en consola que muestra el progreso real basado en el volumen de datos de cada archivo.

Manejo de Errores Robusto: Gestión de excepciones para prevenir cierres inesperados si un archivo está bloqueado o corrupto.

Arquitectura Escalable: Estructura modular preparada para integrarse con bases de datos SQL en el futuro.

🛠️ Tecnologías Utilizadas
Lenguaje: Python 3.x

Librerías Estándar: os, re, csv, time (No requiere instalaciones externas).

📦 Estructura del Proyecto
Plaintext

CleanDataEngine/
├── input/          # Carpeta para los archivos CSV sucios
├── output/         # Carpeta donde se guardan los archivos limpios
├── main.py         # Código fuente principal
├── .gitignore      # Filtro para evitar subir datos sensibles a Git
└── README.md       # Documentación del proyecto
🔧 Cómo usarlo
Clona este repositorio o descarga el archivo main.py.

Asegúrate de tener una carpeta llamada input con tus archivos .csv.

Ejecuta el script:

Bash

python main.py
Sigue las instrucciones del menú interactivo.

Nota: Hay un archivo de prueba llamado sample.csv para que pruebe por usted
mismo el programa.

⚠️ Seguridad y Buenas Prácticas
Este proyecto incluye protecciones contra:

Path Traversal: Uso de os.path.join para manejo seguro de rutas en Windows/Linux.

Memory Efficiency: El procesamiento se realiza línea por línea para evitar el consumo excesivo de RAM en archivos grandes.

Data Integrity: El software nunca modifica el archivo original; siempre genera una copia limpia en la carpeta de salida.

## 🛠️ Mejoras Futuras (Roadmap)

Este proyecto está en constante evolución. Las próximas etapas de desarrollo incluyen:

* **Integración con Bases de Datos (Semana 7):** Migrar el almacenamiento de archivos CSV a una base de datos local **SQLite** para permitir consultas complejas y persistencia de datos profesional.
* **Interfaz Web (Flask):** Desarrollar un dashboard básico con **Flask** para que los usuarios puedan cargar sus archivos desde un navegador en lugar de la consola.
* **Reporte de Auditoría PDF:** Generar automáticamente un reporte visual (PDF) que resuma las estadísticas de limpieza (registros exitosos vs. descartados).
* **Soporte Multiformato:** Ampliar la capacidad del motor para procesar archivos JSON y Excel (.xlsx).

## 👤 Autor

Desarrollado con dedicación por Daniel Mitchell González Henao.

* **LinkedIn:** www.linkedin.com/in/daniel-gonzález-551b22305
* **Email:** dmgh20212022@gmail.com

---
*Este proyecto fue creado como parte de mi proceso de aprendizaje en el desarrollo Backend, aplicando conceptos de CS50 y lógica avanzada de Python.*