# BillApp

## DATABASE
- First you need to create a database on your local host or server using this name **bills_system**
  ```
  create database bills_system; # Only this name should be used in the database

## Dockerfile

If you create a Docker image, change the variable values on **Dockerfile** first

- Database UserName
  ```
  ENV DB_USE="root"
  ```
- Database Password
  ```
  ENV DB_PASS="02136"
  ```
- Database Hostname (or) IP Address
  ```
  ENV HOST_NAME="34.27.144.61"
  ```
