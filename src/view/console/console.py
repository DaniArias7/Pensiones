import sys
sys.path.append('C:/Users/ACER/Pensiones')
from src.model.calculator import CalculadoraPensional
from src.model.user import Usuario
from src.controller.app_controller import ControladorPensiones

def format_number_with_dots(number):
    """Formatea el número agregando puntos para facilitar la lectura"""
    return "{:,.2f}".format(number)

def get_int_input(prompt):
    """Obtiene un valor entero válido del usuario"""
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Error: Ingrese un número entero válido.")

def get_str_input(prompt):
    """Obtiene un valor entero válido del usuario"""
    while True:
        try:
            value = str(input(prompt))
            return value
        except ValueError:
            print("Error: Ingrese una opción valida.")

def get_float_input(prompt):
    """Obtiene un valor flotante válido del usuario"""
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Error: Ingrese un número válido.")

def main():
    controlador_pensiones = ControladorPensiones()
    controlador_pensiones.CrearTablas()
    calculadora_pensional = CalculadoraPensional()

    while True:
        print("\nMenú principal:")
        print("1. Registrar nuevo usuario")
        print("2. Modificar usuario existente")
        print("3. Eliminar usuario")
        print("4. Listar usuarios")
        print("5. Calcular pensión")
        print("6. Salir")

        opcion = get_int_input("Ingrese una opción: ")

        if opcion == 1:
            # Registrar nuevo usuario
            nombre = input("Ingrese el nombre: ")
            edad = get_int_input("Ingrese la edad: ")
            estado_civil = get_str_input("Ingrese el estado civil (soltero/casado)")

            usuario = Usuario(nombre, edad, estado_civil)
            controlador_pensiones.InsertarUsuario(usuario)
            print("Usuario registrado correctamente.")

        elif opcion == 2:
            # Modificar usuario existente
            usuarios = controlador_pensiones.ObtenerUsuarios()
            if not usuarios:
                print("No hay usuarios registrados.")
            else:
                print("Usuarios registrados:")
                for usuario in usuarios:
                    print(f"ID: {usuario.id}, Nombre: {usuario.name}, Edad: {usuario.age}")

                id_usuario = get_int_input("Ingrese el ID del usuario a modificar: ")
                usuario_modificar = next((u for u in usuarios if u.id == id_usuario), None)

                if usuario_modificar:
                    nombre = input(f"Ingrese el nuevo nombre (actual: {usuario_modificar.name}): ") or usuario_modificar.name
                    edad = get_int_input(f"Ingrese la nueva edad (actual: {usuario_modificar.age}): ") or usuario_modificar.age

                    usuario_modificar.name = nombre
                    usuario_modificar.age = edad

                    controlador_pensiones.ModificarUsuario(usuario_modificar)
                    print("Usuario modificado correctamente.")
                else:
                    print("No se encontró el usuario.")

        elif opcion == 3:
            # Eliminar usuario
            usuarios = controlador_pensiones.ObtenerUsuarios()
            if not usuarios:
                print("No hay usuarios registrados.")
            else:
                print("Usuarios registrados:")
                for usuario in usuarios:
                    print(f"ID: {usuario.id}, Nombre: {usuario.name}, Edad: {usuario.age}")

                id_usuario = get_int_input("Ingrese el ID del usuario a eliminar: ")
                usuario_eliminar = next((u for u in usuarios if u.id == id_usuario), None)

                if usuario_eliminar:
                    controlador_pensiones.EliminarUsuario(usuario_eliminar.id)
                    print("Usuario eliminado correctamente.")
                else:
                    print("No se encontró el usuario.")

        elif opcion == 4:
            # Listar usuarios
            usuarios = controlador_pensiones.ObtenerUsuarios()
            if not usuarios:
                print("No hay usuarios registrados.")
            else:
                print("Usuarios registrados:")
                for usuario in usuarios:
                    print(f"ID: {usuario.id}, Nombre: {usuario.name}, Edad: {usuario.age}")

        elif opcion == 5:
            # Calcular pensión
            usuarios = controlador_pensiones.ObtenerUsuarios()
            if not usuarios:
                print("No hay usuarios registrados. Registre un usuario primero.")
            else:
                print("Usuarios registrados:")
                for usuario in usuarios:
                    print(f"ID: {usuario.id}, Nombre: {usuario.name}, Edad: {usuario.age}")

                id_usuario = get_int_input("Ingrese el ID del usuario: ")
                usuario = next((u for u in usuarios if u.id == id_usuario), None)

                if usuario:
                    salario = get_float_input("Ingrese el salario mensual: ")
                    semanas_laboradas = get_int_input("Ingrese las semanas laboradas: ")
                    rentabilidad_fondo = get_float_input("Ingrese la rentabilidad del fondo (0 a 1): ")
                    tasa_administracion = get_float_input("Ingrese la tasa de administración (0 a 1): ")
                    sexo = input("Ingrese el sexo (masculino/femenino): ").lower()
                    estado_civil = input("Ingrese el estado civil (casado/soltero): ").lower()
                    esperanza_vida = get_int_input("Ingrese la esperanza de vida esperada: ")

                try:
                    ahorro_pensional, _ = calculadora_pensional.calculo_ahorro_pensional(usuario.age, salario, semanas_laboradas, rentabilidad_fondo, tasa_administracion)
                    pension, _ = calculadora_pensional.calculo_pension(usuario.age, ahorro_pensional, sexo, estado_civil, esperanza_vida)

                    print(f"El ahorro pensional esperado es: {format_number_with_dots(ahorro_pensional)}")
                    print(f"La pensión esperada es: {format_number_with_dots(pension)}")

                    # Agregar nueva pensión
                    controlador_pensiones.InsertarPension(usuario.id, ahorro_pensional, pension)
                    print("Pensión registrada correctamente.")
                except Exception as e:
                    print(f"Error al calcular la pensión: {type(e).__name__}: {e}")


        elif opcion == 6:
            # Salir
            break

        else:
            print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    main()
