SELECT order_no, man.full_name, cust.full_name FROM 'order'
INNER JOIN customer cust ON cust.customer_id = 'order'.customer_id
INNER JOIN manager man ON man.manager_id = 'order'.manager_id
WHERE man.city != cust.city