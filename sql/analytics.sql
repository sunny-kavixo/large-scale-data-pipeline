-- Revenue by city
SELECT city, SUM(revenue) AS total_revenue
FROM sales
GROUP BY city
ORDER BY total_revenue DESC;

-- Top products
SELECT product, SUM(quantity) AS units_sold, SUM(revenue) AS total_revenue
FROM sales
GROUP BY product
ORDER BY total_revenue DESC;

-- Monthly trend
SELECT DATE_TRUNC('month', order_date::timestamp) AS month,
       SUM(revenue) AS total_revenue
FROM sales
GROUP BY 1
ORDER BY 1;
