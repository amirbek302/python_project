----------------CREATE SCHEMA------------------------------
-- customers
-- products
-- orders
-- logs
-- CREATE SCHEMA logs;
----------------CREATE SCHEMA------------------------------
--------------////////////////-----------------------------
----------------CREATE TABLE-------------------------------

-- CREATE TABLE IF NOT EXISTS customers.customers(
-- 	client_id SERIAL PRIMARY KEY,
-- 	telegram_id BIGINT UNIQUE NOT NULL,
-- 	username VARCHAR(50) NOT NULL,
-- 	bonus_points INTEGER DEFAULT 0
-- )

-- CREATE TABLE IF NOT EXISTS products.products(
-- 	product_id SERIAL PRIMARY KEY,
-- 	product_name VARCHAR(50) NOT NULL,
-- 	price NUMERIC(10,2) NOT NULL,
-- 	stock INTEGER DEFAULT 0
-- )


-- SELECT * FROM customers.customers;
-- ALTER TABLE products.products
-- ADD COLUMN photo VARCHAR(255);


-- INSERT INTO products.products(product_name, price, stock, photo)
-- VALUES
-- ('iPhone 15',1200,10,'images/iphone15.jpg'),
-- ('Samsung A55',500,15,'images/samsung.jpg'),
-- ('AirPods Pro',250,20,'images/airpods.jpg'),
-- ('Lenovo IdeaPad',900,8,'images/lenovo.jpg');


-- CREATE TABLE IF NOT EXISTS orders.orders(
-- 	order_id SERIAL PRIMARY KEY,
-- 	client_id INTEGER REFERENCES customers.customers(client_id),
-- 	status VARCHAR(20) DEFAULT 'new',
-- 	order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- )

-- SELECT 1;
-- SELECT * FROM orders.order_items
-- SELECT * FROM products.products
-- SELECT * FROM customers.customers
-- SELECT * FROM logs.price_logs
-- SELECT * FROM orders.orders

-- CREATE TABLE IF NOT EXISTS logs.price_logs(
-- 	log_id SERIAL PRIMARY KEY,
-- 	product_id INTEGER,
-- 	old_price NUMERIC(10,2),
-- 	new_price NUMERIC(10,2),
-- 	change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- )

-- CREATE TABLE orders.order_items(
--     item_id SERIAL PRIMARY KEY,
--     order_id INTEGER REFERENCES orders.orders(order_id),
--     product_id INTEGER REFERENCES products.products(product_id),
--     quantity INTEGER NOT NULL CHECK(quantity>0)

-- );

----------------CREATE TABLE-------------------------------
--------------////////////////-----------------------------
---------------CREATE TRIGGER-------------------------------

-- -- #1 Валидация: Проверка корректности данных 
-- CREATE OR REPLACE FUNCTION validate_price()
-- RETURNS TRIGGER
-- LANGUAGE plpgsql
-- AS $$
-- BEGIN
--     IF NEW.price <= 0 THEN
--         RAISE EXCEPTION 'Цена должна быть больше 0';
--     END IF;

--     RETURN NEW;
-- END;
-- $$;

-- CREATE TRIGGER trg_validate_price
-- BEFORE INSERT OR UPDATE
-- ON products.products
-- FOR EACH ROW
-- EXECUTE FUNCTION validate_price();


-- -- #2 for bonus (Автовычисление)
-- CREATE OR REPLACE FUNCTION add_bonus()
-- RETURNS TRIGGER
-- LANGUAGE plpgsql
-- AS $$
-- BEGIN
--     IF NEW.status = 'completed'
--        AND OLD.status <> 'completed' THEN

--         UPDATE customers.customers
-- 		SET bonus_points = bonus_points + 10
-- 		WHERE client_id = NEW.client_id;

--     END IF;

--     RETURN NEW;
-- END;
-- $$;

-- CREATE TRIGGER trg_add_bonus
-- AFTER UPDATE
-- ON orders.orders
-- FOR EACH ROW
-- EXECUTE FUNCTION add_bonus();



-- -- #3 изменение цены (Логирование)
-- CREATE OR REPLACE FUNCTION log_price_change()
-- RETURNS TRIGGER
-- LANGUAGE plpgsql
-- AS $$
-- BEGIN

--     INSERT INTO logs.price_logs(
--         product_id,
--         old_price,
--         new_price
--     )
--     VALUES(
--         OLD.product_id,
--         OLD.price,
--         NEW.price
--     );

--     RETURN NEW;
-- END;
-- $$;

-- CREATE TRIGGER trg_log_price
-- AFTER UPDATE
-- ON products.products
-- FOR EACH ROW
-- WHEN (OLD.price IS DISTINCT FROM NEW.price)
-- EXECUTE FUNCTION log_price_change();


-- -- #4 prevent delete (Защита данных) предотвратить
-- CREATE OR REPLACE FUNCTION prevent_product_delete()
-- RETURNS TRIGGER
-- LANGUAGE plpgsql
-- AS $$
-- BEGIN

--     IF EXISTS(
--         SELECT 1
--         FROM orders.order_items
--         WHERE product_id = OLD.product_id
--     ) THEN

--         RAISE EXCEPTION
--         'Нельзя удалить товар, участвующий в заказах';

--     END IF;

--     RETURN OLD;
-- END;
-- $$;

-- CREATE TRIGGER trg_prevent_delete
-- BEFORE DELETE
-- ON products.products
-- FOR EACH ROW
-- EXECUTE FUNCTION prevent_product_delete();

---------------CREATE TRIGGER-------------------------------
--------------////////////////-----------------------------
---------------CREATE FUNCTION------------------------------

-- DROP FUNCTION IF EXISTS create_order(INTEGER, INTEGER, INTEGER);
-- -- #1 сделать заказ
-- CREATE OR REPLACE FUNCTION create_order(
--     p_client_id INTEGER
-- )
-- RETURNS INTEGER
-- LANGUAGE plpgsql
-- AS $$
-- DECLARE
--     v_order_id INTEGER;
-- BEGIN

--     INSERT INTO orders.orders(client_id)
--     VALUES(p_client_id)
--     RETURNING order_id
--     INTO v_order_id;

--     RETURN v_order_id;

-- END;
-- $$;
-- -- SELECT create_order(?, ?, ?)

-- -- #2 искать самый популярный продукт
-- CREATE OR REPLACE FUNCTION most_popular_product()
-- RETURNS TABLE(
--     product_name VARCHAR,
--     total_orders BIGINT
-- )
-- LANGUAGE plpgsql
-- AS $$
-- BEGIN

--     RETURN QUERY

--     SELECT
--         p.product_name,
--         COUNT(*)
--     FROM orders.order_items oi
--     JOIN products.products p
--         ON oi.product_id = p.product_id
--     GROUP BY p.product_name
--     ORDER BY COUNT(*) DESC
--     LIMIT 1;

-- END;
-- $$;
-- -- SELECT most_popular_product()

-- -- #3 очистка старых логов
-- CREATE OR REPLACE FUNCTION clear_old_logs()
-- RETURNS VOID
-- LANGUAGE plpgsql
-- AS $$
-- BEGIN

--     DELETE
--     FROM logs.price_logs
--     WHERE change_date <
--           CURRENT_DATE - INTERVAL '30 days';

-- END;
-- $$;
-- -- SELECT clear_old_logs()

---------------CREATE FUNCTION------------------------------

-- педро-педро я всё