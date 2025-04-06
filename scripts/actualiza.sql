-- Script actualiza.sql.

-- Añadir columna balance a la tabla customers si no existe
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name='customers' AND column_name='balance'
    ) THEN
        ALTER TABLE customers ADD COLUMN balance BIGINT DEFAULT 0;
    END IF;
END $$;

-- Crear tabla likes para guardar valoraciones de los usuarios a las películas
CREATE TABLE IF NOT EXISTS likes (
    like_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customerid) ON DELETE CASCADE,
    movie_id INTEGER REFERENCES imdb_movies(movieid) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (customer_id, movie_id)
);

-- Modificar la columna password de la tabla customers
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name='customers' AND column_name='password'
    ) THEN
        ALTER TABLE customers ALTER COLUMN password TYPE VARCHAR(512);
    END IF;
END $$;

-- Crear función para establecer un saldo aleatorio para los clientes
CREATE OR REPLACE FUNCTION setCustomersBalance(IN initialBalance BIGINT) RETURNS VOID AS $$
BEGIN
    UPDATE customers SET balance = FLOOR(RANDOM() * initialBalance);
END;
$$ LANGUAGE plpgsql;

-- Llamar a la función para establecer el saldo de los clientes
SELECT setCustomersBalance(200);


-- Asegurar que las claves foráneas estén correctamente establecidas con acciones en cascada.
ALTER TABLE orders
    ADD CONSTRAINT fk_orders_customerid FOREIGN KEY (customerid)
    REFERENCES customers(customerid) ON DELETE CASCADE;

ALTER TABLE orderdetail
    ADD CONSTRAINT fk_orderdetail_orderid FOREIGN KEY (orderid)
    REFERENCES orders(orderid) ON DELETE CASCADE,
    ADD CONSTRAINT fk_orderdetail_prodid FOREIGN KEY (prod_id)
    REFERENCES products(prod_id) ON DELETE CASCADE;

ALTER TABLE inventory
    ADD CONSTRAINT fk_inventory_prodid FOREIGN KEY (prod_id)
    REFERENCES products(prod_id) ON DELETE CASCADE;

ALTER TABLE imdb_actormovies
    ADD CONSTRAINT fk_actormovies_actorid FOREIGN KEY (actorid)
    REFERENCES imdb_actors(actorid) ON DELETE CASCADE,
    ADD CONSTRAINT fk_actormovies_movieid FOREIGN KEY (movieid)
    REFERENCES imdb_movies(movieid) ON DELETE CASCADE;

-- Añadir restricciones para evitar valores inconsistentes
ALTER TABLE inventory
    ADD CONSTRAINT chk_inventory_stock CHECK (stock >= 0);

ALTER TABLE customers
    ADD CONSTRAINT chk_customers_balance CHECK (balance >= 0);

-- Crear índices para optimizar las consultas
CREATE INDEX IF NOT EXISTS idx_orders_customerid ON orders (customerid);
CREATE INDEX IF NOT EXISTS idx_orderdetail_orderid ON orderdetail (orderid);
CREATE INDEX IF NOT EXISTS idx_orderdetail_prodid ON orderdetail (prod_id);
CREATE INDEX IF NOT EXISTS idx_inventory_prodid ON inventory (prod_id);
CREATE INDEX IF NOT EXISTS idx_likes_customerid_movieid ON likes (customer_id, movie_id);
CREATE INDEX IF NOT EXISTS idx_imdb_actormovies_movieid ON imdb_actormovies (movieid);
CREATE INDEX IF NOT EXISTS idx_imdb_directormovies_movieid ON imdb_directormovies (movieid);
CREATE INDEX IF NOT EXISTS idx_orders_customerid_orderdate ON orders (customerid, orderdate);

-- Incluir otros scripts para actualizaciones adicionales
\i 'actualizaPrecios.sql'

\i 'actualizaTablas.sql'

\i 'actualizaCarrito.sql'

\i 'pagado.sql';