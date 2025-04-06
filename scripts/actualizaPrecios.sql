CREATE OR REPLACE FUNCTION updateOrderTotal(id_order INTEGER) RETURNS VOID AS $$
DECLARE
    net_total NUMERIC := 0;
    tax_amount NUMERIC := 0;
    total NUMERIC := 0;
BEGIN
    PERFORM pg_catalog.set_config('session_replication_role', 'replica', true);

    UPDATE orderdetail od
    SET price = p.price
    FROM products p
    WHERE od.prod_id = p.prod_id AND od.orderid = id_order;

    SELECT SUM(price * quantity) INTO net_total
    FROM orderdetail
    WHERE orderid = id_order;

    SELECT tax INTO tax_amount
    FROM orders
    WHERE orderid = id_order;

    tax_amount := net_total * (tax_amount / 100);

    total := net_total + tax_amount;

    UPDATE orders
    SET netamount = net_total,
        totalamount = total
    WHERE orderid = id_order;

    PERFORM pg_catalog.set_config('session_replication_role', 'origin', true);
END;
$$ LANGUAGE plpgsql;

-- 2. Crear una función almacenada para actualizar todos los pedidos en lotes de 500
CREATE OR REPLACE FUNCTION updateAllOrdersTotalBatch(batch_size INTEGER) RETURNS VOID AS $$
DECLARE
    order_ids INTEGER[];
    offset_val INTEGER := 0;
    id_order INTEGER;
BEGIN
    LOOP
        EXECUTE FORMAT('SELECT ARRAY(SELECT orderid FROM orders ORDER BY orderid LIMIT %L OFFSET %L)', batch_size, offset_val) INTO order_ids;

        IF array_length(order_ids, 1) IS NULL THEN
            EXIT;
        END IF;

        FOREACH id_order IN ARRAY order_ids
        LOOP
            PERFORM updateOrderTotal(id_order);
        END LOOP;

        offset_val := offset_val + batch_size;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

SELECT updateAllOrdersTotalBatch(500);
