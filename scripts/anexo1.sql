EXPLAIN SELECT customerid
FROM customers
WHERE customerid NOT IN (
  SELECT customerid
  FROM orders
  WHERE status = 'Paid'
);

EXPLAIN SELECT customerid
FROm (
  SELECT customerid
  FROM customers
  UNION ALL
  SELECT customerid
  FROM orders
  WHERE STATUS ='Paid'
) AS A
GROUP BY customerid
HAVING COUNT(*) = 1;

EXPLAIN SELECT customerid
FROM customers
EXCEPT
 SELECT customerid
 FROM orders
 WHERE STATUS = 'Paid';