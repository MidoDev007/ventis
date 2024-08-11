import csv
from recomendaciones import recomendar_productos
from tabulate import tabulate

print(
"""
BIENVENIDO/A! °˖✧◝(⁰▿⁰)◜✧˖° 

░▒▓█▓▒░░▒▓█▓▒░ ░▒▓████████▓▒░ ░▒▓███████▓▒░  ░▒▓████████▓▒░ ░▒▓█▓▒░  ░▒▓███████▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░    ░▒▓█▓▒░     ░▒▓█▓▒░ ░▒▓█▓▒░        
 ░▒▓█▓▒▒▓█▓▒░  ░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░    ░▒▓█▓▒░     ░▒▓█▓▒░ ░▒▓█▓▒░        
 ░▒▓█▓▒▒▓█▓▒░  ░▒▓██████▓▒░   ░▒▓█▓▒░░▒▓█▓▒░    ░▒▓█▓▒░     ░▒▓█▓▒░  ░▒▓██████▓▒░  
  ░▒▓█▓▓█▓▒░   ░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░    ░▒▓█▓▒░     ░▒▓█▓▒░        ░▒▓█▓▒░ 
  ░▒▓█▓▓█▓▒░   ░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░    ░▒▓█▓▒░     ░▒▓█▓▒░        ░▒▓█▓▒░ 
   ░▒▓██▓▒░    ░▒▓████████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░    ░▒▓█▓▒░     ░▒▓█▓▒░ ░▒▓███████▓▒░  
                                                                                   
"""
)

name = input("Por favor, diganos su nombre ^w^: ").lower().strip()
id_client = -1
all_id_client = []
all_clients = []
found = False

print("Por favor, espere un momento :O!")


#BUSCA EL NOMBRE DEL CLIENTE
with open('data/clients.csv', mode="r") as file:
    clientes = csv.reader(file)

    for i in list(clientes)[1:]:
        if name == i[1]:
            all_id_client = [int(i[0])]
            found = True
            break
        else:
            all_id_client.append(int(i[0]))
            all_clients.append(i[1])


if not found:
    print("Usuario no registrado. Lo añadiremos a nuestra base de datos uwu")
    with open('data/clients.csv', mode="a", newline="") as file:
        csv_writer = csv.writer(file)
        n = max(all_id_client) + 1
        csv_writer.writerow([n, name])

times = 0
while True:
    menu_msg= """
Que desea hacer? (⁄ ⁄>⁄ ▽ ⁄<⁄ ⁄) 
Comprar - c
Recomiendame productos - r
Salir - salir

"""
    w = input(menu_msg).lower().strip()

    while w not in ["c", "r", "salir"]:
        print("\nCOMANDO NO ENCONTRADO")
        w = input(menu_msg).lower().strip()

    match w:
        case "c": #COMPRA
            print(
"""

Para añadir productos escriba su codigo (⁀ᗢ⁀). Y para añadir varios simplemente escribela por espacios.
Ejemplo: 101 105 103

"""
)
            print("Lista de productos:")
            productos_selected = [["producto", "precio"]]
            precio_total = 0.0
            tarjeta = {}
            direccion = ""

            with open('data/productos.csv', mode="r") as file:
                productos = list(csv.reader(file))
                table = []

                for i in productos:
                    table.append([ i[0], i[1], i[2] ])

                print(tabulate(table))

                ps = input("Seleccione sus productos ^w^: ").split(" ")
                ps = list(map(str, ps))

                for x in productos[1:]:
                    if str(x[0]) in str(ps):
                        productos_selected.append([x[1], x[2]])
                        precio_total = float(x[2]) + precio_total


            #TARJETA DE CREDITO
            tarjeta["codigo"] = input("Codigo de la tarjeta: ")
            tarjeta["cvv"] = input("CVV: ")
            tarjeta["fecha"] = input("Fecha de la tarjeta: ") 
            
            direccion = input("Escriba su direccion: ")

            #VISTA GENERAL
            print("\nVista general:")

            print("Productos: ")
            print(tabulate(productos_selected))
            print(f"Precio total: {precio_total}")


            print(f"""\n Tarjeta de credito:
                  "Codigo": {tarjeta["codigo"]}
                  "cvv:" {tarjeta["cvv"]}
                  "Fecha:" {tarjeta["fecha"]}
                  """)

            print(f"\n Direccion: {direccion}")

            confirm = input(
"""\nDesea confirmar?:
Si - s
No - n
Salir - salir
""")

            while confirm not in ["s", "n", "salir"]:
                confirm = input(
"""\nDesea confirmar?:
Si - s
No - n
Salir - salir
""")

            match confirm:
                case "s":
                    print("\nEspera un momento.... :D!")
                    with open('data/historial_compras.csv', mode="a", newline="") as file:
                        historial = csv.writer(file)
                        for i in productos:
                            historial.writerow([all_id_client[0], i])

                    print("Muchas gracias por su compra. Pase cuando quiera ＼(٥⁀▽⁀ )／ ")                        

                case "n":
                    print("Entendido compra cancelada (｡╯︵╰｡)")

                case "salir":
                    exit()

        case "r": #RECOMENDAR COMPRA
            a = recomendar_productos(all_id_client[0])
            if str(type(a)) == "<class 'pandas.core.series.Series'>":

                productos_recomendados = list(a.to_dict().keys())
                productos_recomendados = list(map(str, productos_recomendados))

                print("\nEsperemos que le guste (o^ ^o) :")

                with open('data/productos.csv', mode="r") as file:
                    productos = csv.reader(file)
                    table = [["producto_id", "nombre", "precio"]]

                    for i in list(productos)[1:]:
                        if str(i[0]) in productos_recomendados:
                            table.append([i[0], i[1], i[2]])

                    print(tabulate(table))

        case "salir": #SALIR DEL PROGRAMA
            exit()

    print(f"{times}################################################################################################\n")
    times += 1