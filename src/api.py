from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from quart import Quart, request, jsonify
import os

app = Quart(__name__)
DATABASE_URL = "postgresql://alumnodb:1234@db:5432/si1"

# Sincroniza la secuencia de orders
def _synchronize_sequence():
    query = text("SELECT setval('orders_orderid_seq', (SELECT MAX(orderid) FROM orders) + 1)")
    with create_engine(DATABASE_URL).connect() as conn:
        conn.execute(query)
    
    print("Secuencia de orderid sincronizada.")

# Crear un nuevo pedido
def _create_new_order(customer_id):
    query = text("""
        INSERT INTO orders (customerid, orderdate, status, netamount, tax, totalamount)
        VALUES (:customer_id, NOW(), 'Pending', 0, 15, 0)
        RETURNING orderid
    """)
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query, {'customer_id': customer_id}).fetchone()
    return result[0]

# Obtener el saldo de un cliente
def _get_balance(customer_id):
    query = text("SELECT balance FROM customers WHERE customerid = :customer_id")
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query, {'customer_id': customer_id}).fetchone()
    return result[0]

# Endpoint de login
@app.route("/login", methods=["POST"])
async def login():
    data = await request.json
    username = data.get("username")
    password = data.get("password")
    
    query = text("SELECT * FROM customers WHERE username = :username AND password = :password")
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query, {'username': username, 'password': password}).fetchone()
        
    if result:
        return jsonify({"message": "Login successful", "customer_id": result[0]}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Endpoint para añadir saldo
@app.route("/add_balance", methods=["POST"])
async def add_balance():
    data = await request.json
    customer_id = data.get("customer_id")
    amount = data.get("amount")
    password = data.get("password")
    
    # Verificar credenciales
    query = text("SELECT * FROM customers WHERE customerid = :customer_id AND password = :password")
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query, {'customer_id': customer_id, 'password': password}).fetchone()
        
    if not result:
        return jsonify({"message": "Invalid credentials"}), 401
    
    query = text("UPDATE customers SET balance = balance + :amount WHERE customerid = :customer_id")
    with create_engine(DATABASE_URL).connect() as conn:
        conn.execute(query, {'amount': amount, 'customer_id': customer_id})
    return jsonify({"message": f"Saldo de {amount}€ añadido correctamente."}), 200

# Endpoint para añadir un producto al carrito
@app.route("/add_to_cart", methods=["POST"])
async def add_to_cart():
    data = await request.json
    customer_id = data.get("customer_id")
    prod_id = data.get("prod_id")
    quantity = data.get("quantity")
    password = data.get("password")
    
    # Verificar credenciales
    query = text("SELECT * FROM customers WHERE customerid = :customer_id AND password = :password")
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query, {'customer_id': customer_id, 'password': password}).fetchone()
        
    if not result:
        return jsonify({"message": "Invalid credentials"}), 401
    
    # Verificar si hay stock suficiente
    query = text("SELECT stock FROM inventory WHERE prod_id = :prod_id")
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query, {'prod_id': prod_id}).fetchone()
        
        if not result:
            return jsonify({"message": "Producto no encontrado."}), 404
        
        stock = result[0]
        if stock < quantity:
            return jsonify({"message": "Stock insuficiente."}), 409

    # Busca o crea el pedido pendiente
    query = text("SELECT orderid FROM orders WHERE customerid = :customer_id AND status = 'Pending'")
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query, {'customer_id': customer_id}).fetchone()
        
        if result:
            order_id = result[0]
        else:
            order_id = _create_new_order(customer_id)
            
        query = text("""
            INSERT INTO orderdetail (orderid, prod_id, quantity, price)
            VALUES (:order_id, :prod_id, :quantity, (SELECT price FROM products WHERE prod_id = :prod_id))
        """)
        conn.execute(query, {'order_id': order_id, 'prod_id': prod_id, 'quantity': quantity})
    return jsonify({"message": f"{quantity} unidad(es) del producto {prod_id} añadido(s) al pedido {order_id}."}), 200

