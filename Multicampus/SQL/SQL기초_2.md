### 멀티캠퍼스 인공지능 자연어처리[NLP]기반 기업 데이터 분석.
- 3주차 4일 (5/27)

SQL 기초_2
---
> ## 1. 기초 쿼리 실습_2 문제풀이.
>> ``` MySQL
>> use w3schools;
>> 
>> select Country, count(Country) as country_count From customers
>> group by country order by country_count desc;
>> 
>> select Country, City, count(City) as city_count from customers 
>> group by Country, City order by city_count desc;
>> 
>> select Country, count(Country) as country_count From customers
>> group by country having country_count > 5
>> order by country_count desc;
>> 
>> # 실습
>> 
>> select productname, price from products where productname like "C%" and price > 20
>> order by price desc;
>> 
>> select CategoryId, sum(price) as sum_price, max(price) as max_price , min(price) as min_price From products
>> group by CategoryId;
>> 
>> # inner join
>> 
>> select customers.CustomerName, orders.OrderDate from customers
>> inner join orders
>> on orders.CustomerID = customers.CustomerID;
>> 
>> select c.CustomerName, o.OrderDate from customers as c
>> inner join orders as o
>> on o.CustomerID = c.CustomerID;
>> 
>> select c.CustomerName, o.OrderDate from customers as c
>> left join orders as o
>> on o.CustomerID = c.CustomerID;
>> 
>> select c.CustomerName, o.OrderDate from customers as c
>> right join orders as o
>> on o.CustomerID = c.CustomerID;
>> 
>> # 실습2
>> #2_1
>> select s.City, s.SupplierName, p.ProductName, p.Price from Suppliers as s
>> inner join Products as p
>> on s.SupplierID = p.SupplierID;
>> #2_2
>> select c.CategoryName, p.ProductName from categories as c
>> inner join Products as p
>> on c.CategoryID = p.CategoryID
>> where c.CategoryName = 'Seafood';
>> #2_3
>> select s.Country, c.CategoryName, avg(price), count(ProductName) from Suppliers as s
>> inner join Products as p
>> on s.SupplierID = p.SupplierID
>> inner join categories as c
>> on c.CategoryID = p.CategoryID
>> group by country;
>> #2_4
>> select o.OrderID, c.CustomerName, e.LastName, s.ShipperName, count(o.OrderID) as order_count from Orders as o
>> inner join order_details as o_d
>> on o.OrderID = o_d.OrderID
>> inner join customers as c
>> on o.CustomerID  = c.CustomerID
>> inner join employees as e
>> on o.EmployeeID = e.EmployeeID
>> inner join shippers as s
>> on o.ShipperID = s.ShipperID
>> group by o.OrderID;
>> #2_5
>> select SupplierName, sum(Quantity) as sum_Quantity from order_details as o_d
>> inner join products as p
>> on o_d.ProductID = p.ProductID
>> inner join suppliers as s
>> on s.SupplierID = p.SupplierID
>> group by s.SupplierName
>> order by sum_Quantity desc
>> limit 3;
>> #2_6
>> select c_t.CategoryName, c.City, sum(o_d.Quantity) as sum_Quantity from orders as o
>> inner join order_details as o_d
>> on o.OrderID = o_d.OrderID
>> inner join customers as c
>> on o.CustomerID = c.CustomerID
>> inner join products as p
>> on p.ProductID  = o_d.ProductID
>> inner join categories as c_t
>> on c_t.CategoryID = p.CategoryID
>> group by c_t.CategoryName, c.City
>> order by sum_Quantity desc;
>> #2_7
>> select ProductName, sum(o_d.Quantity) as sum_Quantity, p.price*sum(o_d.Quantity) as sum_price from customers as c
>> inner join orders as o
>> on c.CustomerID = o.CustomerID
>> inner join order_details as o_d
>> on o.OrderID = o_d.OrderID
>> inner join products as p
>> on p.ProductID = o_d.ProductID
>> where c.country = 'USA'
>> group by p.ProductID
>> order by sum_Quantity desc;
>> 
>> select * from products where ProductName='Gnocchi di nonna Alice';
>> select * from order_details
>> ```
