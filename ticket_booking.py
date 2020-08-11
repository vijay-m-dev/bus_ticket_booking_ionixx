#importing cx_oracle
import cx_Oracle
#Making connection
con=cx_Oracle.connect("system/needforspeed@127.0.0.1/XE")
#creating cursor
cur=con.cursor()
#Class for bus details
class bus():
    def __init__(self,bus_name,from_loc,to_loc,total_seat,price):
        self.bus_name=bus_name
        self.from_loc=from_loc
        self.to_loc=to_loc
        self.total_seat=total_seat
        self.price=price
    def getbus_name(self):
        return self.bus_name
    def getfrom_loc(self):
        return self.from_loc
    def getto_loc(self):
        return self.to_loc
    def gettotal_seat(self):
        return self.total_seat
    def getprice(self):
        return self.price
    def setbus_name(self,bus_name):
        self.bus_name=bus_name
    def setfrom_loc(self,from_loc):
        self.from_loc=from_loc
    def setto_loc(self,to_loc):
        self.to_loc=to_loc
    def settotal_seat(self,total_seat):
        self.total_seat=total_seat
    def setprice(self,price):
        self.price=price
# Class for agent details
class agent():
    def __init__(self,agent_name,mobile_no,password):
        self.agent_name=agent_name
        self.mobile_no=mobile_no
        self.password=password
    def getagent_name(self):
        return self.agent_name
    def getmobile_no(self):
        return self.mobile_no
    def getpassword(self):
        return self.password
    def setagent_name(self,agent_name):
        self.agent_name=agent_name
    def setmobile_no(self,mobile_no):
        self.mobile_no=mobile_no
    def setpassword(self,password):
        self.password=password
# Class for booked details
class latest_booked_tickets():
    def __init__(self,agent_id,bus_id,total_tickets,total_fare):
        self.agent_id=agent_id
        self.bus_id=bus_id
        self.total_tickets=total_tickets
        self.total_fare=total_fare
    def getagent_id(self):
        return self.agent_id
    def getbus_id(self):
        return self.bus_id
    def gettotal_tickets(self):
        return self.total_tickets
    def gettotal_fare(self):
        return self.total_fare
    def setagent_id(self,agent_id):
        self.agent_id=agent_id
    def setbus_id(self,bus_id):
        self.bus_id=bus_id
    def settotal_tickets(self,total_tickets):
        self.total_tickets=total_tickets
    def settotal_fare(self,total_fare):
        self.total_fare=total_fare

'''Below are the queries to drop the created tables and sequences.For the first time of the program execution,it can be remained commented. Kindly, when executing the program after first time please uncomment the
 below 6 lines dropping queries to uncomment. so, that the tables created in the previous execution will be dropped. Otherwise,it will show error'''
cur.execute("""drop table Latest_booked_tickets""")
cur.execute("""drop table  Bus""")
cur.execute("""drop table Agent""")
cur.execute("""drop sequence seq11""")
cur.execute("""drop sequence seq22""")
cur.execute("""drop sequence seq33""")

# These are the sequences used in each table for their id's
cur.execute("""create sequence seq11 increment by 1 start with 1 minvalue 1 maxvalue 100 nocycle """)
cur.execute("""create sequence seq22 increment by 1 start with 1 minvalue 1 maxvalue 100 nocycle """)
cur.execute("""create sequence seq33 increment by 1 start with 1 minvalue 1 maxvalue 100 nocycle """)

#These are the queries to create the tables
cur.execute("""create table Bus(Bus_name varchar2(30),from_loc varchar2(30),to_loc varchar2(30),total_seat number(10),price number(10),bus_id number(10) primary key)""")
cur.execute("""create table Agent(agent_name varchar2(30),mobile_no number(10),password varchar2(30),agent_code number(10) primary key)""")
cur.execute("""create table Latest_booked_tickets (booking_id number primary key,agent_id number references Agent(agent_code),bus_id number references Bus(bus_id),total_tickets number(10),total_fare number(10))""")

#These are the procedures to insert the data in tables
cur.execute("""create or replace procedure bus_insert
    (bus_name in varchar2,from_loc in varchar2,to_loc in varchar2,total_seat in number,price in number)
    is
    begin
    insert into Bus values(bus_name,from_loc,to_loc,total_seat,price,seq11.nextval);
    commit;
    end;
""")
cur.execute("""create or replace procedure agent_insert
    (agent_name in varchar2,mobile_no in number,password in varchar2)
    is
    begin
    insert into Agent values(agent_name,mobile_no,password,seq22.nextval);
    commit;
    end;
""")
cur.execute("""create or replace procedure booking_insert
    (agent_id in number,bus_id in number,total_tickets in number,total_fare number)
    is
    begin
    insert into Latest_booked_tickets values(seq33.nextval,agent_id,bus_id,total_tickets,total_fare);
    commit;
    end;
""")

#This is the procedure to update the number of tickets available after each agent booked tickets.
cur.execute("""create or replace procedure update_bus
    (bus_id1 in number,tickets in number)
    is
    begin
    update bus set total_seat=total_seat-tickets where bus_id=bus_id1;
    commit;
    end;
""")

