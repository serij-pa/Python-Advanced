SELECT cust.full_name, man.full_name, purchase_amount, 'date' FROM 'order'
INNER JOIN customer cust ON cust.customer_id = 'order'.customer_id
INNER JOIN manager man ON man.manager_id = 'order'.manager_id