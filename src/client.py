import requests

BASE_URL = "http://localhost:5050"

# Login del usuario
def login(username, password):
    """
    Inicia sesión en el sistema.

    Args:
        username (str): El nombre de usuario.
        password (str): La contraseña del usuario.

    Returns:
        str or None: ID del cliente si el inicio de sesión es exitoso, None si las credenciales son incorrectas.
    """
    
    print()
    response = requests.post(f"{BASE_URL}/login", json={'username': username, 'password': password})
    if response.status_code == 200:
        customer_id = response.json().get("customer_id")
        print("Login successful")
        return customer_id
    else:
        print("Invalid credentials")
        return None

# Añadir saldo a la cuenta del usuario
def add_balance(customer_id, amount, password):
    """
    Añade saldo a la cuenta del usuario.

    Args:
        customer_id (str): ID del cliente.
        amount (float): La cantidad de saldo a añadir.
        password (str): La contraseña del usuario.
    """
    print()
    response = requests.post(f"{BASE_URL}/add_balance", json={'customer_id': customer_id, 'amount': amount, 'password': password})
    if response.status_code == 200:
        print(response.json().get("message"))
    else:
        print("Error al añadir saldo")

# Añadir un producto al carrito
def add_to_cart(customer_id, prod_id, quantity, password):
    """
    Añade un producto al carrito del usuario.

    Args:
        customer_id (str): ID del cliente.
        prod_id (int): ID del producto a añadir.
        quantity (int): Cantidad del producto.
        password (str): La contraseña del usuario.
    """
    print()
    response = requests.post(f"{BASE_URL}/add_to_cart", json={'customer_id': customer_id, 'prod_id': prod_id, 'quantity': quantity, 'password': password})
    if response.status_code == 200:
        print(response.json().get("message"))
    else:
        print("Error al añadir producto al carrito")

# Pagar el pedido
def pay_order(customer_id, password):
    """
    Realiza el pago del pedido del usuario.

    Args:
        customer_id (str): ID del cliente.
        password (str): La contraseña del usuario.
    """
    print()
    response = requests.post(f"{BASE_URL}/pay_order", json={'customer_id': customer_id, 'password': password})
    if response.status_code == 200:
        print(response.json().get("message"))
    else:
        print("Error al pagar el pedido")

# Ver carrito
def view_cart(customer_id, password):
    """
    Muestra el contenido del carrito del usuario.

    Args:
        customer_id (str): ID del cliente.
        password (str): La contraseña del usuario.
    """
    print()
    print("""
          ⠀⢀⣀⣀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢀⣀⣀⣀⣀⣀⣀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⣀⣀⣀⣀⣀⣀⡀⠀⠀
⠀⠀⢠⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⡄⠀⠀
⠀⠀⣿⣿⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⢹⣿⣿⣿⣿⡟⣿⣿⣿⣿⣿⠀⠀
⠀⠀⣿⣿⣿⣿⡟⢸⣿⣿⣿⣿⢹⣿⣿⣿⣿⡘⣿⣿⣿⣿⡇⢻⣿⣿⣿⣿⠀⠀
⠀⢀⣛⣛⣛⣛⠃⣛⣛⣛⣛⡋⠈⣛⣛⣛⣛⠁⢛⣛⣛⣛⣛⠘⣛⣛⣛⣛⡀⠀
⠀⠈⠻⠿⠿⠋⣀⠈⠻⠿⠟⢁⡀⠙⠿⠿⠋⢀⡈⠻⠿⠟⠁⣀⠙⠿⠿⠟⠁⠀
⠀⢸⣷⣦⣶⣿⣿⣿⣶⣤⣶⣿⣿⣷⣦⣴⣾⣿⣿⣶⣤⣶⣿⣿⣿⣶⣴⣾⡇⠀
⠀⢸⣿⡏⣉⣉⣉⣉⣉⣉⣉⣉⣉⣉⣉⣉⣉⡉⢹⣿⠉⣉⣉⣉⣉⣉⢹⣿⡇⠀
⠀⢸⣿⡇⣿⠉⢉⣩⣭⣽⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⠀⣿⣿⣿⣿⣿⢸⣿⡇⠀
⠀⢸⣿⡇⣿⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⠀⠿⠿⠿⠿⠿⢸⣿⡇⠀
⠀⢸⣿⡇⣿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⠀⠶⠶⠶⠶⠶⢸⣿⡇⠀
⠀⢸⣿⡇⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⢸⣿⠀⣶⣶⣶⣶⣶⢸⣿⡇⠀
⠀⢸⣿⣷⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣾⣿⠀⣿⣿⣿⣿⣿⢸⣿⡇⠀
⠀⠈⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠀⠉⠉⠉⠉⠉⠈⠉⠁⠀
¡Estos son los productos en tu carrito!
          """)
    response = requests.get(f"{BASE_URL}/view_cart", json={'customer_id': customer_id, 'password': password})
    if response.status_code == 200:
        cart = response.json().get("cart")
        total = 0
        for index, item in enumerate(cart, start=1):
            print(f"  Producto {index}:")
            print(f"    ID del Producto: {item['Product ID']}")
            print(f"    Título de la Película: {item['Movie Title']}")
            print(f"    Cantidad: {item['Quantity']}")
            print(f"    Precio por unidad: {item['Price per Unit (€)']}€")
            print(f"    Precio total por línea: {item['Total Line Price (€)']}€")
            print()
            total += int(item['Total Line Price (€)'])
        print(f"Total a pagar: {total}€")
    else:
        print(response.json().get("message"))