# Endpoint para pagar un pedido
@app.route("/pay_order", methods=["POST"])
async def pay_order():
    data = await request.json
    customer_id = data.get("customer_id")
    password = data.get("password")
    
    # Verificar credenciales
    query = text("SELECT * FROM customers WHERE customerid = :customer_id AND password = :password")
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query, {'customer_id': customer_id, 'password': password}).fetchone()
        
    if not result:
        return jsonify({"message": "Invalid credentials"}), 401
    
    
    
    query = text("SELECT orderid FROM orders WHERE customerid = :customer_id AND status = 'Pending'")
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query, {'customer_id': customer_id}).fetchone()
        
        if not result:
            return jsonify({"message": "No hay pedidos pendientes para este cliente."}), 404
        
        order_id = result[0]
        
        # comprobar que tiene saldo suficiente
        query = text("SELECT totalamount FROM orders WHERE orderid = :order_id")
        result = conn.execute(query, {'order_id': order_id}).fetchone()
        totalamount = result[0]
        balance = _get_balance(customer_id)
        if balance < totalamount:
            return jsonify({"message": "Saldo insuficiente."}), 409

        query = text("UPDATE orders SET status = 'Paid' WHERE orderid = :order_id")
        conn.execute(query, {'order_id': order_id})
    return jsonify({"message": f"Pedido {order_id} pagado correctamente."}), 200

# Endpoint para ver el carrito
@app.route("/view_cart", methods=["GET"])
async def view_cart():
    data = await request.json
    customer_id = data.get("customer_id")
    password = data.get("password")
    
    # Verificar credenciales
    query = text("SELECT * FROM customers WHERE customerid = :customer_id AND password = :password")
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query, {'customer_id': customer_id, 'password': password}).fetchone()
        
    if not result:
        return jsonify({"message": "Invalid credentials"}), 401
    
    query = text("SELECT orderid FROM orders WHERE customerid = :customer_id AND status = 'Pending'")
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query, {'customer_id': customer_id}).fetchone()
        
        if not result:
            return jsonify({"message": "No hay pedidos pendientes para este cliente."}), 404

        order_id = result[0]
        query = text("""
            SELECT od.prod_id, m.movietitle, od.quantity, od.price
            FROM orderdetail od
            JOIN products p ON od.prod_id = p.prod_id
            JOIN imdb_movies m ON p.movieid = m.movieid
            WHERE od.orderid = :order_id;
        """)
        result = conn.execute(query, {'order_id': order_id}).fetchall()
    
    if result:
        cart_items = []
        for row in result:
            cart_items.append({
                "Product ID": row['prod_id'],
                "Movie Title": row['movietitle'],
                "Quantity": row['quantity'],
                "Price per Unit (€)": row['price'],
                "Total Line Price (€)": row['quantity'] * row['price']
            })
        return jsonify({"cart": cart_items}), 200
    else:
        return jsonify({"message": "No hay productos en el carrito."}), 404

# Endpoint para eliminar un producto del carrito
@app.route("/remove_from_cart", methods=["POST"])
async def remove_from_cart():
    data = await request.json
    customer_id = data.get("customer_id")
    prod_id = data.get("prod_id")
    password = data.get("password")
    
    # Verificar credenciales
    query = text("SELECT * FROM customers WHERE customerid = :customer_id AND password = :password")
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query, {'customer_id': customer_id, 'password': password}).fetchone()
        
    if not result:
        return jsonify({"message": "Invalid credentials"}), 401
    
    query = text("SELECT orderid FROM orders WHERE customerid = :customer_id AND status = 'Pending'")
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query, {'customer_id': customer_id}).fetchone()
        
        if not result:
            return jsonify({"message": "No hay pedidos pendientes para este cliente."}), 404

        order_id = result[0]
        query = text("DELETE FROM orderdetail WHERE orderid = :order_id AND prod_id = :prod_id")
        conn.execute(query, {'order_id': order_id, 'prod_id': prod_id})
    return jsonify({"message": f"Producto {prod_id} eliminado del carrito."}), 200

