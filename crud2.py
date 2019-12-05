from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://darklord901db:Knowle5478@localhost/SessionOrganizer"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    __tablename__ = 'users'
    #fields:
    UserID = db.Column(db.String(6), primary_key = True, unique = True, nullable = False)
    username = db.Column(db.String(80), nullable = False)
    password = db.Column(db.String(80), nullable = False)
    #relationships:
    groupMembers = relationship("GroupMembers", back_populates = "users")
    UserFreeTimes = relationship("UserFreeTimes", back_populates = "users")

    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('UserID','username', 'password')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

class Groups(db.Model):
    __tablename__ = 'groups'
    #fields:
    GroupID = db.Column(db.String(6), primary_key = True, unique = True, nullable = False)
    groupName = db.Column(db.String(80), nullable = False)
    minimumTime = db.Column(db.Integer(), nullable = False)
    #relationships:
    groupMembers = relationship("GroupMembers", back_populates = "groups")
    GroupFreeTimes = relationship("GroupFreeTimes", back_populates = "groups")

    def __init__(self, GroupID, groupName, minimumTime):
        self.GroupID = GroupID
        self.groupName = groupName
        self.minimumTime = minimumTime

class GroupSchema(ma.Schema):         #defines the structure of our endpoints response
    class Meta:
        fields = ("GroupID", "groupName", "minimumTime")       #these fields will be returned as a response

group_schema = GroupSchema()
listOfGroups_schema = GroupSchema(many = True)

#region GroupMembers

class GroupMembers(db.Model, Base):               #declare the model for GroupMembers and defines it's fieldsproperties
    __tablename__ = 'groupMembers'
    #values:
    id = db.Column(db.String(6), primary_key = True, nullable = False)
    GroupID = db.Column(db.String(6), ForeignKey('groups.GroupID'))
    UserID = db.Column(db.String(6), ForeignKey('users.UserID'))
    ownerStatus = db.Column(db.Boolean())
    #relationshiop
    groups = relationship("Groups", back_populates = "groupMembers")
    users = relationship("Users", back_populates = "groupMembers")

    def __init__(self, groupName, minimumTime, ownerStatus):
        self.groupName = groupName
        self.minimumTime = minimumTime
        self.ownerStatus = ownerStatus

class GroupMembersSchema(ma.Schema):            #defines the structure of our endpoint response
    class Meta:
        fields = ("GroupID", "UserID", "ownerStatus")       #these fields will be returned as a response

groupMember_schema = GroupMembersSchema()
listOfGroupMembers_schema = GroupMembersSchema(many = True)

#endregion

#region FreeTimes

class UserFreeTimes(db.Model, Base):
    __tablename__ = "userFreeTimes"
    #values:
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    UserID = db.Column(db.String(6), ForeignKey('users.UserID'))
    day = db.Column(db.Integer(), nullable = False)
    slot0 = db.Column(db.String(6))
    slot1 = db.Column(db.String(6))
    slot2 = db.Column(db.String(6))
    slot3 = db.Column(db.String(6))
    slot4 = db.Column(db.String(6))
    slot5 = db.Column(db.String(6))
    slot6 = db.Column(db.String(6))
    slot7 = db.Column(db.String(6))
    slot8 = db.Column(db.String(6))
    slot9 = db.Column(db.String(6))
    slot10 = db.Column(db.String(6))
    slot11 = db.Column(db.String(6))
    slot12 = db.Column(db.String(6))
    slot13 = db.Column(db.String(6))
    slot14 = db.Column(db.String(6))
    slot15 = db.Column(db.String(6))
    slot16 = db.Column(db.String(6))
    slot17 = db.Column(db.String(6))
    slot18 = db.Column(db.String(6))
    slot19 = db.Column(db.String(6))
    slot20 = db.Column(db.String(6))
    slot21 = db.Column(db.String(6))
    slot22 = db.Column(db.String(6))
    slot23 = db.Column(db.String(6))
    #relationships:
    Users = relationship("Users", back_populates = "userFreeTimes")

    def __init__(self, day, slot0, slot1, slot2, slot3, slot4, slot5, slot6, slot7, slot8, slot9, slot10, slot11, slot12, slot13, slot14, slot15, slot16, slot17, slot18, slot19, slot20, slot21, slot22, slot23):
        self.day = day
        self.slot0 = slot0
        self.slot1 = slot1
        self.slot2 = slot2
        self.slot3 = slot3
        self.slot4 = slot4
        self.slot5 = slot5
        self.slot6 = slot6
        self.slot7 = slot7
        self.slot8 = slot8
        self.slot9 = slot9
        self.slot10 = slot10
        self.slot11 = slot11
        self.slot12 = slot12
        self.slot13 = slot13
        self.slot14 = slot14
        self.slot15 = slot15
        self.slot16 = slot16
        self.slot17 = slot17
        self.slot18 = slot18
        self.slot19 = slot19
        self.slot20 = slot20
        self.slot21 = slot21
        self.slot22 = slot22
        self.slot23 = slot23

