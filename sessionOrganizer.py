#!/usr/bin/python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import Table, Column, Integer, ForeignKey, update
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()

#Session = sessionmaker(autoFlush = False)
#session = Session()

app = Flask(__name__)           #create the flask application

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://darklord901db:Dark10rd99,,901@localhost/SessionOrganizer"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

#region Database Structure

#region Users

class Users(db.Model):                  #define the structure of the Users table
    __tablename__ = 'users'             #connects the class definition to the "person" database table
    #values:
    UserID = db.Column(db.Integer, autoincrement = True, primary_key = True)
    username = db.Column(db.String(80), nullable = False)
    password = db.Column(db.String(80), nullable = False)
    #relationships:
    groupMembers = relationship('GroupMembers', back_populates = 'users')
    userFreeTimes = relationship("UserFreeTimes")
    # usersFreeTimes = relationship('UserFreeTimes', back_populates = 'users')

    def __init__(self, username, password):         #defines the requirements to add a row to the Users table
        self.username = username
        self.password = password

class UserSchema(ma.Schema):        #defines the format to return a User
    class Meta:
        fields =  ('UserID', 'username', 'password')

user_schema = UserSchema()                  #this variable will be used to handle   
users_schema = UserSchema(many = True)   

#endregion Users

#region Groups

class Groups(db.Model):                 #define the structure of the Groups table
    __tablename__ = 'groups'
    #values:
    GroupID = db.Column(db.Integer, autoincrement = True, primary_key = True)
    groupName = db.Column(db.String(90), nullable = False)
    minimumTime = db.Column(db.Integer, nullable = False)
    #reltionships:
    groupMembers = relationship('GroupMembers', back_populates = 'groups')
    groupFreeTimes = relationship('GroupFreeTimes')
    # groupFreeTimes = relationship('GroupFreeTimes', back_populates = 'groups')

    def __init__(self, groupName, minimumTime):     #defines the requirements to add a row to the Groups table
        self.groupName = groupName
        self.minimumTime = minimumTime

class GroupSchema(ma.Schema):           #defines the format to return to return a user
    class Meta:
        fields = ('GroupID', 'groupName', 'minimumTime')

group_schema = GroupSchema()
groups_schema = GroupSchema(many = True)

#endregion Groups

#region GroupMembers

class GroupMembers(db.Model):
    __tablename__ = 'groupMembers'
    #values:
    RelationshipID = db.Column(db.Integer, primary_key = True)
    UserID = db.Column(db.Integer, ForeignKey('users.UserID'))
    GroupID = db.Column(db.Integer, ForeignKey('groups.GroupID'))
    ownerStatus = db.Column(db.Boolean, nullable = True)
    #relationships:
    users = relationship('Users', back_populates = 'groupMembers')
    groups = relationship('Groups', back_populates = 'groupMembers')


    def __init__(self, UserID, GroupID, ownerStatus):
        self.UserID = UserID
        self.GroupID = GroupID
        self.ownerStatus = ownerStatus

class groupMemberSchema(ma.Schema):
    class Meta:
        fields = ('UserID', 'GroupID', 'ownerStatus')

groupMember_schema = groupMemberSchema()
groupMembers_schema = groupMemberSchema(many = True)

#endregion GroupMembers

#region UserFreeTimes

class UserFreeTimes(db.Model, Base):
    __tablename__ = "userFreeTimes"
    #values:
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    UserID = db.Column(db.Integer, ForeignKey('users.UserID'))
    slots = db.Column(db.String(1169), nullable = False)
#    slot0 = db.Column(db.String(6))
#    slot1 = db.Column(db.String(6))
#    slot2 = db.Column(db.String(6))
#    slot3 = db.Column(db.String(6))
#    slot4 = db.Column(db.String(6))
#    slot5 = db.Column(db.String(6))
#    slot6 = db.Column(db.String(6))
#    slot7 = db.Column(db.String(6))
#    slot8 = db.Column(db.String(6))
#    slot9 = db.Column(db.String(6))
#    slot10 = db.Column(db.String(6))
#    slot11 = db.Column(db.String(6))
#    slot12 = db.Column(db.String(6))
#    slot13 = db.Column(db.String(6))
#    slot14 = db.Column(db.String(6))
#    slot15 = db.Column(db.String(6))
#    slot16 = db.Column(db.String(6))
#    slot17 = db.Column(db.String(6))
#    slot18 = db.Column(db.String(6))
#    slot19 = db.Column(db.String(6))
#    slot20 = db.Column(db.String(6))
#    slot21 = db.Column(db.String(6))
#    slot22 = db.Column(db.String(6))
#    slot23 = db.Column(db.String(6))

    def __init__(self, UserID, slots):
        self.UserID = UserID
        self.slots = slots

class FreeTimesSchema(ma.Schema):
    class Meta:
        fields = ("UserID", "slots")

freeTimes_schema = FreeTimesSchema()
listOfFreeTimes_schema = FreeTimesSchema(many = True)

#endregion UserFreeTimes

#region GroupFreeTimes