# Endpoint para editar la cantidad de un producto en el carrito
@app.route("/edit_cart", methods=["POST"])
async def edit_cart():
    data = await request.json
    customer_id = data.get("customer_id")
    prod_id = data.get("prod_id")
    quantity = data.get("quantity")
    password = data.get("password")
    
    # Verificar credenciales
    query = text("SELECT * FROM customers WHERE customerid = :customer_id AND password = :password")
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query, {'customer_id': customer_id, 'password': password}).fetchone()
        
    if not result:
        return jsonify({"message": "Invalid credentials"}), 401
    
    # Verificar si hay stock suficiente
    query = text("SELECT stock FROM inventory WHERE prod_id = :prod_id")
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query, {'prod_id': prod_id}).fetchone()
        
        if not result:
            return jsonify({"message": "Producto no encontrado."}), 404
        
        stock = result[0]
        if stock < quantity:
            return jsonify({"message": "Stock insuficiente."}), 409
    
    query = text("SELECT orderid FROM orders WHERE customerid = :customer_id AND status = 'Pending'")
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query, {'customer_id': customer_id}).fetchone()
        
        if not result:
            return jsonify({"message": "No hay pedidos pendientes para este cliente."}), 404

        order_id = result[0]
        query = text("UPDATE orderdetail SET quantity = :quantity WHERE orderid = :order_id AND prod_id = :prod_id")
        conn.execute(query, {'quantity': quantity, 'order_id': order_id, 'prod_id': prod_id})
    return jsonify({"message": f"Producto {prod_id} actualizado a {quantity} unidades."}), 200

# Endpoint para obtener el historial de pedidos
@app.route("/get_orders", methods=["GET"])
async def get_orders():
    data = await request.json
    customer_id = data.get("customer_id")
    password = data.get("password")
    
    # Verificar credenciales
    query = text("SELECT * FROM customers WHERE customerid = :customer_id AND password = :password")
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query, {'customer_id': customer_id, 'password': password}).fetchone()
        
    if not result:
        return jsonify({"message": "Invalid credentials *"}), 401
    
    query = text("SELECT orderid, orderdate, status, totalamount FROM orders WHERE customerid = :customer_id")
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query, {'customer_id': customer_id}).fetchall()

    if result:
        orders = []
        for row in result:
            orders.append({
                "Order ID": row['orderid'],
                "Order Date": row['orderdate'],
                "Status": row['status'],
                "Total Amount (€)": row['totalamount']
            })
        return jsonify({"orders": orders}), 200
    else:
        return jsonify({"message": "No hay pedidos para este cliente."}), 404

# Endpoint para obtener los detalles de un pedido        
@app.route("/get_order_details", methods=["GET"])
async def get_order_details():
    data = await request.json
    order_id = data.get("order_id")
    
    query = text("""
        SELECT od.prod_id, m.movietitle, od.quantity, od.price
        FROM orderdetail od
        JOIN products p ON od.prod_id = p.prod_id
        JOIN imdb_movies m ON p.movieid = m.movieid
        WHERE od.orderid = :order_id;
    """)
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query, {'order_id': order_id}).fetchall()
    
    if result:
        order_details = []
        for row in result:
            order_details.append({
                "Product ID": row['prod_id'],
                "Movie Title": row['movietitle'],
                "Quantity": row['quantity'],
                "Price per Unit (€)": row['price'],
                "Total Line Price (€)": row['quantity'] * row['price']
            })
        return jsonify({"order_details": order_details}), 200
    else:
        return jsonify({"message": "No hay detalles para este pedido."}), 404

# Endpoint para obtener el estado de un pedido
@app.route("/get_order_status", methods=["GET"])
async def get_order_status():
    data = await request.json
    order_id = data.get("order_id")
    
    query = text("SELECT status FROM orders WHERE orderid = :order_id")
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query, {'order_id': order_id}).fetchone()
    
    if result:
        return jsonify({"status": result[0]}), 200
    else:
        return jsonify({"message": "No se encontró el pedido."}), 404

# Endpoint para obtener el saldo de un cliente
@app.route("/get_balance", methods=["GET"])
async def get_balance():
    data = await request.json
    customer_id = data.get("customer_id")
    password = data.get("password")
    
    # Verificar credenciales
    query = text("SELECT * FROM customers WHERE customerid = :customer_id AND password = :password")
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query, {'customer_id': customer_id, 'password': password}).fetchone()
        
    if not result:
        return jsonify({"message": "Invalid credentials"}), 401
    
    query = text("SELECT balance FROM customers WHERE customerid = :customer_id")
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query, {'customer_id': customer_id}).fetchone()
    
    if result:
        return jsonify({"balance": result[0]}), 200
    else:
        return jsonify({"message": "No se encontró el cliente."}), 404