# Eliminar producto del carrito
def remove_from_cart(customer_id, prod_id, password):
    """
    Elimina un producto del carrito del usuario.

    Args:
        customer_id (str): ID del cliente.
        prod_id (int): ID del producto a eliminar.
        password (str): La contraseña del usuario.
    """
    print()
    response = requests.post(f"{BASE_URL}/remove_from_cart", json={'customer_id': customer_id, 'prod_id': prod_id, 'password': password})
    if response.status_code == 200:
        print(response.json().get("message"))
    else:
        print("Error al eliminar producto del carrito")

# Obtener historial de pedidos
def get_orders(customer_id, password):
    """
    Muestra el historial de pedidos del usuario.

    Args:
        customer_id (str): ID del cliente.
        password (str): La contraseña del usuario.
    """
    print()
    response = requests.get(f"{BASE_URL}/get_orders", json={'customer_id': customer_id, 'password': password})
    if response.status_code == 200:
        orders = response.json().get("orders")
        for order in orders:
            print(f"Pedido {order['Order ID']}:")
            print(f"  Estado: {order['Status']}")
            print(f"  Fecha de Creación: {order['Order Date']}")
            print(f"  Total: {order['Total Amount (€)']}")
            print()
    else:
        print(response.json().get("message"))

# Editar el carrito
def edit_cart(customer_id, prod_id, quantity, password):
    """
    Edita la cantidad de un producto en el carrito del usuario.

    Args:
        customer_id (str): ID del cliente.
        prod_id (int): ID del producto a editar.
        quantity (int): Nueva cantidad del producto.
        password (str): La contraseña del usuario.
    """
    print()
    response = requests.post(f"{BASE_URL}/edit_cart", json={'customer_id': customer_id, 'prod_id': prod_id, 'quantity': quantity, 'password': password})
    if response.status_code == 200:
        print(response.json().get("message"))
    else:
        print("Error al editar el carrito")

