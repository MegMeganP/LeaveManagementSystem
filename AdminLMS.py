'''Megan Perry
Maryville University-SWDV630
Final Project-Summer 2022
Leave Management System-This file is to run for the Admin functionality.
The main() that is called to run the program is at the bottom of the file.'''

import employeeFactory as E  #import the file with the employee classes and table attributes
import Leave as L
#import sqlalchemy to set up database and functionality
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def add_employee():
    engine = create_engine('sqlite:///emp.db', echo=False)  #create the sqlite database if it doesn't exist, use this one if it exists
    E.Base.metadata.create_all(engine)  #Base knows what engine to use to store our objects

    name = (input("Enter employee name (Firstname Lastname):"))
    emp_type = input("Enter the type of employee to create (hourly, temp, salary): ").lower()  #hourly, temp, salary
    approver = input("Enter the name of employee's leave approver (Firstname Lastname): ")  #new employee's supervisor or manager
    
    new_employee1 = E.EmployeeFactory(name, emp_type, approver).create_employee()
    print()
    print(new_employee1)  #prove that the new employee is created
    print()

    Session = sessionmaker(bind=engine)  #need a session to do SQLAlchemy things, opening connection to database engine where it will store objects, bind engine that we created above
    session = Session()  #intantiate the session object
    session.add(new_employee1)  #add the new created employee to database

    session.commit()  #commit chages to database

    if emp_type=="hourly":
        units="hours"
    if emp_type=="salary":
        units="days"

    if (emp_type == "hourly") or (emp_type == "salary"):
        history_entry = L.LeaveHistory(new_employee1.name, "admin", new_employee1.leave, units, "initial", "initialize", new_employee1.leave)
        print(history_entry)
        session.add(history_entry)
        session.commit()
        print()
    else:
        print("Temp employee leave transactions are not recorded in history- Temp functions are disabled and under construction")


def delete_employee():
    engine = create_engine('sqlite:///emp.db', echo=False)  #create the sqlite database if it doesn't exist, use this one if it exists
    E.Base.metadata.create_all(engine)  #Base knows what engine to use to store our objects
    print("h=hourly, t= temporary, s=salaried")
    emp_type_table = input("Enter the employee type table to delete from (h, t, s): ").lower()

    #Use the table that user chooses
    if emp_type_table =="h":
        emp_type_table = E.HourlyEmployee
    elif emp_type_table =="t":
        emp_type_table = E.TempEmployee
    elif emp_type_table =="s":
        emp_type_table = E.SalariedEmployee
    else:
        print("invalid entry")
        exit()  #exit so that you can start over if you typed the wrong thing

    Session = sessionmaker(bind=engine)  #need a session to do SQLAlchemy things, opening connection to database engine where it will store objects, bind engine that we created above
    session = Session()  #intantiate the session object

    print("List of the chosen employee type with ID's.  ID will be needed to delete.")
    for row in session.query(emp_type_table).all():
        print("ID: ", row.id, " Name: ", row.name)

    print("Warning: Deletes are permanent")
    del_id = int(input("Enter the ID of the employee to delete: "))  #use primary key id

    #query out the employee to delete
    record_to_del = session.query(emp_type_table).filter_by(id=del_id).one()
    
    session.delete(record_to_del)  #delete the queried employee
    session.commit()  #commit changes to database
    print("Record Deleted\n")