# Endpoint para cambiar la contraseña de un cliente
@app.route("/change_password", methods=["POST"])
async def change_password():
    data = await request.json
    customer_id = data.get("customer_id")
    new_password = data.get("new_password")
    password = data.get("old_password")
    
    # Verificar credenciales
    query = text("SELECT * FROM customers WHERE customerid = :customer_id AND password = :password")
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query, {'customer_id': customer_id, 'password': password}).fetchone()
        
    if not result:
        return jsonify({"message": "Invalid credentials"}), 401
    
    # Actualizar la contraseña del usuario
    query = text("UPDATE customers SET password = :new_password WHERE customerid = :customer_id")
    with create_engine(DATABASE_URL).begin() as conn:
        conn.execute(query, {'new_password': new_password, 'customer_id': customer_id})
        
    return jsonify({"message": "Contraseña actualizada correctamente."}), 200

# Endpoint para crear un nuevo usuario
@app.route("/create_user", methods=["POST"])
async def create_user():
    data = await request.json
    username = data.get("username")
    password = data.get("password")
    address = data.get("address")
    email = data.get("email")
    creditcard = data.get("creditcard")
    balance = 0
    
    query = text("SELECT setval('customers_customerid_seq', (SELECT MAX(customerid) FROM customers) + 1);")
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query)
    
    # Verificar si el usuario ya existe
    query = text("SELECT * FROM customers WHERE username = :username")
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query, {'username': username}).fetchone()

    if result:
        return jsonify({"message": "El usuario ya existe."}), 409

    # Insertar nuevo usuario, sin especificar customerid (autogenerado)
    query = text("""
        INSERT INTO customers (username, password, address, email, creditcard, balance)
        VALUES (:username, :password, :address, :email, :creditcard, :balance)
    """)
    with create_engine(DATABASE_URL).begin() as conn:
        conn.execute(query, {
            'username': username,
            'password': password,
            'address': address,
            'email': email,
            'creditcard': creditcard,
            'balance': balance
        })

    return jsonify({"message": f"Usuario {username} creado correctamente."}), 200

# Endpoint para eliminar un usuario
@app.route("/delete_user", methods=["POST"])
async def delete_user():
    data = await request.json
    customer_id = data.get("customer_id")
    password = data.get("password")
    
    # Verificar si el usuario existe y las credenciales son correctas
    query = text("SELECT * FROM customers WHERE customerid = :customer_id AND password = :password")
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query, {'customer_id': customer_id, 'password': password}).fetchone()
    
    if not result:
        return jsonify({"message": "Invalid credentials or user not found"}), 401

    # Eliminar al usuario si se encuentran las credenciales correctas
    delete_query = text("DELETE FROM customers WHERE customerid = :customer_id")
    with create_engine(DATABASE_URL).begin() as conn:
        conn.execute(delete_query, {'customer_id': customer_id})

    return jsonify({"message": "Usuario eliminado correctamente."}), 200

# Endpoint para obtener los productos disponibles
@app.route("/get_available_products", methods=["GET"])
async def get_available_products():
    query = text("""SELECT p.prod_id, m.movieid, m.movietitle, p.price, i.stock, p.description
        FROM products p
        JOIN imdb_movies m ON p.movieid = m.movieid
        JOIN inventory i ON p.prod_id = i.prod_id
        WHERE i.stock > 0
    """)
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query).fetchall()
    
    if result:
        products = []
        for row in result:
            products.append({
                "Product ID": row['prod_id'],
                "Movie ID": row['movieid'],
                "Movie Title": row['movietitle'],
                "Price (€)": row['price'],
                "Stock": row['stock'],
                "Description": row['description']
            })
        return jsonify({"products": products}), 200
    else:
        return jsonify({"message": "No hay productos disponibles."}), 404

