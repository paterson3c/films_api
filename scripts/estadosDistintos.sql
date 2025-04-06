EXPLAIN SELECT COUNT(DISTINCT c.state) AS distinct_state_count
FROM customers c
JOIN orders o ON o.customerid = c.customerid
WHERE EXTRACT(YEAR FROM o.orderdate) = 2017 
  AND c.country = 'Peru';

CREATE INDEX IF NOT EXISTS idx_customers_country ON customers (country);
CREATE INDEX IF NOT EXISTS idx_orders_customerid_orderdate ON orders (customerid, orderdate);


EXPLAIN SELECT COUNT(DISTINCT c.state) AS distinct_state_count
FROM customers c
JOIN orders o ON o.customerid = c.customerid
WHERE EXTRACT(YEAR FROM o.orderdate) = 2017 
  AND c.country = 'Peru';

DROP INDEX IF EXISTS idx_customers_country;
DROP INDEX IF EXISTS idx_orders_customerid_orderdate;

