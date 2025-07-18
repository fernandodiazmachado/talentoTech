import sqlite3

from colorama import Fore, init
init()#inicio módulo colorama

#Titulo del programa
print(Fore.RED + "Sistema de Gestión Básica De Productos" + Fore.RESET)

#Creo la db si no existe
conexion = sqlite3.connect("inventario.db")

cursor = conexion.cursor()

#Creo la tabla productos (si no existe)
cursor.execute('''
CREATE TABLE IF NOT EXISTS productos(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               nombre TEXT NOT NULL,
               descripcion TEXT,
               cantidad INTEGER NOT NULL,
               precio REAL NOT NULL,
               categoria TEXT)
''')

conexion.commit()

#Creo lista de productos
productos = []

#Inicio de MENÚ
def menu():
    while True:
        print(Fore.GREEN + "\n--- Menú ---" + Fore.RESET)
        print("1. Registrar producto")
        print("2. Ver productos")
        print("3. Actualizar productos")
        print("4. Eliminar producto")
        print("5. Buscar producto")
        print("6. Reporte de stock")
        print("7. Salir")

        # Validacion de ingreso de opcion
        try:
            opcion = int(input(Fore.BLUE + "Seleccione una opción del menú:" + Fore.RESET))
            if opcion < 1 or opcion > 7:
                print(Fore.RED + "Error: El número debe estar entre 1 y 7" + Fore.RESET)
                continue
        except ValueError:
            print(Fore.RED + "Error: Debe ingresar un número correspondiente al menú" + Fore.RESET)
            continue
        
        # inicio match con opcion ingresada
        match opcion:
            case 1:
                registrar_producto()
            case 2:
                print ("\nVISUALIZAR PRODUCTOS")
                print(f"{'No.':<5} | {'NOMBRE':<20} | {'CATEGORÍA':<15} | {'PRECIO':>10}")
                print("-" * 60)
                for i in range(len(productos)):
                    print(f"\033[36m{i+1:<5}\033[0m | {productos[i][0]:<20} | {productos[i][1]:<15} | ${productos[i][2]:>10}")
            case 3:
                print ("\nBUSCAR PRODUCTO")
                producto_buscado = input("ingrese el nombre del producto a buscar:").upper().strip()
                resultados = []

                for producto in productos:
                    if producto_buscado == producto[0]: #BUSQUEDA EXACTA --- SI QUIERO BUSQUEDA PARCIAL, USAR "in"
                        resultados.append(producto)

                if resultados:
                    print("\nResultado de busqueda:")
                    print(f"{'No.':<5} | {'NOMBRE':<20} | {'CATEGORÍA':<15} | {'PRECIO':>10}")
                    print("-" * 60)
                    for producto in resultados:
                        idx = productos.index(producto)+1
                        print(f"{idx:<5} | {producto[0]:<20} | {producto[1]:<15} | ${producto[2]:>10}")
                    
                else:
                    print("\033[31mNO SE ENCONTRARON RESULTADOS\033[0m")

            case 4:
                print ("\nELIMINAR PRODUCTO")

                try:
                    idx_eliminar = int(input("\nIngrese el N° de producto a eliminar: ")) - 1  # Resto 1 para convertir a índice interno
                    
                    if 0 <= idx_eliminar < len(productos):
                        producto_eliminado = productos.pop(idx_eliminar)
                        print(f"\033[32mProducto eliminado: {producto_eliminado[0]}\033[0m")
                    else:
                        print("\033[31mEr5ror: Número fuera de rango. Ingrese un número de la lista.\033[0m")
        
                except ValueError:
                    print("\033[31mError: Debe ingresar un número válido.\033[0m")

            case 5:
                print ("\033[33mSaliendo del sistema\033[0m")
                break
            case _:
                print (Fore.RED + "Error de selección en Menú!" + Fore.RESET) #Algún error no tenido en cuenta


def registrar_producto():
    print(f"{Fore.CYAN}\n--- AGREGAR PRODUCTO ---{Fore.RESET} ({Fore.RED}*{Fore.RESET} significa campo obligatorio)")
    nombre = ingreso_texto("Nombre",True)
    descripcion = ingreso_texto("Descripcion")
    cantidad = ingreso_numero("Cantidad",True,int,True)
    precio = ingreso_numero("Precio",True,positivo=True)
    categoria = ingreso_texto("Categoria")  

    try:
        cursor.execute('''INSERT INTO productos (nombre,descripcion,cantidad,precio,categoria) 
                    VALUES (?,?,?,?,?)''',
                    (nombre,descripcion,cantidad,precio,categoria))
        conexion.commit()
        print(f"\n{Fore.GREEN}Producto registrado correctamente{Fore.RESET}")
    except:
        print("Error al insertar producto")

    productos.append([nombre,categoria,precio]) #TODO ACÁ DEBERÍA GUARDAR TAMBIEN EL LARGO DE LA LISTA PARA TENER EL IDX [len(productos)+1, nombre, apellido,...] PARA FACILITAR LA ELIMINACION POR INDICE


def ingreso_texto(parametro, obligatorio=False):
    """
    Solicita texto al usuario con validación opcional de campo obligatorio
    
    Args:
        parametro (str): Texto que se muestra como prompt
        obligatorio (bool): Si True, valida que no se ingrese texto vacío
    
    Returns:
        str: Texto ingresado por el usuario en mayúsculas y sin espacios extras
    """
    while True:
        # Construir el prompt visual
        prompt = f"{Fore.RED + '*' + Fore.RESET if obligatorio else ''}{parametro}: "
        texto = input(prompt).upper().strip()
        
        # Validar solo si es obligatorio
        if obligatorio and not texto:
            print(Fore.RED + "Error: Este campo es obligatorio" + Fore.RESET)
        else:
            return texto

def ingreso_numero(parametro, obligatorio=True, tipo_dato=float, positivo=True):
    """
    Solicita un número al usuario con validación configurable
    
    Args:
        parametro (str): Texto descriptivo del campo
        obligatorio (bool): Si True, muestra asterisco y valida vacíos
        tipo_dato (type): float o int - tipo de número a retornar
        positivo (bool): Si True, valida que el número sea > 0
    
    Returns:
        float/int: Número validado según parámetros
    """
    while True:
        try:
            # Construir el prompt visual
            prompt = f"{Fore.RED + '*' + Fore.RESET if obligatorio else ''}{parametro}: "
            entrada = input(prompt).strip()
            
            if not entrada and not obligatorio:
                return None  # Permitir vacío si no es obligatorio
            
            # Convertir al tipo especificado
            valor = tipo_dato(entrada)
            
            # Validar positividad si está habilitado
            if positivo and valor <= 0:
                print(Fore.RED + "Error: Debe ingresar un valor positivo" + Fore.RESET)
            else:
                return valor
                
        except ValueError:
            tipo_esperado = "entero" if tipo_dato == int else "numérico"
            print(Fore.RED + f"Error: Debe ingresar un valor {tipo_esperado} válido" + Fore.RESET)

if __name__ == "__main__":
    menu()
    conexion.close()