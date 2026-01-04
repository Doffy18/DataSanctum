CREATE TABLE food_orders (order_id SERIAL PRIMARY KEY, customer_name varchar(30),restaurant_name varchar(30),
	item varchar(30), amount numeric(10,2),order_status varchar(30), created_at timestamp default current_timestamp);

INSERT INTO food_orders 
(customer_name, restaurant_name, item, amount, order_status)
VALUES
('Rahul', 'Pizza Hut', 'Margherita Pizza', 299, 'PLACED'),
('Sneha', 'Burger King', 'Veg Whopper', 189, 'PLACED'),
('Amit', 'Dominos', 'Paneer Pizza', 349, 'PREPARING'),
('Kiran', 'Subway', 'Veg Sub', 249, 'DELIVERED'),
('Rohit', 'KFC', 'Zinger Burger', 199, 'PLACED'),
('Ananya', 'McDonalds', 'McVeggie', 159, 'CANCELLED'),
('Priya', 'Biryani House', 'Chicken Biryani', 450, 'DELIVERED'),
('Vikas', 'Taco Bell', 'Veg Taco', 129, 'PREPARING'),
('Meera', 'Haldiram', 'Samosa Plate', 99, 'PLACED'),
('Arjun', 'Starbucks', 'Cold Coffee', 280, 'PLACED');

SELECT * FROM food_orders;

INSERT INTO food_orders 
(customer_name, restaurant_name, item, amount, order_status)
VALUES
('Sabari', 'Pizza Hut', 'Margherita Pizza', 299, 'PLACED'),
('krishna', 'Burger King', 'Veg Whopper', 189, 'PLACED'),
('Ram', 'Dominos', 'Paneer Pizza', 349, 'PREPARING'),
('Priya', 'Subway', 'Veg Sub', 249, 'DELIVERED'),
('vaish', 'KFC', 'Zinger Burger', 199, 'PLACED');


INSERT INTO food_orders 
(customer_name, restaurant_name, item, amount, order_status)
VALUES
('kashi', 'Pizza Hut', 'Margherita Pizza', 299, 'PLACED');
