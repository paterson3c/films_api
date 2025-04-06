CREATE OR REPLACE FUNCTION actualizarCarritoTrigger() RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
        PERFORM updateOrderTotal(NEW.orderid);
    ELSIF TG_OP = 'DELETE' THEN
        PERFORM updateOrderTotal(OLD.orderid);
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER actualizaCarrito
AFTER INSERT OR UPDATE OR DELETE ON orderdetail
FOR EACH ROW
EXECUTE FUNCTION actualizarCarritoTrigger();