### 멀티캠퍼스 인공지능 자연어처리[NLP]기반 기업 데이터 분석.
- 3주차 3일 (5/26)

SQL 기초.
---
> ## 1. 기초 쿼리 실습.
>> ``` MySQL
>> use w3schools;
>> 
>> SELECT *
>> FROM Customers
>> ORDER BY CustomerName ASC;
>> 
>> SELECT CustomerName, Country FROM Customers;
>> 
>> SELECT * FROM Customers;
>> 
>> SELECT DISTINCT Country From Customers;
>> 
>> select * from customers where country = 'France';
>> # country France인 것.
>> 
>> select * from customers where ContactName like 'Mar%';
>> # ContactName이 Mar로 시작하는 것
>> 
>> select * from customers where ContactName like '%et';
>> # ContactName이 et로 끝나는 것
>> 
>> select * from customers where country = 'France' and CustomerName like 'La%';
>> # country가 France이면서 CustomerName이 La로 시작하는 것.
>> 
>> select * from customers where country = 'Germany' or CustomerName like 'Ma%';
>> # county가 germany이거나 CustomerName이 Ma로 시작하는 것.
>> 
>> select * from customers where Not country = 'France';
>> # country가 France가 아닌 것.
>> 
>> select * from customers where country in ('France', 'spain');
>> country가 France 거나 spain인 것.
>> 
>> select ProductName, price from products where price >= 15 and price <= 20;
>> # price가 15~20 인 것.
>> 
>> select ProductName, price from products where ProductID in (select ProductID from products where price >= 15 and price <= 20);
>> # price가 15~20 인 것.
>> 
>> select ProductName, price from products where price between 15 and 20;
>> # price가 15~20 인 것.
>> 
>> select * from customers where PostalCode IS NULL;
>> # PostalCode가 NULL인 것.
>> 
>> select * from customers where PostalCode IS NOT NULL;
>> # PostalCode가 NULL이 아닌 것
>> 
>> select * from customers order by CustomerName asc;
>> # CustomerName 기준 오름차순 정렬
>> 
>> select * from products order by Price desc;
>> # Price기준 내림차순 정렬
>> 
>> select * from customers order by CustomerName asc, Country desc;
>> # CustomerName기준 오름차순 정렬, Country기준 내림차순 정렬
>> 
>> select * from customers where country = 'UK' LIMIT 3;
>> # Coutry가 UK인것 3개만 출력
>> 
>> select *
>> ,
>> CASE
>> 	when price > 50 then '고'
>>     when price >= 30 then '중'
>>     else '저'
>> end as 'Category'
>> from products;
>> # Category 를 만들고 Price가 50 초과인것 '고', 50이하 30이상 '중', 30 미만 '저'로 설정.
>> 
>> select COUNT(*) as country_count from customers where country = 'France';
>> # country가 France인 것을 Count해서 country_count라는 이름으로 출력
>> 
>> select avg(price) as '평균' from products;
>> #price의 평균을 평균이라는 이름으로 출력.
>> 
>> select sum(Quantity) from order_details;
>> # Quantity합을 출력.
>> 
>> select min(price) from products;
>> # price의 최솟값을 출력
>> 
>> select max(price) from products
>> # price의 최댓값을 출력
>> ```
