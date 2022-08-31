'''Megan Perry
Maryville University-SWDV630
Final Project-Summer 2022
Leave Management System-This file to run for Admin functionality.
The main() that is called to run the program is at the bottom of the file.'''

import employeeFactory as E  #import the file with the employee classes and table attributes
import Leave as L
#import sqlalchemy to set up database and functionality
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def fake_login(emp_type_table):
    engine = create_engine('sqlite:///emp.db', echo=False)  #create the sqlite database if it doesn't exist, use this one if it exists
    L.Base.metadata.create_all(engine)  #Base knows what engine to use to store our objects

    Session = sessionmaker(bind=engine)  #to do anything in SQL alchemy for storing objects, need a session, opening connection to database engine where it will store objects binding with the engine that we created above creates like a factory
    session = Session()  #instantiate an object from this factory

    #emp_type_table passed in from input in main() so we can use that info later
    if emp_type_table =="h":
        emp_type_table = E.HourlyEmployee
    #elif emp_type_table =="t":
        #emp_type_table = E.TempEmployee  -temp employee functionality disabled/under construction
    elif emp_type_table =="s":
        emp_type_table = E.SalariedEmployee
    else:
        print("invalid entry\n-or if temp employee was chosen: temp employee functionality is disabled/under construction")
        exit()  #exit so that you can start over if you typed the wrong thing

    print()
    for row in session.query(emp_type_table).all():
        print(row.id, row.name)

    emp_id = input("Enter the ID of the employee that you are going to be for this session: ")

    test_employee = session.query(emp_type_table).filter_by(id=emp_id).first()

    return test_employee
    
    
def submit_leave_request(employee, units):
    engine = create_engine('sqlite:///emp.db', echo=False)  #create the sqlite database if it doesn't exist, use this one if it exists
    L.Base.metadata.create_all(engine)  #Base knows what engine to use to store our objects

    Session = sessionmaker(bind=engine)  #to do anything in SQL alchemy for storing objects, need a session, opening connection to database engine where it will store objects binding with the engine that we created above creates like a factory
    session = Session()  #instantiate an object from this factory

    leave_amt_requested = int(input("Enter amount of leave requesting to take (whole, positive number): "))
    if leave_amt_requested < 0:  #Do not allow negative amount requests-since that would change to addingleave!
        print("Requesting negative leave not allowed-defaulting to 0")
        leave_amt_requested = 0

    leave_date = input("Enter the date that leave will be taken-or beginning date if it is multiple days (format: mm/dd/yyyy): ")

    request = L.LeaveRequest(employee.name, leave_amt_requested, units, leave_date, employee.approver)
    print(request)

    session.add(request)
    session.commit()
    print("Your request has been submitted")
    print()
    print("Your pending requests: ")
    for row in session.query(L.LeaveRequest).filter_by(name=employee.name).all():
        print("ID: ", row.id,"Request Submit Date: ", row.request_date," Name: ", row.name, " Approver: ", row.approver, " Leave Amt Requested: ", row.leave_requested, units, " Leave Date: ", row.lv_begin_date, "\n")


def cancel_pending_request(employee, units):
    engine = create_engine('sqlite:///emp.db', echo=False)  #create the sqlite database if it doesn't exist, use this one if it exists
    L.Base.metadata.create_all(engine)  #Base knows what engine to use to store our objects

    Session = sessionmaker(bind=engine)  #to do anything in SQL alchemy for storing objects, need a session, opening connection to database engine where it will store objects binding with the engine that we created above creates like a factory
    session = Session()  #instantiate an object from this factory

    print("Your pending requests: ")
    for row in session.query(L.LeaveRequest).filter_by(name=employee.name).all():
        print("ID: ", row.id,"Request Submit Date: ", row.request_date," Name: ", row.name, " Approver: ", row.approver, " Leave Amt Requested: ", row.leave_requested, units, " Leave Date: ", row.lv_begin_date, "\n")

    print("\nWarning-deletes cannot be undone!")
    cancel_id = input("Enter the ID of the pending request that you would like to cancel: ")

    record_to_delete = session.query(L.LeaveRequest).filter_by(id=cancel_id).first()
    session.delete(record_to_delete)
    session.commit()

    print("Pending request deleted")


def view_pending_requests(employee, units):
    engine = create_engine('sqlite:///emp.db', echo=False)  #create the sqlite database if it doesn't exist, use this one if it exists
    L.Base.metadata.create_all(engine)  #Base knows what engine to use to store our objects

    Session = sessionmaker(bind=engine)  #to do anything in SQL alchemy for storing objects, need a session, opening connection to database engine where it will store objects binding with the engine that we created above creates like a factory
    session = Session()  #instantiate an object from this factory


    print("Your pending requests: ")
    for row in session.query(L.LeaveRequest).filter_by(name=employee.name).all():
        print("ID: ", row.id,"Request Submit Date: ", row.request_date," Name: ", row.name, " Approver: ", row.approver, " Leave Amt Requested: ", row.leave_requested, units, " Leave Date: ", row.lv_begin_date, "\n")
        

def view_history(employee):
    engine = create_engine('sqlite:///emp.db', echo=False)  #create the sqlite database if it doesn't exist, use this one if it exists
    L.Base.metadata.create_all(engine)  #Base knows what engine to use to store our objects

    Session = sessionmaker(bind=engine)  #to do anything in SQL aclhemy for storing objects, need a session, opening connection to database engine where it will store objects binding with the engine that we created above creates like a factory
    session = Session()  #instantiate an object from this factory

    for row in session.query(L.LeaveHistory).filter_by(name=employee.name).all():
        print("ID: ", row.id, "Post Date: ", row.post_date, "Name: ", row.name, "Posted By: ", row.posted_by, "Leave Requested: ", row.leave_requested, row.units, "Leave Date: ", row.leave_date, "Status: ", row.status, "Available Leave: ", row.emp_avail_leave, "\n")



def main():
    
    print("Hello, Employee!  Welcome to the Leave Management System.")
    print("This is version: Early Prototype2. Keep in mind that there is not a lot of input validation and everything is CASE SENSITIVE.")
    print("For the functionality to work, INPUTS MUST BE TYPED IN CORRECTLY, and future versions would be more forgiving and designed around the company's needs and existing infrastructure.")
    print("\nFuture versions would use a login for the employee to reach their LMS account.  Since this is a test prototype, an employee list will be printed and an employee can be chosen off of the list")

    emp_type_table = input("\nChoose employee type (h=hourly or s=salary): ")
    employee = fake_login(emp_type_table)
    #use type input to create units for some of the outputs/displays
    if emp_type_table =="h":
        units="hours"
    #elif emp_type_table =="t":
        #emp_type_table = E.TempEmployee  -temp employee functionality disabled/under construction
    elif emp_type_table =="s":
        units="days"
    else:
        print("invalid entry\n-or if temp employee was chosen: temp employee functionality is disabled/under construction")
        exit()  #exit so that you can start over if you typed the wrong thing

    print("\nHello,", employee.name, "!")
    print("Available leave:", employee.leave, units, "\n")

    while True:
        
        action = input("\nPlease enter the action to perform (request=submit leave request, pending=view pending requests, cancel=cancel pending request, history=view leave transaction history, q=quit): ").lower()

        if action == "q":
            exit()
        
        elif action == "request":
            submit_leave_request(employee, units)

        elif action == "pending":
            view_pending_requests(employee, units)

        elif action == "cancel":
            cancel_pending_request(employee, units)

        elif action == "history":
            view_history(employee)
        
        else:
            print("invalid entry")

main()