while(1):
    print("1.Admin Login\n2.Agent Login\n3.Exit")
    t=int(input())
    #Below block is for admin operations
    if t==1:
        #Admin name and password is set to 'admin'
        username1="admin"
        password1="admin"
        print("Enter admin username:")
        username=input()
        print("Enter password:")
        password=input()
        #Checks the condition for admin username and password
        if username==username1 and password==password1:
            while(1):
                print("1.Add bus\n2.Add Agent\n3.Logout")
                tt=int(input())
                #Below block is for adding bus details
                if tt==1:
                    #Getting details for bus
                    print("Enter Bus details")
                    print("Enter bus name:")
                    bus_name=input()
                    print("Enter from place:")
                    bus_from=input()
                    print("Enter to place:")
                    bus_to=input()
                    print("Enter total seats:")
                    bus_seats=int(input())
                    print("Enter price:")
                    bus_price=int(input())
                    #Creating object for bus
                    bus_object=bus(bus_name,bus_from,bus_to,bus_seats,bus_price)
                    bus_list=[bus_object.getbus_name(),bus_object.getfrom_loc(),bus_object.getto_loc(),bus_object.gettotal_seat(),bus_object.getprice()]
                    #Calling procedure to insert the details of bus 
                    cur.callproc('bus_insert',bus_list)
                    #Fetching the details of all bus and displaying
                    cur.execute(""" select * from Bus""")
                    for i in cur.fetchall():
                        print(i)
                #Below block is for adding agent details
                elif tt==2:
                    #Getting details of agent
                    print("Enter Agent details")
                    print("Enter agent name:")
                    agent_name=input()
                    print("Enter mobile number:")
                    agent_mobile=int(input())
                    print("Enter password:")
                    agent_password=input()
                    #Creating object for agent
                    agent_object=agent(agent_name,agent_mobile,agent_password)
                    agent_list=[agent_object.getagent_name(),agent_object.getmobile_no(),agent_object.getpassword()]
                    #Calling procedure for inserting the agent details
                    cur.callproc('agent_insert',agent_list)
                    #Fetching the details of all agents and displaying
                    cur.execute(""" select * from Agent""")
                    for i in cur.fetchall():
                        print(i)
                #if any other value given,it will be logged out
                elif tt==3:
                    print("Logged Out")
                    break
                else:
                    print("Please Enter valid number")
        else:
            print("Wrong password")
    #This block is for agent operations
    elif t==2:
        #Getting agent code and password
        print("Enter Agent Code:")
        agent_code=int(input())
        print("Enter Agent password:")
        agent_password=input()
        #Checking for agent code and password
        cur.execute("select password from Agent where agent_code={}".format(agent_code,))
        allowed=0
        for i in cur.fetchall():
            if agent_password in i:
                allowed=1
                break
        #Below block is executed,if agent code and password matched
        if allowed==1:
            while(1):
                print("1.List the Bus details\n2.Book Ticket\n3.Show my booking\n4.Logout")
                ttt=int(input())
                #Below block displays the details of the buses
                if ttt==1:
                    cur.execute("select * from Bus")
                    for i in cur.fetchall():
                        print(i)
                #Below bloac is used to book tickets
                elif ttt==2:
                    #Getting bus id
                    print("Enter the Bus id:")
                    bus_id=int(input())
                    #Fetching the corresponding bus id details
                    cur.execute(" select * from Bus where bus_id={}".format(bus_id,))
                    i=cur.fetchone()
                    print("Bus name:",i[0])
                    print("Bus from place:",i[1])
                    print("Bus to place:",i[2])
                    print("Bus total seats:",i[3])
                    print("Bus price:",i[4])
                    print("Enter number of tickets to book")
                    #Getting number of tickets to be booked
                    tickets_book=int(input())
                    #Below block is executed, if number of tickets available
                    if tickets_book<=i[3]:
                        #Calculating fare
                        fare=tickets_book*i[4]
                        #Displaying fare
                        print("total fare:",fare)
                        #Confirmation for booking
                        print("Confirm booking:\nEnter 1 for Yes\nEnter 2 for No")
                        tttt=int(input())
                        #Below block is executed, if booking is confirmed
                        if tttt==1:
                            agent_id1=agent_code
                            bus_id1=i[5]
                            #Creating object for the latest_booked_details
                            booking_object=latest_booked_tickets(agent_id1,bus_id1,tickets_book,fare)
                            booking=[booking_object.getagent_id(),booking_object.getbus_id(),booking_object.gettotal_tickets(),booking_object.gettotal_fare()]
                            #Calling procedur to insert the booking details
                            cur.callproc('booking_insert',booking)
                            update=[bus_id1,tickets_book]
                            #Calling procedure to update the abailable tickets in the bus which is booked
                            cur.callproc('update_bus',update)
                            print("Tickets booked")
                        #Below block is executed when confirmation fails
                        else:
                            print("Tickets not booked")
                    #Below block is executed when requested number of tickets is not available
                    else:
                        print("Tickets not available")
                #Below block is to display the latest booked details of the corresponding agent logged in
                elif ttt==3:
                    #joining the two tables bus and latest_ticked_booked and fetching the details and displaying
                    cur.execute("select B.Bus_name,B.from_loc,B.to_loc,L.total_tickets,L.total_fare from Latest_booked_tickets L join Bus B using(bus_id) where agent_id={} order by L.booking_id desc".format(agent_code,))
                    for i in cur.fetchall():
                        print(i)
                #Below block is executed to log out
                elif ttt==4:
                    print("Logged out")
                    break
    #Below block is executed to exit the app
    else:
        print("Exited")
        break

'''
This testcase inserts two buses and two agents and agent1 is booking for two buses and the booked details of agent1 will be displayed and the bus details after booking will be displayed 
Testcase:

1
admin
admin
1
redbus
chennai
salem
50
600
1
tourtravels
chennai
coimbatore
40
700
2
sam
8925226543
123123
2
stark
9977656543
156156
3
2
1
123123
2
1
5
1
2
2
10
1
3
1
4
3

'''