class GroupFreeTimes(db.Model, Base):
    __tablename__ = "groupFreeTimes"
    #values:
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    GroupID = db.Column(db.Integer, ForeignKey('groups.GroupID'))
    slots = db.Column(db.String(1169), nullable = False)

    #relationships:
    #groups = relationship('Groups', back_populates = 'groupFreeTimes')

    def __init__(self, GroupID, slots): 
        self.GroupID = GroupID
        self.slots = slots

class GroupFreeTimesSchema(ma.Schema):
    class Meta:
        fields = ("GroupID", "slots")

groupFreeTimes_schema = FreeTimesSchema()
listOfGroupFreeTimes_schema = FreeTimesSchema(many = True)

#endregion GroupFreeTimes

#endregion Database Structure

#region Users Endpoints

#endpoint to create a new user and give them 7 days of free slots in the UserFreeTimes table
@app.route("/user", methods = ["POST"])
def create_user():
    #request all the details for the user:
    #username
    username = request.json['username']
    #password
    password = request.json['password']

    #create the new_user object with the detials
    new_user = Users(username, password)

    #add the new_user object to the database
    db.session.add(new_user)
    #commit the changes to the database
    db.session.commit()
    #refresh our new_user object so it has the correct UserID attribute
    db.session.refresh(new_user)

    #create a UserFreeTimes row for the user in the UserFreeTimes table, with a blank set of slots all set to zero, meaning 'free'
    new_userFreeTimes = UserFreeTimes(new_user.UserID, "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0")
    db.session.add(new_userFreeTimes)
    db.session.commit()

    #return the UserID of the user so they know their own UserID
    return str(new_user.UserID)

#endpoint to create a new group and automatical set the creator as the owner throught the groupMembers table
@app.route("/group", methods = ["POST"])        #OBJECTIVE: the user is able to create their own groups
def create_group():
    #request all the detials for the group:
    #the UserID of the user creating the database
    UserID = request.json['UserID']
    #the name of the group being made
    groupName = request.json['groupName']
    #the minimum time for the group
    minimumTime = request.json['minimumTime']

    #creates the group object
    new_group = Groups(groupName, minimumTime)
    
    #adds the group to the database
    db.session.add(new_group)
    #make the chages to the database
    db.session.commit()
    #refresh the new_group object so that it has the correct GroupID attribute
    db.session.refresh(new_group)
    
    #print the details of the action to the console
    print("Group Details:")
    print("GroupID:", new_group.GroupID)
    print("groupName:", new_group.groupName)
    print("minimumTime:", new_group.minimumTime)

    #creates the relationship between the user who made the group and the group itself.
    new_groupMember = GroupMembers(UserID, new_group.GroupID, True) 
    
    #add the relationship to groupMembers
    db.session.add(new_groupMember)
    #commit the chagnes to the database
    db.session.commit()
    #return the GroupID so the user can tell people what to enter when joing a group.
    return str(new_group.GroupID)

#endpoint to add a user to a group
@app.route("/group/adduser", methods = ["POST"])
def add_user_to_group():                            #OBJECTIVE: the user is able to invite other users to their group
    #request the details:
    #the UserID of the user being added to the gorup
    UserID = request.json['UserID']
    #the GroupID of the group they are being added to 
    GroupID = request.json['GroupID']

    #creates the relationship between the user and the group, with  ownerStatus set to false
    new_groupMember = GroupMembers(UserID, GroupID, False)

    #add the relationship to the database
    db.session.add(new_groupMember)
    #save the changes to the database
    db.session.commit()
    #retunr the username of the user added and the groupName of the group they were added to
    return str("some dude got added to some group")

@app.route("/user/userFreeTimes/update", methods = ["POST"])
def update_user_free_times():
    UserID = request.json['UserID']
    newSlots = request.json['slots']

    print(UserID)
    #updateObj =update(UserFreeTimes).where(UserFreeTimes.UserID==givenUserID).values(slot10='X')
    x = db.session.query(UserFreeTimes).filter(UserFreeTimes.UserID==UserID)

    record = x.one()
    record.slots = newSlots

    db.session.commit()

    return "slots updated succesfuly."

#endregion

#region Admin Endpoints

#endpoint to get all groups
@app.route("/group", methods = ["GET"])
def get_all_groups():
    #get all the groups from the database
    all_groups = Groups.query.all()
    #dump the details into a schema
    result = groups_schema.dump(all_groups)
    return jsonify(result)

#endpoint to get all users
@app.route("/user", methods = ["GET"])
def get_all_users():
    all_users = Users.query.all()       #get all users in the users table
    result = users_schema.dump(all_users)       #dump the result into a users_schema
    return jsonify(result)      #return the users_schema with all the users' details

#endpoint to get a user by UserID
@app.route("/user/update/<UserID>", methods = ["GET"])
def get_user(UserID):
    #get the user details from their UserID
    user = Users.query.get(UserID)
    #return the details of the user
    return user_schema.jsonify(user)

#endregion

#run the application at the host ip address on port 5000
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug=True)