class FreeTimesSchema(ma.Schema):
    class Meta:
        fields = ("day", "slot0", "slot1", "slot2", "slot3", "slot4", "slot5", "slot6", "slot7", "slot8", "slot9", "slot10", "slot11", "slot12", "slot13", "slot14", "slot15", "slot16", "slot17", "slot18", "slot19", "slot20", "slot21", "slot22", "slot23")

freeTimes_schema = FreeTimesSchema()
listOfFreeTimes_schema = FreeTimesSchema(many = True)

#endregion

#region GroupFreeTimes

class GroupFreeTimes(db.Model, Base):
    __tablename__ = "groupFreeTimes"
    #values:
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    GroupID = db.Column(db.String(6), ForeignKey('groups.GroupID'))
    day = db.Column(db.Integer(), nullable = False)
    slot0 = db.Column(db.String(6))
    slot1 = db.Column(db.String(6))
    slot2 = db.Column(db.String(6))
    slot3 = db.Column(db.String(6))
    slot4 = db.Column(db.String(6))
    slot5 = db.Column(db.String(6))
    slot6 = db.Column(db.String(6))
    slot7 = db.Column(db.String(6))
    slot8 = db.Column(db.String(6))
    slot9 = db.Column(db.String(6))
    slot10 = db.Column(db.String(6))
    slot11 = db.Column(db.String(6))
    slot12 = db.Column(db.String(6))
    slot13 = db.Column(db.String(6))
    slot14 = db.Column(db.String(6))
    slot15 = db.Column(db.String(6))
    slot16 = db.Column(db.String(6))
    slot17 = db.Column(db.String(6))
    slot18 = db.Column(db.String(6))
    slot19 = db.Column(db.String(6))
    slot20 = db.Column(db.String(6))
    slot21 = db.Column(db.String(6))
    slot22 = db.Column(db.String(6))
    slot23 = db.Column(db.String(6))
    #relationships:
    Groups = relationship("Groups", back_populates = "groupFreeTimes")

    def __init__(self, day, slot0, slot1, slot2, slot3, slot4, slot5, slot6, slot7, slot8, slot9, slot10, slot11, slot12, slot13, slot14, slot15, slot16, slot17, slot18, slot19, slot20, slot21, slot22, slot23):
        self.day = day
        self.slot0 = slot0
        self.slot1 = slot1
        self.slot2 = slot2
        self.slot3 = slot3
        self.slot4 = slot4
        self.slot5 = slot5
        self.slot6 = slot6
        self.slot7 = slot7
        self.slot8 = slot8
        self.slot9 = slot9
        self.slot10 = slot10
        self.slot11 = slot11
        self.slot12 = slot12
        self.slot13 = slot13
        self.slot14 = slot14
        self.slot15 = slot15
        self.slot16 = slot16
        self.slot17 = slot17
        self.slot18 = slot18
        self.slot19 = slot19
        self.slot20 = slot20
        self.slot21 = slot21
        self.slot22 = slot22
        self.slot23 = slot23

class GroupFreeTimesSchema(ma.Schema):
    class Meta:
        fields = ("day", "slot0", "slot1", "slot2", "slot3", "slot4", "slot5", "slot6", "slot7", "slot8", "slot9", "slot10", "slot11", "slot12", "slot13", "slot14", "slot15", "slot16", "slot17", "slot18", "slot19", "slot20", "slot21", "slot22", "slot23")

groupFreeTimes_schema = FreeTimesSchema()
listOfGroupFreeTimes_schema = FreeTimesSchema(many = True)

#endregion

#endpoint to create new user
@app.route("/user", methods=["POST"])
def add_user():
    username = request.json['username']
    email = request.json['email']
    
    new_user = User(username, email)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user)


# endpoint to show all users
@app.route("/user", methods=["GET"])
def get_user():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)


# endpoint to get user details by id
@app.route("/user/<id>", methods=["GET"])
def user_detail(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


# endpoint to update user
@app.route("/user/<id>", methods=["PUT"])
def user_update(id):
    user = User.query.get(id)
    username = request.json['username']
    email = request.json['email']

    user.email = email
    user.username = username

    db.session.commit()
    return user_schema.jsonify(user)


# endpoint to delete user
@app.route("/user/<id>", methods=["DELETE"])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)




if __name__ == '__main__':
    app.run(debug=True)