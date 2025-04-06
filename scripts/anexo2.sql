EXPLAIN SELECT COUNT (*)
FROM orders
WHERE status IS null;

EXPLAIN SELECT count(*)
FROM orders
WHERE status = 'Shipped';

CREATE INDEX IF NOT EXISTS idx_orders_status ON orders (status);

EXPLAIN SELECT COUNT (*)
FROM orders
WHERE status IS null;

EXPLAIN SELECT count(*)
FROM orders
WHERE status = 'Shipped';

ANALYZE orders;

EXPLAIN SELECT COUNT(*) FROM orders WHERE status IS NULL;
EXPLAIN SELECT COUNT(*) FROM orders WHERE status = 'Shipped';
EXPLAIN SELECT COUNT(*) FROM orders WHERE status = 'Paid';
EXPLAIN SELECT COUNT(*) FROM orders WHERE status = 'Processed';
