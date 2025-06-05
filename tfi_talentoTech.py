'''Gestion de información inicial sobre los productos de la empresa

REQUERIMIENTOS:
    1-  Ingreso de datos de productos: [NOMBRE, CATEGORIA, PRECIO(Sin centavos)]-> Almacenados en lista
    2 - Visualizacion de productos registrados: Mostrar TODOS los productos ingresados. Deben estar enumerados.
    3 - Busqueda de productos: Por nombre. Si encuentra nombre, mostrar info completa, sino, "NO SE ENCONTRARON RESULTADOS"
    4 - Eliminacion de productos: Eliminar producto por su posición (número en la lista)

CONDICIONES
    * LISTAS --> Para almacenar y gestionar datos
    * Bucles while y for según corresponda
    * Validar carga de usuario (datos vacios o incorrectos)
    * Condicionales para opciones del menú.
    * MENU debe tener las funcionalidades: AGREGAR PRODUCTOS, VISUALIZAR PRODUCTOS, BUSCAR PRODUCTOS, ELIMINAR PRODUCTOS (CRUD)
    * Sistema continúa funcionando hasta opción SALIR
'''
#Titulo del programa
print("\033[33m\nSistema de Gestión Básica De Productos\033[0m")

#Creo lista de productos
productos = []

#Inicio de MENÚ
while True:
    print("\033[32m\n--- Menú ---\033[0m")
    print("\033[32m1.\033[0m Agregar producto")
    print("\033[32m2.\033[0m Visualizar productos")
    print("\033[32m3.\033[0m Buscar producto")
    print("\033[32m4.\033[0m Eliminar producto")
    print("\033[32m5.\033[0m Salir")

    try:
        opcion = int(input("\033[34mSeleccione una opción del menú:\033[0m"))
    except ValueError:
        print("\033[31mDebe ingresar un número correspondiente al menú\033[0m")
        continue

    match opcion:
        case 1:
            print ("\nAGREGAR PRODUCTO")
            nombre = input("Nombre:").upper().strip()
            categoria = input("Categoria:").upper().strip()
            while True:
                try:
                    precio = int(input("Precio (sin centavos): "))  # Fuerza entrada como entero
                    if precio <= 0:
                        print("\033[31mEl precio debe ser mayor a 0.\033[0m")
                    else:
                        break
                except ValueError:
                    print("\033[31mError: Debe ingresar un número entero válido.\033[0m")
            

            productos.append([nombre,categoria,precio]) #TODO ACÁ DEBERÍA GUARDAR TAMBIEN EL LARGO DE LA LISTA PARA TENER EL IDX [len(productos)+1, nombre, apellido,...] PARA FACILITAR LA ELIMINACION POR INDICE

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
                    print("\033[31mError: Número fuera de rango. Ingrese un número de la lista.\033[0m")
    
            except ValueError:
                print("\033[31mError: Debe ingresar un número válido.\033[0m")

        case 5:
            print ("\033[33mSaliendo del sistema\033[0m")
            break
        case _:
            print ("\033[31mNúmero fuera de rango!\033[0m")
