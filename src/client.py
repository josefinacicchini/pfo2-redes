import requests

BASE_URL = "http://127.0.0.1:5000"
session = requests.Session()  # mantiene cookies de sesión
logged = False

def registro():
    username = input("Ingrese usuario: ")
    password = input("Ingrese contraseña: ")
    data = {"username": username, "password": password}
    resp = session.post(f"{BASE_URL}/registro", json=data)
    print(resp.json())

def login():
    global logged    
    username = input("Ingrese usuario: ")
    password = input("Ingrese contraseña: ")
    data = {"username": username, "password": password}
    resp = session.post(f"{BASE_URL}/login", json=data)
    resultado = resp.json()
    print(resultado)
    if resp.status_code == 200:
        logged = True

def ver_tareas():
    if not logged:
        print("Primero debes iniciar sesión")
        return
    resp = session.get(f"{BASE_URL}/tareas")
    if resp.status_code == 200:
        print(resp.text)
    else:
        print(resp.json())

def logout():
    global logged
    resp = session.post(f"{BASE_URL}/logout")
    print(resp.json())
    logged = False

def menu():
    while True:
        print("\n--- MENÚ ---")
        print("1. Registro")
        print("2. Login")
        print("3. Ver tareas")
        print("4. Logout")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registro()
        elif opcion == "2":
            login()
        elif opcion == "3":
            ver_tareas()
        elif opcion == "4":
            logout()
        elif opcion == "5":
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()
