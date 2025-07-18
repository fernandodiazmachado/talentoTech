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
                ver_productos()
            case 3:
                actualizar_productos()       
            case 4:
                eliminar_producto()
            case 5:
                buscar_producto()
            case 6:
                control_stock()
            case 7:
                print (f"{Fore.BLUE}Saliendo del sistema{Fore.RESET}")
                break
            case _:
                print (Fore.RED + "Error: Error en selección en Menú!" + Fore.RESET) #Algún error no tenido en cuenta

def obtener_campos():
    return {
        1: {"nombre":"Nombre","tipo":str,"obligatorio":True},
        2: {"nombre":"Descripcion","tipo":str,"obligatorio":False},
        3: {"nombre":"Cantidad","tipo":int,"obligatorio":True},
        4: {"nombre":"Precio","tipo":float,"obligatorio":True},
        5: {"nombre":"Categoria","tipo":str,"obligatorio":False}
    }

def imprimir_tabla(productos):
    # Cabecera de tabla ajustada
    print(f"{Fore.CYAN}"
          f"{'ID':<5} "
          f"{'Nombre':<20} "
          f"{'Descripcion':<30} "
          f"{'Cantidad':>8} "
          f"{'Precio':>10} "
          f"{'Categoría':<20} "
          f"{Fore.RESET}")
    print("-" * 88)  # Línea separadora

    for producto in productos:
        # Limitar la descripción a 25 caracteres para evitar desbordamiento
        descripcion = (producto[2][:25] + '...') if len(producto[2]) > 25 else producto[2]
        
        print(
            f"{producto[0]:<5} "          # ID
            f"{producto[1]:<20} "         # Nombre
            f"{descripcion:<30} "         # Descripción (recortada si es muy larga)
            f"{producto[3]:>8} "          # Cantidad
            f"{Fore.GREEN}${producto[4]:>9.2f}{Fore.RESET}"  # Precio
            f" {producto[5]:<20} "         # Categoría
        )

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

def ver_productos():
    print (f"\n {Fore.GREEN}VISUALIZAR PRODUCTOS{Fore.RESET}")
    cursor.execute('''
                    SELECT * FROM productos
                    ''')
    productos = cursor.fetchall()

    # Verificar si hay productos antes de mostrar
    if not productos:
        print(f"{Fore.YELLOW}No hay productos registrados.{Fore.RESET}")
        return
    
    imprimir_tabla(productos)

def actualizar_productos():
    campos = obtener_campos()
    ver_productos()
    id_producto = int(input(f"{Fore.GREEN}Ingrese el ID del producto a actualizar:{Fore.RESET}")) #TODO FALTA VALIDAR ID_VALIDO
    campo = menu_campos(campos)

    match campo["nombre"]:
        case "Nombre":
            nuevo_valor = ingreso_texto("Nombre",True)
        case "Descripcion":
            nuevo_valor = ingreso_texto("Descripcion")
        case "Cantidad":
            nuevo_valor = ingreso_numero("Cantidad",True,int,True)
        case "Precio":
            nuevo_valor = ingreso_numero("Precio",True,positivo=True)
        case "Categoria":
            nuevo_valor = ingreso_texto("Categoria")
    
    cursor.execute(f'''
                    UPDATE productos SET {campo["nombre"]} = ? WHERE id = ?
                   ''',(nuevo_valor,id_producto))

    conexion.commit()
    print(f"{campo['nombre']} actualizado correctamente")

def menu_campos(campos):
    """
    Muestra menú de campos y retorna el campo seleccionado con toda su configuración
    
    Args:
        campos (dict): Diccionario con la estructura {num: {config_campo}}
        
    Returns:
        dict: Diccionario con la configuración completa del campo seleccionado
    """
    while True:
        # Menú dinámico con indicador de campos obligatorios
        print(f"\n{Fore.CYAN}Seleccione campo a modificar:{Fore.RESET}")
        for num, config in campos.items():
            obligatorio = Fore.RED + "*" + Fore.RESET if config["obligatorio"] else ""
            print(f"{num}. {config['nombre']} {obligatorio}")

        # Validación de entrada
        try:
            opcion = int(input(Fore.BLUE + "\nOpción: " + Fore.RESET))
            if opcion in campos:
                return campos[opcion]  # Retorna toda la configuración del campo
            print(Fore.RED + f"Error: Debe ser entre 1 y {len(campos)}" + Fore.RESET)
        except ValueError:
            print(Fore.RED + "Error: Ingrese un número válido" + Fore.RESET)

def eliminar_producto():
    print (f"\n{Fore.RED}ELIMINAR PRODUCTO{Fore.RESET}")
    ver_productos()
    try:
        id_producto = int(input(f"{Fore.RED}Ingrese el ID del producto a Eliminar:{Fore.RESET}")) #TODO FALTA VALIDAR ID_VALIDO
        
        # Verificar si el ID existe
        cursor.execute("SELECT id FROM productos WHERE id = ?", (id_producto,))
        if not cursor.fetchone():
            print(Fore.YELLOW + f"Error: No existe un producto con ID {id_producto}" + Fore.RESET)
            return None
        # Confirmar eliminación
        print(f"\n{Fore.RED}¡ATENCIÓN!{Fore.RESET}")
        print(f"Está por eliminar el producto ID: {Fore.RED}{id_producto}{Fore.RESET}")
        confirmacion = input(f"{Fore.RED}¿Está seguro? (S/N): {Fore.RESET}").upper()
        
        if confirmacion == 'S':
            cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
            conexion.commit()
    except ValueError:
        print(f"{Fore.RED}Error: Debe ingresar un número válido.{Fore.RESET}")

def control_stock():
    print("Ingrese el limite CANTIDAD a consultar")
    limite = ingreso_numero("Limite",True,int,True)
    cursor.execute('''
                    SELECT * FROM productos WHERE cantidad < ?
                   ''',(limite,))
    productos = cursor.fetchall()
    if productos:
        print("\nProductos con bajo stock:")
        imprimir_tabla(productos)
    else:
        print(f"{Fore.GREEN}Todos los productos tienen suficiente Stock{Fore.RESET}")

def buscar_producto():
    print (f"{Fore.GREEN}\nBUSCAR PRODUCTO{Fore.RESET}")

    ver_productos()
    try:
        id_producto = int(input(f"{Fore.RED}Ingrese el ID del producto a Buscar:{Fore.RESET}")) #TODO FALTA VALIDAR ID_VALIDO
        
        # Verificar si el ID existe
        cursor.execute("SELECT id FROM productos WHERE id = ?", (id_producto,))
        if not cursor.fetchone():
            print(Fore.YELLOW + f"Error: No existe un producto con ID {id_producto}" + Fore.RESET)
            return None
        cursor.execute("SELECT * FROM productos WHERE id = ?",(id_producto,))
        resultados = cursor.fetchall()

        if resultados:
            imprimir_tabla(resultados)
        else:
            print("No se encontraron productos")
    except ValueError:
        print("Error: Debe ingresar un numero valido")

   

if __name__ == "__main__":
    menu()
    conexion.close()