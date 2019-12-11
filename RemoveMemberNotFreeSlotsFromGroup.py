# Remove slots that member isn't free #
# '0' reprisents a free times slot. anything else meanes the user is not free #
# all user time slots are set to free by default #

userFiles = ["User1Times.txt", "User2Times.txt", "GroupTimes.txt"]    #list of files to be opened and formated. The real program should only take one member's free times and the group's times


UserTimes = []

def openFileAndFormat(fileName):
    userTimesRead = open(fileName, "r")
    userLines = userTimesRead.readlines()
    userDays = [[],[],[],[],[],[],[]]
    UserTimes.append(formatTimeSlots(userDays, userLines))
    

def formatTimeSlots(days, lines):
    for day in range(0,7):
        days[day] = (lines[day])
        days[day] = days[day].split()
        for slot in range(0,24):
            days[day][slot] = days[day][slot].split(',')
    return days

def printDays(days):
    for i in range(0,7):
        print("Day ", i)
        print(days[i])
    print("\n\n\n")


# looking through user times, if there is a slot that isn't free then
# the cooresponding group slot is set to not free
def removeCoorespondingNotFreeSlots(userDays, groupDays):
    for day in range(0,7):
        for slot in range(0,24):
            if (userDays[day][slot][0] != "0"):
                groupDays[day][slot][0] = "1"
    return groupDays

def putGroupDaysIntoFile(groupDays):
    groupDaysFile = open("GroupFreeTimes.txt", "w+")
    for day in range(0,7):
        for slot in range(0,24):
            groupDaysFile.write(groupDays[day][slot][0])
            groupDaysFile.write(" ")
        groupDaysFile.write("\n")
    groupDaysFile.close()


for i in range(0,len(userFiles)):
    openFileAndFormat(userFiles[i])

printDays(UserTimes[2])


UserTimes[2] = removeCoorespondingNotFreeSlots(UserTimes[0], UserTimes[2])
UserTimes[2] = removeCoorespondingNotFreeSlots(UserTimes[1], UserTimes[2])

printDays(UserTimes[2])

putGroupDaysIntoFile(UserTimes[2])