# Obtener detalles del pedido
def get_order_details(order_id):
    """
    Muestra los detalles de un pedido específico.

    Args:
        order_id (int): ID del pedido.
    """
    print()
    response = requests.get(f"{BASE_URL}/get_order_details", json={'order_id': order_id})
    if response.status_code == 200:
        order_details = response.json().get("order_details")
        print(f"Detalles del Pedido {order_id}:")
        for detail in order_details:
            print(f"Producto {detail['Product ID']}:")
            print(f"  Título de la Película: {detail['Movie Title']}")
            print(f"  Cantidad: {detail['Quantity']}")
            print(f"  Precio por unidad: {detail['Price per Unit (€)']}€")
            print(f"  Precio total por línea: {detail['Total Line Price (€)']}€")
            print()
        print()
    else:
        print(response.json().get("message"))

# Obtener estado del pedido
def get_order_status(order_id):
    """
    Muestra el estado de un pedido específico.

    Args:
        order_id (int): ID del pedido.
    """
    print()
    response = requests.get(f"{BASE_URL}/get_order_status", json={'order_id': order_id})
    if response.status_code == 200:
        print(f"Estado del Pedido {order_id}: {response.json().get('status')}")
    else:
        print(response.json().get("message"))

# Obtener saldo
def get_balance(customer_id, password):
    """
    Muestra el saldo disponible en la cuenta del usuario.

    Args:
        customer_id (str): ID del cliente.
        password (str): La contraseña del usuario.
    """
    print()
    response = requests.get(f"{BASE_URL}/get_balance", json={'customer_id': customer_id, 'password': password})
    if response.status_code == 200:
        print(f"Saldo actual: {response.json().get('balance')}€")
    else:
        print(response.json().get("message"))

# Cambiar contraseña
def change_password(customer_id, old_password, new_password):
    """
    Cambia la contraseña del usuario.

    Args:
        customer_id (str): ID del cliente.
        old_password (str): La contraseña actual.
        new_password (str): La nueva contraseña.
    """
    print()
    response = requests.post(f"{BASE_URL}/change_password", json={'customer_id': customer_id, 'old_password': old_password, 'new_password': new_password})
    if response.status_code == 200:
        print(response.json().get("message"))
    else:
        print(response.json().get("message"))

# Crear usuario
def create_user(username, password, address, email, creditcard):
    """
    Crea un nuevo usuario en el sistema.

    Args:
        username (str): El nombre de usuario.
        password (str): La contraseña del usuario.
        address (str): La dirección del usuario.
        email (str): El correo electrónico del usuario.
        creditcard (str): La tarjeta de crédito del usuario.
    """
    print()
    response = requests.post(f"{BASE_URL}/create_user", json={'username': username, 'password': password, 'address': address, 'email': email, 'creditcard': creditcard})
    if response.status_code == 200:
        print(response.json().get("message"))
    else:
        print(response.json().get("message"))

# Eliminar usuario        
def delete_user(customer_id, password):
    """
    Elimina un usuario del sistema.

    Args:
        customer_id (str): ID del cliente.
        password (str): La contraseña del usuario.
    """
    print()
    response = requests.post(f"{BASE_URL}/delete_user", json={'customer_id': customer_id, 'password': password})
    try:
        response_data = response.json()
        print(response_data.get("message"))
    except requests.exceptions.JSONDecodeError:
        # Si hay un error al decodificar JSON, imprimir el contenido de la respuesta
        print(f"Error inesperado: {response.status_code} - {response.text}")

# Obtener productos disponibles
def get_available_products():
    """
    Muestra todos los productos disponibles para la compra.
    """
    print()
    response = requests.get(f"{BASE_URL}/get_available_products")
    if response.status_code == 200:
        products = response.json().get("products")   
        for product in products:
            print(f"Producto {product['Product ID']}:")
            print(f"  ID de la Película: {product['Movie ID']}")
            print(f"  Título de la Película: {product['Movie Title']}")
            print(f"  Precio: {product['Price (€)']}€")
            print(f"  Stock: {product['Stock']}")
            print(f"  Descripción: {product['Description']}")
            print()
    else:
        print(response.json().get("message"))

