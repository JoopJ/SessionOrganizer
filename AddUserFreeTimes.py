# Adding User free times to group free times #

import sys

UserFileName = input("User File Name: ")
UserTimesRead = open(UserFileName, "r")

GroupFileName = input("Group File Name: ") 
GroupTimesRead = open(GroupFileName, "r") 

GroupID = input("Group ID: ")


def formatTimeSlots(days, lines):
    for day in range(0,7):
        days[day] = (lines[day])
        days[day] = days[day].split()
        for slot in range(0,24):
            days[day][slot] = days[day][slot].split(',')

def printDays(days):
    for i in range(0,7):
        print("Day ", i)
        print(days[i])

def isIDPresent(ID, day, slot, Days):
    slotLength = len(Days[day][slot])
    for i in range(0,slotLength):
        if (Days[day][slot][i] == ID):
            return True
    return False

## goes through the user times and and recognizes any times that the user is Not Free and puts a the corresponding slot in its own times down as Not Free
## and adds the group ID to any time that the user is Free
def addTimeSlotsFromUserToGroup():
    for day in range(0,7):
        for slot in range(0,24):
            currentSlot = UserDays[day][slot]
            if currentSlot[0] == '1':
                GroupDays[day][slot].clear()
                GroupDays[day][slot].append('1')
            elif currentSlot[0] == '0':
                UserDays[day][slot].clear()
                UserDays[day][slot].append(GroupID)
            else:
                UserDays[day][slot].append(GroupID)
    return UserDays

## write the Days of a group to a file
def writeDaysToFile(days, file):
    for day in range(0,7):      
        for slot in range(0,24):
            file.write(str(days[day][slot]))
            file.write(" ")
        file.write("\n")
    
                

GroupLines = GroupTimesRead.readlines()
GroupDays = [[],[],[],[],[],[],[],[]]

UserLines = UserTimesRead.readlines()
UserDays = [[],[],[],[],[],[],[]]

try:
    formatTimeSlots(GroupDays, GroupLines)
except IndexError:
    print("ERROR: Incorrent Number of Slots for GroupDays, double check inputed slots")
    sys.exit()

try:
    formatTimeSlots(UserDays, UserLines)
except IndexError:
    print("ERROR: Incorrect Number of Slots for UserDays, double check inputed slots")
    sys.exit()

print("Group Days:")
printDays(GroupDays)
print("User Days:")
printDays(UserDays)

addTimeSlotsFromUserToGroup()

print("Group Days with User times taken into accont: ")
printDays(GroupDays)

print("User dDays with group times taken into account: ")
printDays(UserDays)


UserTimesWrite = open(UserFileName, "w")
GroupTimesWrite = open(GroupFileName, "w")

writeDaysToFile(UserDays, UserTimesWrite)
writeDaysToFile(GroupDays, GroupTimesWrite)

UserTimesWrite.close()
GroupTimesWrite.close()





