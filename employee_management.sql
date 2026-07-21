CREATE DATABASE employee_management;
use employee_management;
CREATE TABLE admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT INTO admin (username, password)VALUES ('admin', 'admin123');

CREATE TABLE department (
    dept_id INT AUTO_INCREMENT PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL UNIQUE
);

INSERT INTO department (dept_name)VALUES('Human Resources'),('Information Technology'),('Finance'),('Marketing'),('Sales');

CREATE TABLE employee (
    emp_id INT AUTO_INCREMENT PRIMARY KEY,
    emp_name VARCHAR(100) NOT NULL,
    gender ENUM('Male','Female','Other'),
    age INT,
    department VARCHAR(100),
    designation VARCHAR(100),
    salary DECIMAL(10,2),
    phone VARCHAR(15),
    email VARCHAR(100),
    address TEXT
);

show tables;

INSERT INTO employee
(emp_name, gender, age, department, designation, salary, phone, email, address)
VALUES
('Rahul Sharma','Male',25,'Information Technology','Software Developer',45000,'9876543210','rahul@gmail.com','Delhi'),
('Priya Singh','Female',27,'Human Resources','HR Manager',55000,'9876543211','priya@gmail.com','Noida'),
('Amit Kumar','Male',30,'Finance','Accountant',50000,'9876543212','amit@gmail.com','Lucknow'),
('Sneha Verma','Female',24,'Marketing','Marketing Executive',42000,'9876543213','sneha@gmail.com','Ghaziabad');

drop table department;
CREATE TABLE department(
    dept_id INT AUTO_INCREMENT PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL
);

INSERT INTO department(dept_name) VALUES('Human Resources'),('Information Technology'),('Finance'),('Marketing'),('Sales');

ALTER TABLE employee ADD created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;