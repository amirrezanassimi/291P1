import sqlite3
import getpass
import random
import re
import os

connection = None
cursor = None

def connect_to_DB():
    global connection, cursor
  
    path = input("Enter path of database: ")
    check_db = os.path.isfile(path)
    if check_db:
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
        cursor.execute(' PRAGMA forteign_keys=ON; ')
        connection.commit()
        return check_db, path
    else:
        return check_db, path
    

def get_login():
    global connection, cursor

    print("Please enter your login credentials.")
    valid = False
    while (not valid):
        username = input("Username: ")
        password = getpass.getpass()
        if (re.match('^[a-zA-Z0-9]*$', username) and re.match('^[a-zA-Z0-9]*$', password)):
            cursor.execute(" SELECT * FROM users WHERE uid LIKE ? and pwd = ?; ", (username, password)) 
            user = cursor.fetchone()
            if user != None:
                valid = True
            else:
                print("Incorrect username or password. Please try again.")
        else:
            print("Incorrect username or password. Please try again")
            
    connection.commit()
    return user


def display_menu(utype):
    global connection, cursor

    if utype == 'a':
        print("Which task would you like to perform?")
        print("1 - Register a birth")
        print("2 - Register a marriage")
        print("3 - Renew vehicle registration")
        print("4 - Process a bill of sale")
        print("5 - Process a payment")
        print("6 - Get a driver abstract")
        print("0 - Logout")
        valid = False
        
        while (not valid):
            try:
                task = int(input("Enter a number: "))
            except: # user did not enter a number
                print("Please enter a valid option")
            else:
                if (task in range(0,7)): # check if user entered a valid menu option
                    valid = True
                else:
                    print("Please enter a valid option")
    
    elif utype == 'o':
        print("1 - Issue a ticket")
        print("2 - Find a car owner") 
        print("0 - Logout")
        valid = False
        
        while (not valid):
            try:
                task = int(input("Enter a number: "))
            except: # user did not enter a number
                print("Please enter a valid option")
            else:
                if (task in range(0,3)): # check if user entered a valid menu option
                    valid = True
                else:
                    print("Please enter a valid option")
        if task != 0:
            task += 6 # officers options actually correlate to options 7 and 8
    return task

        
def register_birth(user_info):
    global connection, cursor

    os.system('clear')
    print("Birth registry")

    valid = False
    while(not valid):
        reg_no = unique_registration()
        cursor.execute("SELECT * FROM births WHERE regno = ?", (reg_no, ))
        if (not cursor.fetchone()): # check if any other births have the same reg_no
            valid = True

    fname = input("First name: ") 
    lname = input("Last name: ")
    regplace = user_info[5]
    gender = input("Gender: ")

    m_fname = input("Mothers first name: ")
    m_lname = input("Mothers last name: ")
    cursor.execute(" SELECT * FROM persons WHERE fname LIKE ? and lname LIKE ?; ", (m_fname, m_lname)) 
    mother = cursor.fetchone()
    if mother == None:
        print("Mother's name not found in database. Redirecting to register mother...\n")
        insert_person(m_fname, m_lname)



    f_fname = input("Fathers first name: ")
    f_lname = input ("Fathers last name: ")
    cursor.execute(" SELECT * FROM persons WHERE fname LIKE ? and lname LIKE ?; ", (f_fname, f_lname)) 
    father = cursor.fetchone()
    if father == None:
        print("Father's name not found in database. Redirecting to register father...\n")
        insert_person(f_fname, f_lname)
    
    cursor.execute("SELECT address, phone FROM persons WHERE fname LIKE ? AND lname LIKE ?", (m_fname, m_lname))
    mothers_info = cursor.fetchone()
    address = mothers_info[0]
    phone = mothers_info[1]
    bdate = input("Birth date (YYYY-MM-DD): ")
    bplace = input("Birth place: ")
	
    data_person = (fname, lname, bdate, bplace, address, phone)

    cursor.execute("INSERT INTO persons VALUES (?, ?, ?, ? ,?, ?); ", data_person)

    data_birth = (reg_no, fname, lname, regplace, gender, f_fname, f_lname, m_fname, m_lname)
    cursor.execute("INSERT INTO births VALUES (?, ?, ?, date('now'), ?, ?, ?, ?, ?, ? ); ", data_birth)

    connection.commit()

	
	
		   
    
