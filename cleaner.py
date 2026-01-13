import re

def clean_file(register):
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    try:
        if not register or not isinstance(register, str):
            return None
        email = register.strip().lower()
        if re.match(patron, email):
            return register
        else: 
            return
    except Exception as e:
        print(f"\n❌ Error crítico en archivo: {e}")