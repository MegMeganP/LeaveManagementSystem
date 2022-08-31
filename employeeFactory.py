'''Megan Perry
Maryville University-SWDV630
Final Project-Summer 2022
Leave Management System-This file is a module, imported by the three drivers (AdminLMS, ApproverLMS, EmployeeLMS).
Contains classes to create leave employees and approvers (and their tables in the database).
This was built upon from the week 4 assignment. Most of the methods were deleted as they were unused in this system, and the drivers handle a lot. 
Most of the Temp functionality is shut down in this system, but shows that there can be more employee types and functions that can be customized'''
#import sqlalchemy to set up database and functionality
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()  #instantiate dec base-global variable to make classes ORM capable


class EmployeeFactory:  #factory-admin will use to create employee without having to know what subclasses etc to call
    def __init__(self, name, emp_type, approver):
        self.name = name
        self.type = emp_type.strip().lower()  #change input to a standard format to use easily
        self.approver = approver

    def create_employee(self):  #depending on admin input, call the correct subclass to create the correct employee type
        if self.type == 'hourly':
            leave_hours = int(input("Enter the amount of initial leave hours (whole number): "))  #whole numbers
            new_employee = HourlyEmployee(self.name, leave_hours, self.approver)
            return new_employee
        elif self.type == 'temp':
            contracted_hours_available = int(input("Enter the amount of hours contracted (whole number): "))
            leave_taken = 0  #temps initialize not having taken any leave yet
            new_employee = TempEmployee(self.name, leave_taken, self.approver, contracted_hours_available)
            return new_employee
        elif self.type == 'salary':
            leave_days = int(input("Enter the amount of initial leave days (whole number): "))  #whole numbers
            new_employee = SalariedEmployee(self.name, leave_days, self.approver)
            return new_employee
        else:
            print("The input is not recognized as a valid employee type")


class Employee:
    def __init__(self, name, leave, approver):
        self.name = name
        self.leave = leave
        self.approver = approver
    
    def __repr__(self):
        return self.name + ' -Leave: ' + str(self.leave) + ' -approver: ' + self.approver
    

class HourlyEmployee(Employee, Base):
    def __init__(self, name, leave_hours, approver):
        super(HourlyEmployee, self).__init__(name, leave_hours, approver)  #hourly employees get hours of leave

    __tablename__ = "HourlyEmployee1"  #create name for table

    #define columns and their data types
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)  #primary key, autoincremented, unique, null not allowed
    name = Column(String, nullable=False)
    leave = Column(Integer)
    approver = Column(String)

#most of the Temp functionality is shut down in drivers (a company could customize and use in the future)
class TempEmployee(Employee, Base):  #most of the Temp functionality is shut down in drivers (a company could customize and use in the future)
    def __init__(self, name, leave_taken, approver, contracted_hours_available):  #Temps don't have leave initialized, but it is approved amt taken is tracked
        self.name = name
        self.leave_taken = 0
        self.approver = approver
        self.contracted_hours_available = contracted_hours_available  #Temp employees have contracts for an amount of hours and duration
        super(TempEmployee, self).__init__(name, leave_taken, approver)  #temp employees don't get paid leave, only unpaid

    __tablename__ = "TempEmployee1"  #create name for table

    #define columns and their data types
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    leave_taken = Column(Integer)
    approver = Column(String)
    contracted_hours_available = Column(Integer)

    def __repr__(self):
        return self.name + ' -Leave taken: ' + str(self.leave_taken) + ' -approver: ' + self.approver + ' Contracted Hours: ' + str(self.contracted_hours_available)


class SalariedEmployee(Employee, Base):
    def __init__(self, name, leave_days, approver):
        super(SalariedEmployee, self).__init__(name, leave_days, approver)

    __tablename__ = "SalaryEmployee1"  #create name for table

    #define columns and their data types
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    leave = Column(Integer)
    approver = Column(String)


'''Approver Class, so that approvers can be tracked (and later can be customized).  Employees have an approver.'''
class Approver(Base):
    def __init__(self, name):
        self.name = name

    __tablename__ = "Approver1"  #create name for table

    #define columns and their data types
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)

    def __repr__(self):
        return "ID: " + str(self.id) + "Name: " + self.name