def register_marriage(user_info):
    global connection, cursor

    os.system('clear')
    print("\n Marriage registration.\n")
    valid = False
    while(not valid):
        reg_no = unique_registration()
        cursor.execute("SELECT * FROM births WHERE regno = ?", (reg_no, ))
        if not cursor.fetchone(): # check if any other births have the same reg_no
            valid = True
    p1_fname = input("p1 First name: ")
    p1_lname = input("p1 Last name: ")
    cursor.execute("SELECT * FROM persons WHERE fname LIKE ? AND lname LIKE?", (p1_fname, p1_lname))
    p1_info = cursor.fetchone()
    if p1_info == None:
	    print("Person not found in databse. Redirecting to register...")
	    insert_person(p1_fname, p1_lname)
	
    p2_fname = input("p2 First name: ")
    p2_lname = input("p2 Last name: ")
    cursor.execute("SELECT * FROM persons WHERE fname LIKE ? AND lname LIKE?", (p2_fname, p2_lname))
    p2_info = cursor.fetchone()
    if p2_info == None:
	    print("Person not found in databse. Redirecting to register...")
	    insert_person(p2_fname, p2_lname)
    regplace = user_info[5]
    data = (reg_no, regplace, p1_fname, p1_lname, p2_fname, p2_lname)
	
    cursor.execute("INSERT INTO marriages VALUES (?, date('now'), ?, ?, ?, ?, ?); ", data)
    connection.commit()
	
def renew_reg():
    global connection, cursor

    os.system('clear')

    valid = False
    while(not valid):
        reg_no = input("Enter an existing registration number: ")
        cursor.execute("SELECT * from registrations WHERE regno = ?", (reg_no, ))
        if(cursor.fetchone()):
            valid = True
        else:
            print("Registration number does not exist.\n")

    cursor.execute("SELECT * FROM registrations WHERE regno = ? and expiry <= date('now');",(reg_no, ))
    regData = cursor.fetchone()

    if regData is not None:
        cursor.execute("UPDATE registrations SET expiry=date('now','+1 year') where regno=?;", (reg_no, ))
    else:
        cursor.execute("UPDATE registrations SET expiry = date(expiry, '+1 year') where regno = ?;", (reg_no, ))

    connection.commit()
    return

def bill_of_sale():
    os.system('clear')
    
    print("Process a bill of sale ")
   
    vin =  input("\nenter  VIN: ")
    cursor.execute("SELECT * FROM registrations WHERE vin = ? ;" , (vin,))
    if not cursor.fetchone():

        print("\nVIN doesn't exist or didn't entered!" )
        print("\nTry aging (press 1)")
        print("exit (press 2)")
        print("main menu (press3)")
 
        valid = False
        while (not valid):
            try:
                choice = int(input("\nEnter a number: "))
            except: 
                print("Please enter a valid option")
            else:
                if(choice in range(1,4)):  
                    if(choice == 1):
                        bill_of_sale()
                    elif (choice == 2):
                        exit()
                    elif (choice == 3):
                        main()
                    elif (choice == None):
                        return
                else:
                        print("Number entered is not valid, Try again!")
                 
    current_owner_fname = input("enter current owner first name: ")
    cursor.execute("SELECT fname FROM registrations WHERE fname =? ;",(current_owner_fname, ))
    if not cursor.fetchone():

        print("\nFirst Name doesn't exist or didn't entered!" )
        print("\nTry aging (press 1)")
        print("exit (press 2)")
        print("main menu (press3)")
 
        valid = False
        while (not valid):
            try:
                choice = int(input("\nEnter a number: "))
            except: 
                print("Please enter a valid option")
            else:
                if(choice in range(1,4)):  
                    if(choice == 1):
                        bill_of_sale()
                    elif (choice == 2):
                        exit()
                    elif (choice == 3):
                        main()
                    elif (choice == None):
                        return
                else:
                        print("Number entered is not valid, Try again!")

    current_owner_lname = input("enter current owner last name: ")
    cursor.execute("SELECT lname FROM registrations WHERE lname =? ;" , (current_owner_lname, ))
    if not cursor.fetchone():

        print("\nLast Name doesn't exist or didn't entered!" )
        print("\nTry aging (press 1)")
        print("exit (press 2)")
        print("main menu (press3)")
 
        valid = False
        while (not valid):
            try:
                choice = int(input("\nEnter a number: "))
            except: 
                print("Please enter a valid option")
            else:
                if(choice in range(1,4)):  
                    if(choice == 1):
                        bill_of_sale()
                    elif (choice == 2):
                        exit()
                    elif (choice == 3):
                        main()
                    elif (choice == None):
                        return
                else:
                        print("Number entered is not valid, Try again!")
        
    cursor.execute("SELECT * FROM registrations WHERE vin =? AND fname =? AND lname = ? AND expiry < date('now');",(vin,current_owner_fname,current_owner_lname))
    reg_info = cursor.fetchone()
    if isinstance(reg_info, type(None)): 
        print("\n",current_owner_fname," ",current_owner_lname, "is not the most recent owner")

       
        print("\nTry aging (press 1)")
        print("exit (press 2)")
        print("main menu (press3)")
        valid = False
        while (not valid):
            try:
                choice = int(input("\nEnter a number: "))
            except: 
                print("Please enter a valid option")
            else:
                if(choice in range(1,4)):  
                    if(choice == 1):
                        bill_of_sale()
                    elif (choice == 2):
                        exit()
                    elif (choice == 3):
                        main()
                    elif (choice == None):
                        return
                else:
                        print("Number entered is not valid, Try again!")
     
    new_owner_fname = input("enter new owner first name: ")
    new_owner_lname = input("enter new owner last name: ")
    new_plate = input("enter new plate number: ")
        
    new_reg_nu = unique_registration()
    new_reg = (new_reg_nu, new_plate, vin, new_owner_fname, new_owner_lname )
    cursor.execute("INSERT INTO registrations VALUES (?, date('now'), date('now','+1 year'),?,?,?,?) ;", (new_reg))
    cursor.execute("UPDATE registrations SET expiry = date('now') WHERE regno = ? AND fname = ? AND lname = ?;",(reg_info[0], reg_info[5], reg_info[6]))
    print("Transfer completed sucessfully!")
    connection.commit()
    return

