## Overview and User Guide

### Overview
The following application is used to connect to a SQLite3 database storing enterprise data. Users with valid login credentials will be able provided access to various functions to interact with and update the database, depending on their user type (agents or officers). The application runs through simple command line interfaces. *See User Guide*.

### User Guide
To launch the application, run the following command from the directory holding the source code:
```
$ python3 db.py
```
To connect to a database, enter the path to the database when prompted:
```
Enter path of database: path/to/database.db
```
If the database connection is successfuly established, the user will be prompted to enter their username and password:
```
Username: admin123
Password: pwd12345
```
Depending in the user type (agent or officer), numerical options will appear on screen. Enter the number of the task you wish to perform, and follow the on-screen instructions. For further information regarding the options, see *Software Design*.

## Software Design

Major functions of the application

## Testing Strategy



## Group Work Breakdown
October 21 - Harrison and Dalton: created meanus and functions for valid user login

October 23 - Harrison and Dalton: created register_birth function with basic error checks and register person function; password no longer appears when typed in   