# Endpoint para obtener los productos disponibles filtrados por idioma y género
@app.route("/get_available_products_filter", methods=["GET"])
async def get_available_products_filter():
    data = await request.json
    language = data.get("language")
    genre = data.get("genre")
    
    string_query = """
        SELECT p.prod_id, m.movieid, m.movietitle, p.price, i.stock, p.description, m.languages, m.genres
        FROM products p
        JOIN imdb_movies m ON p.movieid = m.movieid
        JOIN inventory i ON p.prod_id = i.prod_id
        WHERE i.stock > 0"""
    
    # Filtrar por idioma
    if language:
        string_query += " AND m.languages ILIKE '%' || :language || '%'"

    # Filtrar por género si está especificado
    if genre:
        string_query += " AND m.genres ILIKE '%' || :genre || '%'"
        
    query = text(string_query)
    
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query, {'language': language, 'genre': genre}).fetchall()
    
    if result:
        products = []
        for row in result:
            products.append({
                "Product ID": row['prod_id'],
                "Movie ID": row['movieid'],
                "Movie Title": row['movietitle'],
                "Price (€)": row['price'],
                "Stock": row['stock'],
                "Description": row['description']
            })
        return jsonify({"products": products}), 200
    else:
        return jsonify({"message": "No hay productos disponibles."}), 404

# Endpoint para obtener información de un producto
@app.route("/get_product_info", methods=["GET"])
async def get_product_info():
    data = await request.json
    prod_id = data.get("prod_id")
    
    query = text("""
        SELECT p.prod_id, m.movieid, m.movietitle, p.price, i.stock, p.description
        FROM products p
        JOIN imdb_movies m ON p.movieid = m.movieid
        JOIN inventory i ON p.prod_id = i.prod_id
        WHERE p.prod_id = :prod_id
    """)
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query, {'prod_id': prod_id}).fetchone()
    
    if result:
        product = {
            "Product ID": result['prod_id'],
            "Movie ID": result['movieid'],
            "Movie Title": result['movietitle'],
            "Price (€)": result['price'],
            "Stock": result['stock'],
            "Description": result['description']
        }
        return jsonify({"product": product}), 200
    else:
        return jsonify({"message": "Producto no encontrado."}), 404

# Endpoint para obtener información de una película
@app.route("/get_movie_info", methods=["GET"])
async def get_movie_info():
    data = await request.json
    movie_id = data.get("movie_id")
    
    query = text("""SELECT m.movieid, m.movietitle, d.directorname, m.year, m.issuspended, m.movietype, m.countries, m.genres, m.languages
FROM imdb_movies m
JOIN imdb_directormovies dm ON m.movieid = dm.movieid
JOIN imdb_directors d ON dm.directorid = d.directorid
WHERE m.movieid = :movie_id

                """)
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query, {'movie_id': movie_id}).fetchone()
    
    if result:
        movie = {
            "Movie ID": result['movieid'],
            "Movie Title": result['movietitle'],
            "Director": result['directorname'],
            "Year": result['year'],
            "Suspended": result['issuspended'],
            "Type": result['movietype'],
            "Country": result['countries'],
            "Genre": result['genres'],
            "Language": result['languages']
        }
        return jsonify({"movie": movie}), 200
    else:
        return jsonify({"message": "Película no encontrada."}), 404

@app.route("/get_languages", methods=["GET"])
async def get_languages():
    query = text("SELECT DISTINCT languages FROM imdb_movies")

    languages = set()  # Usar un conjunto para evitar duplicados
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query).fetchall()
        for row in result:
            if row['languages']:
                languages.update([lang.strip() for lang in row['languages'].split(',')])

    if languages:
        return jsonify({"message": "Languages list given", "languages": sorted(list(languages))}), 200
    else:
        return jsonify({"message": "No languages found"}), 404

@app.route("/get_genres", methods=["GET"])
async def get_genres():
    query = text("SELECT DISTINCT genres FROM imdb_movies")

    genres = set()  # Usar un conjunto para evitar duplicados
    with create_engine(DATABASE_URL).connect() as conn:
        result = conn.execute(query).fetchall()
        for row in result:
            if row['genres']:
                genres.update([genre.strip() for genre in row['genres'].split(',')])

    if genres:
        return jsonify({"message": "Genres list given", "genres": sorted(list(genres))}), 200
    else:
        return jsonify({"message": "No genres found"}), 404



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
    _synchronize_sequence()