def process_payment():
    global connection, cursor

    os.system('clear')

    valid = False
    while(not valid):
        tick_no = input("Enter a ticket number: ")
        cursor.execute("SELECT fine FROM tickets WHERE tno = ?;", (tick_no, ))
        fine = cursor.fetchone()
        if fine is not None:
            valid = True
        else:
            print("Ticket number not found\n")
    fine = fine[0]
    cursor.execute("SELECT SUM(amount) FROM payments WHERE tno = ?;", (tick_no, ))
    sumPayments = cursor.fetchone()
    sumPayments = sumPayments[0]
    if sumPayments is None:
        sumPayments = 0
    valid = False
    while(not valid):
        amount = int(input("Enter payment amount (integer): "))
        if ((sumPayments + amount) <= fine):
            valid = True
        else:
            print("Amount exceeds ticket fine.")
    data = (tick_no, amount)
    cursor.execute("INSERT INTO payments VALUES (?, date('now'), ?);", data)
    
    connection.commit()
    return

def get_driver_abstract():
    global connection, cursor

    os.system('clear')

    fname = input("Enter first name: ")
    lname = input("Enter last name: ")
    
    pass

def issue_ticket():
    global connection, cursor

    os.system('clear')

    reg_no = input("Enter a registration number: ")
    cursor.execute("SELECT fname, lname, make, model, year, color FROM vehicles, registrations WHERE registrations.vin = vehicles.vin AND regno = ?;", (reg_no, ))
    reg_info = cursor.fetchone()
    print("\nName: {} {}\nMake: {}\nModel: {}\nYear: {}\nColor: {}".format(reg_info[0],reg_info[1],reg_info[2],reg_info[3],reg_info[4], reg_info[5]))

    date = input("Enter date of violation: ")
    desc = input("Enter violation description: ")
    amount = input("Enter fine amount: ")
    tno = unique_registration()

    if (date == ''):
        data = (tno, reg_no, amount, desc)
        cursor.execute("INSERT INTO tickets VALUES (?, ?, ?, ?, date('now')); ", data)
    else:
        data = (tno, reg_no, amount, desc, date)
        cursor.execute("INSERT INTO tickets VALUES (?, ?, ?, ?, ?); ", data)
    
    connection.commit()
    return

def find_car_owner():
    pass

def unique_registration():
	return random.randint(0,9999)

def insert_person(fname = None, lname = None):
    print("Registering a person")

    if(fname is not None):
        print("First name: {}".format(fname))
    else:
        fname = input("First name: ") # get fname if it is not provided

    if(lname is not None):
        print("Last name: {}".format(lname))
    else:   
        lname = input("Last name: ") # get lname if it is not provided

    bdate = input("Birth date: ")
    bplace = input("Birth place: ")
    address = input("Address: ")
    phone = input("Phone: ")

    data = [fname, lname, bdate, bplace, address, phone]

    for i in range(2, len(data)):
        if data[i] == '':
            data[i] = None

    cursor.execute("INSERT INTO persons VALUES (?, ?, ?, ?, ?, ?);", data)

    cursor.execute("SELECT * FROM persons WHERE fname = ? AND lname = ?", (fname, lname))
    check = cursor.fetchone()
    if check != None:
        print(fname + ' ' + lname + ' successfuly registered.\n')

    connection.commit()

def main():
    global connection, cursor
    
    db_connection = False
    while not db_connection:
        db_connection, path = connect_to_DB()
        while db_connection:
            os.system('clear')
            print("Sucessfully connected to database: " + path + "\n")
            user = get_login()
            logout = False
            while not logout:
                os.system('clear')
                print("Welcome " + user[3] + ".\n")
                task = display_menu(user[2])
                if task == 1:
                    register_birth(user)
                elif task == 2:
                    register_marriage(user)
                elif task == 3:
                    renew_reg()
                elif task == 4:
                    bill_of_sale()
                elif task == 5:
                    process_payment()
                elif task == 6:
                    get_driver_abstract()
                elif task == 7:
                    issue_ticket()
                elif task == 8:
                    find_car_owner()
                elif task == 0:
                    logout = True
        else:
            ans = input("Unable to connect to the specified database. Would you like to try again? (Y for yes, N to exit) ")
            if ans == 'N':
                exit()
            else:
                os.system('clear')


if __name__ == "__main__":
    main()