# Obtener productos disponibles filtrados por idioma y género
def get_available_products_filter(language, genre):
    """
    Muestra los productos disponibles filtrados por idioma y género.

    Args:
        language (str): Idioma del producto.
        genre (str): Género del producto.
    """
    print()
    # Realizar la solicitud GET
    response = requests.get(f"{BASE_URL}/get_available_products_filter", json={'language': language, 'genre': genre})
    
    if response.status_code == 200:
        print("Productos disponibles: ")
        products = response.json().get("products", [])
        for index, product in enumerate(products, start=1):
            print(f"Producto {index}:")
            print(f"  ID del Producto: {product['Product ID']}")
            print(f"  ID de la Película: {product['Movie ID']}")
            print(f"  Título de la Película: {product['Movie Title']}")
            print(f"  Precio: {product['Price (€)']}€")
            print(f"  Stock: {product['Stock']}")
            print(f"  Descripción: {product['Description']}")
            print()
    else:
        print(response.json().get("message"))

# Obtener información detallada de un producto
def get_product_info(prod_id):
    """
    Muestra la información detallada de un producto específico.

    Args:
        prod_id (int): ID del producto.
    """
    print()
    response = requests.get(f"{BASE_URL}/get_product_info", json={'prod_id': prod_id})
    if response.status_code == 200:
        product = response.json().get("product")
        print(f"Producto {product['Product ID']}:")
        print(f"  ID de la Película: {product['Movie ID']}")
        print(f"  Título de la Película: {product['Movie Title']}")
        print(f"  Precio: {product['Price (€)']}€")
        print(f"  Stock: {product['Stock']}")
        print(f"  Descripción: {product['Description']}")
        print()
    else:
        print(response.json().get("message"))

# Obtener información de una película
def get_movie_info(movie_id):
    """
    Muestra la información detallada de una película específica.

    Args:
        movie_id (int): ID de la película.
    """
    print()
    response = requests.get(f"{BASE_URL}/get_movie_info", json={'movie_id': movie_id})
    if response.status_code == 200:
        movie = response.json().get("movie")
        print(f"Película {movie['Movie ID']}:")
        print(f"  Título de la Película: {movie['Movie Title']}")
        print(f"  Director: {movie['Director']}")
        print(f"  Año: {movie['Year']}")
        if movie['Suspended'] == 1:
            print("  Estado: Suspendida")
        else: 
            print("  Estado: No suspendida")
        print(f"  Tipo: {movie['Type']}")
        print(f"  País: {movie['Country']}")
        print(f"  Género: {movie['Genre']}")
        print(f"  Idioma: {movie['Language']}")
        print()
    else:
        print(response.json().get("message"))

# Obtener lista de idiomas
def get_languages():
    """
    Muestra todos los idiomas disponibles en las películas.
    """
    print()
    response = requests.get(f"{BASE_URL}/get_languages")
    if response.status_code == 200:
        print("Languages: ")
        languages = response.json().get("languages", [])
        for index, item in enumerate(languages, start=1):
            print(f" {index}. {item}")
    else:
        print(response.json().get("message"))

# Obtener lista de géneros
def get_genres():
    """
    Muestra todos los géneros disponibles en las películas.
    """
    print()
    response = requests.get(f"{BASE_URL}/get_genres")
    
    try:
        if response.status_code == 200:
            print("Genres: ")
            genres = response.json().get("genres", [])
            for index, item in enumerate(genres, start=1):
                print(f" {index}. {item}")
        else:
            print(response.json().get("message"))
    except requests.exceptions.JSONDecodeError:
        print("Error inesperado: No se pudo decodificar la respuesta JSON.")


