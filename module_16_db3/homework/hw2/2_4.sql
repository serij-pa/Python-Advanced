SELECT order_no, cust.full_name FROM 'order'
INNER JOIN customer cust ON cust.customer_id = 'order'.customer_id
WHERE 'order'.manager_id IS NULL