def edit_employee():
    engine = create_engine('sqlite:///emp.db', echo=False)  #create the sqlite database if it doesn't exist, use this one if it exists
    E.Base.metadata.create_all(engine)  #Base knows what engine to use to store our objects

    print("h=hourly, t= temporary, s=salaried")
    emp_type_table = input("Enter the employee type table to that has the employee to edit (h, t, s): ").lower()

    #Use the table that user chooses
    if emp_type_table =="h":
        emp_type_table = E.HourlyEmployee
    #elif emp_type_table =="t":
        #emp_type_table = E.TempEmployee  -temp employee functionality disabled/under construction
    elif emp_type_table =="s":
        emp_type_table = E.SalariedEmployee
    else:
        print("invalid entry\n-or if temp employee was chosen: temp employee functionality is disabled/under construction")
        exit()  #exit so that you can start over if you typed the wrong thing

    Session = sessionmaker(bind=engine)  #need a session to do SQLAlchemy things, opening connection to database engine where it will store objects, bind engine that we created above
    session = Session()  #intantiate the session object

    print("List of the chosen employee type with ID's.  ID will be needed to edit.")
    for row in session.query(emp_type_table).all():
            print("ID: ", row.id, " Name: ", row.name, "\n")

    edit_id = int(input("Enter the ID of the employee to edit: "))  #use primary key id

    #query out the employee to edit
    record_to_edit = session.query(emp_type_table).filter_by(id=edit_id).one()
    print(record_to_edit)  #check to make sure this is the record you want to edit
    print()

    print("Warning:  Edits cannot be undone")
    edit_field = input("Enter the field to edit (choose name or approver): ").lower()
    
    if edit_field == "name":
        record_to_edit.name = input("Enter the new name (Firstname Lastname): ")
    
    elif edit_field == "approver":
        record_to_edit.approver = input("Enter the name of the new approver (Firstname Lastname): ")
    
    else:
        print("invalid entry")
        exit()
    
    session.commit()
    print("Edited:", record_to_edit, "\n")

def view_all_employees():
    engine = create_engine('sqlite:///emp.db', echo=False)  #create the sqlite database if it doesn't exist, use this one if it exists
    E.Base.metadata.create_all(engine)  #Base knows what engine to use to store our objects

    Session = sessionmaker(bind=engine)  #need a session to do SQLAlchemy things, opening connection to database engine where it will store objects, bind engine that we created above
    session = Session()  #intantiate the session object

    print("All Employees:")
    print("Hourly")
    for row in session.query(E.HourlyEmployee).all():
        print("ID: ", row.id, " Name: ",row.name, " Leave Hours: ",row.leave," Approver: ", row.approver)
    print("Salaried")
    for row in session.query(E.SalariedEmployee).all():
        print("ID: ", row.id, " Name: ",row.name, " Leave Days: ",row.leave," Approver: ", row.approver)
    print("Temp")
    for row in session.query(E.TempEmployee).all():
        print("ID: ", row.id, " Name: ",row.name, " Leave Taken: ",row.leave_taken," Approver: ", row.approver, " Contracted Hours Available: ", row.contracted_hours_available)


def add_approver():
    engine = create_engine('sqlite:///emp.db', echo=False)  #create the sqlite database if it doesn't exist, use this one if it exists
    E.Base.metadata.create_all(engine)  #Base knows what engine to use to store our objects

    name = (input("Enter approver name (Firstname Lastname):"))
    
    new_approver = E.Approver(name)
    print()
    print(new_approver)  #prove that the new employee is created
    print()

    Session = sessionmaker(bind=engine)  #need a session to do SQLAlchemy things, opening connection to database engine where it will store objects, bind engine that we created above
    session = Session()  #intantiate the session object
    session.add(new_approver)  #add the new created employee to database

    session.commit()  #commit chages to database

    print("List of all approvers: ")

    for row in session.query(E.Approver).all():
        print(row.id, row.name)


def view_emp_history():
    engine = create_engine('sqlite:///emp.db', echo=False)  #create the sqlite database if it doesn't exist, use this one if it exists
    L.Base.metadata.create_all(engine)  #Base knows what engine to use to store our objects

    Session = sessionmaker(bind=engine)  #to do anything in SQL aclhemy for storing objects, need a session, opening connection to database engine where it will store objects binding with the engine that we created above creates like a factory
    session = Session()  #instantiate session object

    hist_name = input("Enter the name of the employee (Firstname Lastname) to view history: ")

    for row in session.query(L.LeaveHistory).filter_by(name=hist_name).all():
        print("ID: ", row.id, "Post Date: ", row.post_date, "Name: ", row.name, "Posted By: ", row.posted_by, "Leave Requested: ", row.leave_requested, row.units, "Leave Date: ", row.leave_date, "Status: ", row.status, "Available Leave: ", row.emp_avail_leave)


