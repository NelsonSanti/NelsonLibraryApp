-- create database nelsonLibrary;
use nelsonLibrary;

drop table if exists books;
create table books(
book_id int primary key auto_increment,
book_name varchar(50),
book_author varchar(50),
book_page varchar(50),
book_language varchar(50),
book_status int default 0
);

drop table if exists members;
create table members(
member_id int primary key auto_increment,
member_name varchar(50),
member_phone varchar(50)
);

drop table if exists borrows;
create table borrows(
borrow_id int primary key auto_increment,
bbook_id varchar(50), #not int because i will put the number and the name of the book
bmember_id varchar(50) #not int because i will put the member number and the member name as well
);



