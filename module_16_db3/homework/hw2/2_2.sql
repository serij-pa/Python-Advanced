SELECT cust.full_name FROM customer cust
LEFT JOIN 'order' ord ON cust.customer_id = ord.customer_id
WHERE ord.customer_id IS NULL ORDER BY full_name