if __name__ == "__main__":
    # Configurar las credenciales del usuario
    username = "usuario_demo"
    password = "password_demo"
    new_password = "nuevo_password_demo"

    # 1. Crear usuario (opcional si ya existe)
    print("\n--- 1. Creando usuario ---")
    create_user(username, password, address="Calle Falsa 123", email="usuario@demo.com", creditcard="1111-2222-3333-4444")

    # 2. Iniciar sesión
    print("\n--- 2. Iniciando sesión ---")
    customer_id = login(username, password)
    if not customer_id:
        print("Error al iniciar sesión. Finalizando el proceso.")
        exit(1)

    # 3. Añadir saldo a la cuenta del usuario
    print("\n--- 3.  Añadiendo saldo a la cuenta ---")
    add_balance(customer_id, amount=200, password=password)
    
    print("\n --- 3.1 Verificando el saldo disponible ---")
    get_balance(customer_id, password)

    # 4. Buscar productos disponibles filtrando por idioma y género
    print("\n--- 4. Buscar productos filtrados por idioma y género ---")
    get_available_products_filter(language="Spanish", genre="Western")

    # 5. Añadir productos al carrito
    print("\n--- 5.  Añadiendo productos al carrito ---")
    productos_para_comprar = [
        {'prod_id': 659, 'quantity': 2},
        {'prod_id': 1002, 'quantity': 1},
        {'prod_id': 1506, 'quantity': 4}
    ]

    for producto in productos_para_comprar:
        add_to_cart(customer_id, prod_id=producto['prod_id'], quantity=producto['quantity'], password=password)

    # 6. Ver el contenido del carrito
    print("\n--- 6. Contenido del carrito actual ---")
    view_cart(customer_id, password)

    # 7. Editar cantidades en el carrito (opcional)
    print("\n--- 7. Editando cantidad de un producto en el carrito ---")
    edit_cart(customer_id, prod_id=659, quantity=5, password=password)

    # Ver el carrito nuevamente para confirmar el cambio
    print("\n--- Contenido del carrito después de la edición ---")
    view_cart(customer_id, password)

    # 8. Eliminar un producto del carrito (opcional)
    print("\n--- 8. Eliminando un producto del carrito ---")
    remove_from_cart(customer_id, prod_id=1002, password=password)

    # Ver el carrito nuevamente después de eliminar un producto
    print("\n--- Contenido del carrito después de eliminar un producto ---")
    view_cart(customer_id, password)

    # 9. Verificar saldo antes de proceder al pago
    print("\n--- 9. Verificando el saldo disponible ---")
    get_balance(customer_id, password)

    # 10. Realizar el pago del pedido
    print("\n--- 10. Realizando el pago del pedido ---")
    pay_order(customer_id, password)

    # 11. Verificar el historial de pedidos para confirmar el pedido realizado
    print("\n--- 11. Historial de pedidos ---")
    get_orders(customer_id, password)

    # 12. Cambiar la contraseña del usuario (opcional)
    print("\n--- 12. Cambiando la contraseña del usuario ---")
    change_password(customer_id, old_password=password, new_password=new_password)

    # Actualizar la contraseña para las siguientes operaciones
    password = new_password

    # 13. Verificar el saldo nuevamente después de la compra
    print("\n--- 13. Verificando el saldo después del pago ---")
    get_balance(customer_id, password)

    # 14. Obtener información sobre una película específica (opcional)
    print("\n--- 14. Información de una película específica ---")
    get_movie_info(movie_id=60830)

    # 15. Verificar el listado de idiomas disponibles
    print("\n--- 15. Listado de idiomas disponibles ---")
    get_languages()

    # 16. Obtener géneros de películas disponibles
    print("\n--- 16. Listado de géneros disponibles ---")
    get_genres()

    # 17. Obtener productos disponibles (IMPRIME LA PANTALLA ENTERA ASI QUE NO SE VERA EL RESTO DEL TEST)
    #print("\n--- 17. Productos disponibles ---")
    #get_available_products()

    # 18. Eliminar el usuario (opcional)
    print("\n--- 18. Eliminando usuario ---")
    delete_user(customer_id, password)
    
    # 19. Verificar si el usuario ha sido eliminado
    print("\n--- 18.1 Verificando si el usuario ha sido eliminado ---")
    login(username, password)

    # Finalización del flujo
    print("\n--- Proceso de compra completado. ---")

