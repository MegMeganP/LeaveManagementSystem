'''Megan Perry
Maryville University-SWDV630
Final Project-Summer 2022
Leave Management System-This file is to run for Approver functionality.
The main() that is called to run the program is at the bottom of the file.'''

import employeeFactory as E  #import the file with the employee classes and table attributes
import Leave as L
#import sqlalchemy to set up database and functionality
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def fake_login():
    engine = create_engine('sqlite:///emp.db', echo=False)  #create the sqlite database if it doesn't exist, use this one if it exists
    L.Base.metadata.create_all(engine)  #Base knows what engine to use to store our objects

    Session = sessionmaker(bind=engine)  #to do anything in SQL alchemy for storing objects, need a session, opening connection to database engine where it will store objects binding with the engine that we created above creates like a factory
    session = Session()  #instantiate an object from this factory

    for row in session.query(E.Approver).all():
        print(row.id, row.name)
    approver_id = input("Enter the ID of the approver that you are going to be for this session: ")
    test_approver = session.query(E.Approver).filter_by(id=approver_id).first()

    return test_approver


def view_approver_pending_requests(approver):
    engine = create_engine('sqlite:///emp.db', echo=False)  #create the sqlite database if it doesn't exist, use this one if it exists
    L.Base.metadata.create_all(engine)  #Base knows what engine to use to store our objects

    Session = sessionmaker(bind=engine)  #to do anything in SQL alchemy for storing objects, need a session, opening connection to database engine where it will store objects binding with the engine that we created above creates like a factory
    session = Session()  #instantiate an object from this factory


    print("Your pending requests: ")
    for row in session.query(L.LeaveRequest).filter_by(approver=approver.name).all():
        print("ID: ", row.id,"Request Submit Date: ", row.request_date," Name: ", row.name, " Approver: ", row.approver, " Leave Amt Requested: ", row.leave_requested, row.units, " Leave Date: ", row.lv_begin_date)


def process_request(approver):
    engine = create_engine('sqlite:///emp.db', echo=False)  #create the sqlite database if it doesn't exist, use this one if it exists
    L.Base.metadata.create_all(engine)  #Base knows what engine to use to store our objects

    Session = sessionmaker(bind=engine)  #to do anything in SQL alchemy for storing objects, need a session, opening connection to database engine where it will store objects binding with the engine that we created above creates like a factory
    session = Session()  #instantiate an object from this factory

    view_approver_pending_requests(approver)

    print("If there are no requests to process, press q to quit")
    request_id = input("Enter the ID of the request to process (enter ID or q to quit): ")
    print()
    
    if request_id == "q":
        quit()

    request = session.query(L.LeaveRequest).filter_by(id=request_id).first()
    print(request)

    action = input("Enter action for this request (approve=approve request, decline=decline request, quit=no action and quit): ")

    if action == "approve":
        approve_request(request)

    elif action == "decline":
        decline_request(request)
    else:
        print("quit, or invalid entry-exiting LMS...")
        exit()

def approve_request(request):
    engine = create_engine('sqlite:///emp.db', echo=False)  #create the sqlite database if it doesn't exist, use this one if it exists
    L.Base.metadata.create_all(engine)  #Base knows what engine to use to store our objects

    Session = sessionmaker(bind=engine)  #to do anything in SQL aclhemy for storing objects, need a session, opening connection to database engine where it will store objects
    session = Session()  #instantiate an object from this factory

    #use the request info to find the employee and type
    if request.units == "hours":
        emp_table_type = E.HourlyEmployee
    if request.units == "days":
        emp_table_type = E.SalariedEmployee

    employee = session.query(emp_table_type).filter_by(name=request.name).first()
    print("Request belongs to: ",employee)

    employee.leave = employee.leave - request.leave_requested  #when request is approved, leave is subtracted from available leave
    print(session.dirty)  #do you have dirty data is there something that needs to be committed to database
    session.commit()

    print(employee)

    #record the request approved transaction in the leave history
    history_entry = L.LeaveHistory(request.name, request.approver, request.leave_requested, request.units, request.lv_begin_date, "approved", employee.leave)
    print(history_entry)
    session.add(history_entry)
    session.commit()
    print("Request has been approved and recorded in leave history")

    request3 = session.query(L.LeaveRequest).filter_by(id=request.id).first()  #need to make another object to avoid attaching that request to multiple sessions and erroring out

    session.delete(request3)  #delete the request from the pending request table
    session.commit()