def view_all_histories():
    engine = create_engine('sqlite:///emp.db', echo=False)  #create the sqlite database if it doesn't exist, use this one if it exists
    L.Base.metadata.create_all(engine)  #Base knows what engine to use to store our objects

    Session = sessionmaker(bind=engine)  #to do anything in SQL aclhemy for storing objects, need a session, opening connection to database engine where it will store objects binding with the engine that we created above creates like a factory
    session = Session()  #instantiate session object

    print("Leave Transaction History: All Employees--")

    for row in session.query(L.LeaveHistory).all():
        print("ID: ", row.id, "Post Date: ", row.post_date, "Name: ", row.name, "Posted By: ", row.posted_by, "Leave Requested: ", row.leave_requested, row.units, "Leave Date: ", row.leave_date, "Status: ", row.status, "Available Leave: ", row.emp_avail_leave)


def edit_leave():
    engine = create_engine('sqlite:///emp.db', echo=False)  #create the sqlite database if it doesn't exist, use this one if it exists
    L.Base.metadata.create_all(engine)  #Base knows what engine to use to store our objects

    Session = sessionmaker(bind=engine)  #to do anything in SQL aclhemy for storing objects, need a session, opening connection to database engine where it will store objects binding with the engine that we created above creates like a factory
    session = Session()  #instantiate session object

    print("h=hourly, t= temporary, s=salaried")
    emp_type_table = input("Enter the employee type table to that has the employee of the leave that is being edited (h, t, s): ").lower()

    #Use the table that user chooses
    if emp_type_table =="h":
        emp_type_table = E.HourlyEmployee
        units="hours"
    #elif emp_type_table =="t":
        #emp_type_table = E.TempEmployee  -temp employee functionality disabled/under construction
    elif emp_type_table =="s":
        emp_type_table = E.SalariedEmployee
        units="days"
    else:
        print("invalid entry\n-or if temp employee was chosen: temp employee functionality is disabled/under construction")
        exit()  #exit so that you can start over if you typed the wrong thing

    emp_name = input("Enter the employee name (Firstname Lastname) that needs leave edited: ")

    employee = session.query(emp_type_table).filter_by(name=emp_name).first()
    print(employee)
    print()
    add_subtract = input("Add or subtract leave (Enter the word add or subtract): ").lower()
    print("Negative numbers will not work, if amount subtracted equals negative leave, then it will equal zero")
    amt = int(input("Enter amount of leave units to add or subtract from leave (whole, positive number): "))
    
    if amt < 0:  #do not allow negative leave to be added or subtracted
        print("Invalid input-cannot add or subtract negative leave")
        exit()

    if add_subtract == "add":
        employee.leave = employee.leave + amt
    elif add_subtract == "subtract":
        employee.leave = employee.leave - amt
        if employee.leave < 0:  #employee cannot have negative leave in this version
            employee.leave = 0
    else:
        print("invalid input")
    print(session.dirty) #see if there's changes that need to be committed
    session.commit()
    
    print("Employee leave is edited")
   
    history_entry = L.LeaveHistory(employee.name, "admin", amt, units, add_subtract, "edit", employee.leave)
    print(history_entry)
    session.add(history_entry)
    session.commit()

    print("Employee leave edit is posted\n")
    print("History:")
    print(session.query(L.LeaveHistory).filter_by(name=employee.name).all())


#the function that is for the interface

def main():

    print("Hello, Admin!  Welcome to the Leave Management System.")
    print("This is version: Early Prototype2. Keep in mind that there is not a lot of input validation and everything is CASE SENSITIVE.")
    print("For the functionality to work, INPUTS MUST BE TYPED IN CORRECTLY, and future versions would be more forgiving and designed around the company's needs and existing infrastructure.")
    print("In the future, secure logins would be needed for admin functions, in this test version we do not have a login")

    while True:
        action = input("Please enter the action to perform (employee=enter new employee, delete=delete employee, edit=edit employee, print=print all employees, approver=enter new approver, empHist=view employee leave history, allHist=view all histories, changeLeave=edit available leave, q=quit): ").lower()
        
        if action == "employee":  
            add_employee()

        elif action == "delete": 
            delete_employee()

        elif action == "edit":
            edit_employee()

        elif action == "print":
            view_all_employees()

        elif action == "approver":
            add_approver()

        elif action == "emphist":
            view_emp_history()

        elif action == "allhist":
            view_all_histories()
        
        elif action == "changeleave":
            edit_leave()

        elif action == "q":
            exit()

        else:
            print("invalid input")
            exit()

main()
