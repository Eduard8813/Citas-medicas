import sqlite3

conn_main = sqlite3.connect('medical_services.db')
cursor_main = conn_main.cursor()

conn_reports = sqlite3.connect('reported_issues.db')
cursor_reports = conn_reports.cursor()

cursor_main.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

cursor_main.execute('''
CREATE TABLE IF NOT EXISTS medical_centers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    contact TEXT NOT NULL
)
''')

cursor_main.execute('''
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    request_type TEXT NOT NULL,
    details TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
''')

cursor_reports.execute('''
CREATE TABLE IF NOT EXISTS reported_issues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    problem_description TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
''')

conn_main.commit()
conn_reports.commit()

AUTH_KEY = "mi_secreta_clave"

def add_user():
    print("=== Registro de Usuario ===")
    auth_key = input("Ingrese la clave de autenticación: ")
    
    if auth_key != AUTH_KEY:
        print("Error: Clave incorrecta, no puedes agregar usuarios.")
        return

    username = input("Ingrese su nombre de usuario: ")
    password = input("Ingrese su contraseña: ")

    try:
        cursor_main.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn_main.commit()
        print("Usuario agregado exitosamente.")
    except sqlite3.IntegrityError:
        print("Error: El nombre de usuario ya existe.")

def make_request():
    print("=== Solicitud de Servicio Médico ===")
    user_id = int(input("Ingrese su ID de usuario: "))
    request_type = input("Tipo de solicitud (Ej: Cita médica, Emergencia): ")
    details = input("Detalles adicionales: ")
    problem_desc = input("Descripción del problema: ")

    if request_type.lower() == "cita médica" and details:
        cursor_main.execute("INSERT INTO requests (user_id, request_type, details) VALUES (?, ?, ?)", (user_id, request_type, details))
        conn_main.commit()
        print("Solicitud de cita médica registrada exitosamente.")
    elif request_type.lower() == "emergencia":
        print("¡Se ha registrado una emergencia! Se notificará a los servicios médicos.")
        cursor_main.execute("INSERT INTO requests (user_id, request_type, details) VALUES (?, ?, ?)", (user_id, request_type, "Emergencia médica"))
        conn_main.commit()
    else:
        print("Tipo de solicitud no válida.")
        return

    if problem_desc:
        cursor_reports.execute("INSERT INTO reported_issues (user_id, problem_description) VALUES (?, ?)", (user_id, problem_desc))
        conn_reports.commit()
        print("El problema ha sido reportado en la base de datos de incidencias.")

def get_requests():
    user_id = int(input("Ingrese su ID de usuario para ver sus solicitudes: "))
    cursor_main.execute("SELECT * FROM requests WHERE user_id = ?", (user_id,))
    requests = cursor_main.fetchall()

    if requests:
        print("\n=== Solicitudes Registradas ===")
        for req in requests:
            print(f"ID: {req[0]}, Tipo: {req[2]}, Detalles: {req[3]}")
    else:
        print("No hay solicitudes registradas.")

def get_reported_issues():
    user_id = int(input("Ingrese su ID de usuario para ver problemas reportados: "))
    cursor_reports.execute("SELECT * FROM reported_issues WHERE user_id = ?", (user_id,))
    issues = cursor_reports.fetchall()

    if issues:
        print("\n=== Problemas Reportados ===")
        for issue in issues:
            print(f"ID: {issue[0]}, Descripción: {issue[2]}")
    else:
        print("No hay problemas reportados.")

print("\n=== Bienvenido al Sistema de Servicios Médicos ===")
while True:
    print("\nOpciones:")
    print("1. Agregar usuario")
    print("2. Realizar solicitud médica y reportar problema")
    print("3. Ver solicitudes registradas")
    print("4. Ver problemas reportados")
    print("5. Salir")

    option = input("Seleccione una opción: ")

    if option == "1":
        add_user()
    elif option == "2":
        make_request()
    elif option == "3":
        get_requests()
    elif option == "4":
        get_reported_issues()
    elif option == "5":
        print("Saliendo del sistema. Hasta luego.")
        break
    else:
        print("Opción no válida, intente de nuevo.")

conn_main.close()
conn_reports.close()
