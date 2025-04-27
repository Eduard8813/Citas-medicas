import sqlite3

conn_main = sqlite3.connect('servicios_medicos.db')
cursor_main = conn_main.cursor()

conn_reports = sqlite3.connect('reporte_inusuales.db')
cursor_reports = conn_reports.cursor()

cursor_main.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

cursor_main.execute('''
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    specialty TEXT NOT NULL,
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

AUTH_KEY = "12345"

def authenticate():
    auth_key = input("Ingrese la clave de autenticación para acceder: ")
    return auth_key == AUTH_KEY

def add_user():
    print("=== Registro de Usuario ===")
    if not authenticate():
        print("Error: Clave incorrecta, acceso denegado.")
        return

    username = input("Ingrese su nombre de usuario: ")
    password = input("Ingrese su contraseña: ")

    try:
        cursor_main.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn_main.commit()
        print("Usuario agregado exitosamente.")
    except sqlite3.IntegrityError:
        print("Error: El nombre de usuario ya existe.")

def get_users():
    print("=== Consulta de Usuarios ===")
    if not authenticate():
        print("Error: Clave incorrecta, acceso denegado.")
        return

    cursor_main.execute("SELECT * FROM users")
    users = cursor_main.fetchall()

    if users:
        print("\n=== Usuarios Registrados ===")
        for user in users:
            print(f"ID: {user[0]}, Nombre de usuario: {user[1]}")
    else:
        print("No hay usuarios registrados.")

def add_doctor():
    print("=== Ingrese la clave de autenticacion para acceder ===")
    if not authenticate():
        print("Error: Clave incorrecta, acceso denegado.")
        return
    
    print("=== Registro de Médico ===")
    name = input("Ingrese el nombre del médico: ")
    specialty = input("Ingrese la especialidad: ")
    contact = input("Ingrese el contacto: ")

    cursor_main.execute("INSERT INTO doctors (name, specialty, contact) VALUES (?, ?, ?)", (name, specialty, contact))
    conn_main.commit()
    print("Médico agregado exitosamente.")

def get_doctors():
    print("\n=== Médicos Registrados ===")
    cursor_main.execute("SELECT * FROM doctors")
    doctors = cursor_main.fetchall()

    if doctors:
        for doc in doctors:
            print(f"ID: {doc[0]}, Nombre: {doc[1]}, Especialidad: {doc[2]}, Contacto: {doc[3]}")
    else:
        print("No hay médicos registrados.")

def get_requests():
    print("=== Consulta de Solicitudes Médicas ===")
    if not authenticate():
        print("Error: Clave incorrecta, acceso denegado.")
        return

    user_id = int(input("Ingrese su ID de usuario: "))
    cursor_main.execute("SELECT * FROM requests WHERE user_id = ?", (user_id,))
    requests = cursor_main.fetchall()

    if requests:
        print("\n=== Solicitudes Registradas ===")
        for req in requests:
            print(f"ID: {req[0]}, Tipo: {req[2]}, Detalles: {req[3]}")
    else:
        print("No hay solicitudes registradas.")

def get_reported_issues():
    print("=== Consulta de Problemas Reportados ===")
    if not authenticate():
        print("Error: Clave incorrecta, acceso denegado.")
        return

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
    print("2. Ver usuarios registrados (requiere autenticación)")
    print("3. Agregar médico")
    print("4. Ver médicos registrados (NO requiere autenticación)")
    print("5. Ver solicitudes médicas (requiere autenticación)")
    print("6. Ver problemas reportados (requiere autenticación)")
    print("7. Salir")

    option = input("Seleccione una opción: ")

    if option == "1":
        add_user()
    elif option == "2":
        get_users()
    elif option == "3":
        add_doctor()
    elif option == "4":
        get_doctors()
    elif option == "5":
        get_requests()
    elif option == "6":
        get_reported_issues()
    elif option == "7":
        print("Saliendo del sistema. Hasta luego.")
        break
    else:
        print("Opción no válida, intente de nuevo.")

conn_main.close()
conn_reports.close()
