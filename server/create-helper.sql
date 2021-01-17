--Create role and database with owner
create role stackoverflow_clone login password 'stackoverflow_clone';
create database stackoverflow_clone with owner stackoverflow_clone;