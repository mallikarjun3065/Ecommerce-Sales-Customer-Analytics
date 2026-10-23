-- Sales summary
SELECT
    ROUND(SUM(i.price), 2) AS total_sales,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(
        SUM(i.price) /
        NULLIF(COUNT(DISTINCT o.order_id), 0),
        2
    ) AS average_order_value
FROM orders o
JOIN order_items i
    ON o.order_id = i.order_id
WHERE o.order_status = 'delivered';

-- Monthly sales trend
SELECT
    DATE_FORMAT(
        o.order_purchase_timestamp, '%Y-%m'
    ) AS sales_month,
    ROUND(SUM(i.price), 2) AS monthly_sales
FROM orders o
JOIN order_items i
    ON o.order_id = i.order_id
WHERE o.order_status = 'delivered'
GROUP BY sales_month
ORDER BY sales_month;

-- top 10 product categories
SELECT
    p.product_category_name,
    ROUND(SUM(i.price), 2) AS category_sales,
    COUNT(DISTINCT i.order_id) AS order_count
FROM order_items i
JOIN orders o
    ON i.order_id = o.order_id
JOIN products p
    ON i.product_id = p.product_id
WHERE o.order_status = 'delivered'
GROUP BY p.product_category_name
ORDER BY category_sales DESC
LIMIT 10;

-- Repeat customers
SELECT
    c.customer_unique_id,
    COUNT(DISTINCT o.order_id) AS order_count
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_unique_id
HAVING COUNT(DISTINCT o.order_id) > 1
ORDER BY order_count DESC;

-- Repeat customers percentage
WITH customer_orders AS (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS order_count
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
)
SELECT
    COUNT(*) AS total_customers,
    SUM(order_count > 1) AS repeat_customers,
    ROUND(
        100.0 * SUM(order_count > 1) /
        NULLIF(COUNT(*), 0),
        2
    ) AS repeat_customer_percentage
FROM customer_orders;
 
 -- Payment method anlaysis
 SELECT
    p.payment_type,
    ROUND(SUM(p.payment_value), 2) AS payment_value,
    COUNT(DISTINCT p.order_id) AS order_count
FROM order_payments p
JOIN orders o
    ON p.order_id = o.order_id
WHERE o.order_status = 'delivered'
GROUP BY p.payment_type
ORDER BY payment_value DESC;


