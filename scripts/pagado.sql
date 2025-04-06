CREATE OR REPLACE FUNCTION actualizarPedidoPagado() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'Paid' THEN
        UPDATE inventory
        SET stock = stock - od.quantity,
        sales = sales + od.quantity
        FROM orderdetail od
        WHERE od.prod_id = inventory.prod_id AND od.orderid = NEW.orderid;

        UPDATE customers
        SET balance = balance - NEW.totalamount
        WHERE customerid = NEW.customerid;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER pagado
AFTER UPDATE OF status ON orders
FOR EACH ROW
WHEN (NEW.status = 'Paid')
EXECUTE FUNCTION actualizarPedidoPagado();
