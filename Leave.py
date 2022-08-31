'''Megan Perry
Maryville University-SWDV630
Final Project-Summer 2022
Leave Management System-This file is a module, imported by the three drivers (AdminLMS, ApproverLMS, EmployeeLMS).
Contains classes to create leave requests and leave history (and their tables in the database).'''

#import sqlalchemy to set up database and functionality
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import datetime

Base = declarative_base()  #instantiate dec base-global variable to make classes ORM capable

class LeaveRequest(Base):
    def __init__(self, emp_name, leave_requested, units, lv_begin_date, approver):
        self.request_date = str(datetime.datetime.now().strftime("%x"))  #datestamp
        self.name = emp_name
        self.approver = approver
        self.leave_requested = leave_requested
        self.units = units  #hourly emp=hours, salaried emp=days
        self.lv_begin_date = lv_begin_date  #mm/dd/yyyy date that requesting employee wants leave to start on

    __tablename__ = "LeaveRequests"  #create name for table

    #define columns and their data types
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)  #primary key, autoincremented, unique, null not allowed
    request_date = Column(String, nullable=False)
    name = Column(String, nullable=False)
    approver = Column(String, nullable=False)
    leave_requested = Column(Integer, nullable=False)
    units = Column(String, nullable=False)
    lv_begin_date = Column(String, nullable=False)
        
    def __repr__(self):
        return 'Request Date: ' + self.request_date + ' -Employee Name: ' + self.name + ' -Approver: ' + self.approver + ' -Leave Amt Requested: ' + str(self.leave_requested) + ' ' + self.units + ' -Leave Date: ' + self.lv_begin_date


class LeaveHistory(Base):
    def __init__(self, name, posted_by, leave_requested, units, leave_date, status, emp_avail_leave):
        self.post_date = str(datetime.datetime.now().strftime("%x"))  #datestamp
        self.name = name
        self.posted_by = posted_by
        self.leave_requested = leave_requested
        self.units = units  #hourly emp=hours, salaried emp=days
        self.leave_date = leave_date
        self.status = status  #approved/declined/edit
        self.emp_avail_leave = emp_avail_leave

    __tablename__ = "LeaveHistory"  #create name for table

    #define columns and their data types
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)  #primary key, autoincremented, unique, null not allowed
    post_date = Column(String, nullable=False)
    name = Column(String, nullable=False)
    posted_by = Column(String, nullable=False)
    leave_requested = Column(Integer, nullable=False)
    units = Column(String, nullable=False)
    leave_date = Column(String, nullable=False)
    status = Column(String, nullable=False)
    emp_avail_leave = Column(Integer, nullable=False)

    def __repr__(self):
        return 'Post Date: ' + self.post_date + ' -Employee Name: ' + self.name + ' -Posted By: ' + self.posted_by + ' -Leave Amt Requested: ' + str(self.leave_requested) + ' ' + self.units + ' -Leave Date: ' + self.leave_date + ' -Status:' + self.status + ' -Available Leave: ' + str(self.emp_avail_leave)