def decline_request(request):
    engine = create_engine('sqlite:///emp.db', echo=False)  #create the sqlite database if it doesn't exist, use this one if it exists
    L.Base.metadata.create_all(engine)  #Base knows what engine to use to store our objects

    Session = sessionmaker(bind=engine)  #to do anything in SQL aclhemy for storing objects, need a session, opening connection to database engine where it will store objects
    session = Session()  #instantiate an object from this factory

    #use the request info to find the employee and type-need employee info for leave calculations
    if request.units == "hours":
        emp_table_type = E.HourlyEmployee
    if request.units == "days":
        emp_table_type = E.SalariedEmployee

    employee = session.query(emp_table_type).filter_by(name=request.name).first()
    print("Request belongs to: ",employee)


    employee.leave = employee.leave - 0  #when request is declined, subtract 0
    print(session.dirty)  #do you have dirty data is there something that needs to be committed to database
    session.commit()

    employee = session.query(emp_table_type).filter_by(name=request.name).first()
    print("Request belongs to: ",employee)

    #record declined request in history, does not add or subtract any leave
    history_entry = L.LeaveHistory(request.name, request.approver, request.leave_requested, request.units, request.lv_begin_date, "declined", employee.leave)
    print(history_entry)
    session.add(history_entry)
    session.commit()
    print("Declined leave request recorded in leave history")

    request2 = session.query(L.LeaveRequest).filter_by(id=request.id).first()  #need to make another object to avoid attaching that request to multiple sessions and erroring out

    session.delete(request2)  #delete request from pending request table
    session.commit()


def view_history(approver):
    engine = create_engine('sqlite:///emp.db', echo=False)  #create the sqlite database if it doesn't exist, use this one if it exists
    L.Base.metadata.create_all(engine)  #Base knows what engine to use to store our objects

    Session = sessionmaker(bind=engine)  #to do anything in SQL aclhemy for storing objects, need a session, opening connection to database engine where it will store objects binding with the engine that we created above creates like a factory
    session = Session()  #instantiate an object from this factory

    print("List of your employees:")
    print(get_approver_employees(approver), "\n")

    emp_name = input("Enter name (Firstname Lastname) of your employee's leave history to view: ")

    for row in session.query(L.LeaveHistory).filter_by(name=emp_name).all():
        print("ID: ", row.id, "Post Date: ", row.post_date, "Name: ", row.name, "Posted By: ", row.posted_by, "Leave Requested: ", row.leave_requested, row.units, "Leave Date: ", row.leave_date, "Status: ", row.status, "Available Leave: ", row.emp_avail_leave, "\n")


def get_approver_employees(approver):
    engine = create_engine('sqlite:///emp.db', echo=False)  #create the sqlite database if it doesn't exist, use this one if it exists
    L.Base.metadata.create_all(engine)  #Base knows what engine to use to store our objects

    Session = sessionmaker(bind=engine)  #to do anything in SQL aclhemy for storing objects, need a session, opening connection to database engine where it will store objects binding with the engine that we created above creates like a factory
    session = Session()  #instantiate an object from this factory

    employees = []  #list to hold the employees that get queried

    #query both employee tables
    for row in session.query(E.HourlyEmployee).filter_by(approver=approver.name).all():
        employees.append(row.name)
    for row in session.query(E.SalariedEmployee).filter_by(approver=approver.name).all():
        employees.append(row.name)
    
    return employees

def main():
    
    print("Hello, Approver!  Welcome to the Leave Management System.")
    print("This is version: Early Prototype2. Keep in mind that there is not a lot of input validation and everything is CASE SENSITIVE.")
    print("For the functionality to work, INPUTS MUST BE TYPED IN CORRECTLY, and future versions would be more forgiving and designed around the company's needs and existing infrastructure.\n")
    print("\nFuture versions would use a login for the approver to reach their LMS account.  Since this is a test prototype, an approver list will be printed and an approver can be chosen off of the list")

    approver = fake_login()

    print("Hello,", approver.name, "!\n")

    print("Pending requests:")
    view_approver_pending_requests(approver)

    while True:
        action = input("\nPlease enter the action to perform (process=process request, history=view an employee leave history, requests=view pending requests, list=view approver employees, q=quit): ").lower()

        if action == "q":
            exit()
        
        elif action == "process":
            process_request(approver)

        elif action =="history":
            view_history(approver)

        elif action == "requests":
            view_approver_pending_requests(approver)

        elif action == "list":
            print("Your employee list: ")
            print(get_approver_employees(approver))
main()