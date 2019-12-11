f = open("GroupOrders2.txt", "r")

import random
import sys

lines = f.readlines()
days = [[],[],[],[],[],[],[],[]]

## groups stuff ##
# needed to work out the specifics of inputting groups minium times when i have communication with the raspberry Pi up and running #
AMT = 3
A_ID = 'A'
BMT = 2
B_ID = 'B'
CMT = 1
C_ID = 'C'

GroupsMT = {'A' : 3, 'B' : 2, 'C' : 1}

#takes in the time slot conflicts form the txt document and splits the days
#then plits the slots
#then splits the groupIDs int the time slots.
#your left with a list of 7 lists that have time slots that correspond to
#each hour of the day, if a slot has no groups in it then the slot has a '0'
#if the slot has a group in it, their GroupID will be shown. if another group
#is present in the same slot, the group is split into a list of GroupID's
def formatTimeSlots():      
    for day in range(0,7):
        days[day] = (lines[day])
        days[day] = days[day].split()
        for slot in range(0,24):
            days[day][slot] = days[day][slot].split(',')

### returns True if the given ID is present in the slot ###
def isIDPresent(ID, day, slot):

    slotLength = len(days[day][slot])
    for i in range(0,slotLength):
        if (days[day][slot][i] == ID):
            return True

    return False
        

### counts how many possible time slots a group can have based off their minimum time ###
def calculatePriority(ID, MT):
    currentSlotLength = 0
    priority = 0
    
    for day in range(0,7):
        for slot in range(0,24):
            
            if (isIDPresent(ID, day, slot)):              #if the group was found then increase the current slot length to account for group slots in a row
                currentSlotLength += 1
                                   
            elif (currentSlotLength != 0):          #if this slot is the end of a series of slots for a group then the priority will be calculated
                temp = currentSlotLength - MT + 1
                currentSlotLength = 0
            
                if (temp > 0):
                    priority += temp

        groupPresent = False

    return priority

### returns true of each day of has 24 slots ###
def correctNumberOfHours():
    for i in range(0,7):
        if (len(days[i]) != 24):
            return False
    return True

### removes series of slots that are less than the minimum time for a group ###
def removeUselessSlots(GroupID, MinimumTime):
    currentSlotLength = 0
        
    for day in range (0,7):
        
        for slot in range(0,24):

            if (searchSlotForID(day, slot, GroupID)):      # searchs for slots that contain the groupID
                currentSlotLength += 1
                #print("Slot Found", days[day][slot], currentSlotLength)
                
            else:                           # if a slot dosen't contain the ID then we check if the current series meet the minimum time requirements
                #print("No Slot Found", days[day][slot])                

                if (currentSlotLength != 0 and currentSlotLength < MinimumTime):   # if the current seris of slots is less than the minimum time required for a group
                    #print("Useless Slot(s) found!")                                 #then we remove the Group's IDs from the seris of slots
                    
                    for slotToRemove in range(slot - currentSlotLength, slot):
                        removeGroupIDFromSlot(GroupID, day, slotToRemove)

                    currentSlotLength = 0
                currentSlotLength = 0

### removes the ID from a slot ###
def removeGroupIDFromSlot(GroupID, day, slot):
    #print(days[day][slot], " - Removing: ", GroupID)
    days[day][slot].remove(GroupID)
    if (len(days[day][slot]) == 0):
        days[day][slot].append('0')
        
### displays the days list in python ###
def printDays():
    for i in range(0,7):
        print("Day ", i)
        print(days[i])

### returns True if the ID is present in the given slot ###
def searchSlotForID(day, slot, ID):
    for i in range(0, len(days[day][slot])):
        if (days[day][slot][i] == ID):
            return True

### returns True if there is a conflict in a slot and False if there is no conflict ###
def isConflict(day,slot):
    if (len(days[day][slot]) > 1):
        return True
    else:
        return False

### returns the group with the highest primary priority ###
def comparePrimaryPriorities(groups):
    highestPriority = 169   #168 is the maximum value for primary priority you can have, with a slot on every hour of every day and with a minimum time of 1

    for group in groups:
        currentGroupPriority = priorities[group]
        if (currentGroupPriority < highestPriority):
            highestPriority = currentGroupPriority
            highestPriorityGroup = group
        elif (currentGroupPriority == highestPriority):
            print("GROUPS WITH SAME PRIMARY PRIORITY")
            print(group, " has priority: ",priorities[group])
            print(highestPriorityGroup, " has priority: ", highestPriority)
            ### there are two groups with the same primary priority ###

            highestPriorityGroup = compareSecondaryPriority(highestPriorityGroup, group)           

    return highestPriorityGroup

### return the group with the highest Secondary Prioroity
def compareSecondaryPriority(group1, group2):   
    print("Group ", group1, "'s Secondary Priority: ", GroupsMT[group1])
    print("Group ", group2, "'s Secondary Priority: ", GroupsMT[group2])

    if (GroupsMT[group1] > GroupsMT[group2]):           
        return group1
    elif (GroupsMT[group1] == GroupsMT[group2]):                #if the two groups have the same secondary priority then return a random choice of which group wins
        print("GROUPS WITH SAME SECONDARY PRIORITY")
        choiceList = [group1,group2]
        return random.choice(choiceList)                
    else:
        return group2
    return max(tempMinimumTimes)


### returns the length of a series of slots that contain a given groupID ###
def findLengthOfSeries(ID,startDay,startSlot):
    print("Finding Length of series")
    #takes the given slot and ID and starts going down slots to find a seris of slots that contain the ID
    incriment = 0
    seriesLength = 0
    while True:             #we could assume that the given ID is in the given slot but I think it's worth double checking.
        currentSlot = days[startDay][startSlot + incriment]
        print(days[startDay][startSlot+incriment])
                 
        if (searchSlotForID(startDay, startSlot + incriment, ID)):          #if the ID is present then the series length is increased, if not then the series has ended and we return the length of the series
            seriesLength += 1
            incriment += 1
            
        else:
            return seriesLength


### add the groups in a slot to a given list ###
def addGroups(day,slot, GroupsInConflict):
    print("Groups being added to conflict: ", days[day][slot])
    for group in days[day][slot]:
        
        GroupsInConflict.append(group)

    return GroupsInConflict


### removes duplicates from a given list ###
def removeDuplicatesFromList(IDs):
    return list(dict.fromkeys(IDs))

### reurns the greatest valued item in a given dictionary ###
def greatestItemInDict(dic):
    templist = []
    for key in dic:
        templist.append(dic[key])
    return max(templist)

### removes the group ID's of every group except the given ID ###
def removeLoosingGroups(day,slot, winningGroup, seriesLength):
    for x in range(slot, slot + seriesLength):
        currentSlot = days[day][x]
        print("Slot before removing loosers: ", currentSlot)
        groupsToRemove = []

        if winningGroup in currentSlot:                 #if the given group is in a slot then every group in that slot that isn't the given group will be removed
            
            for i in range(0,len(currentSlot)):             

                if currentSlot[i] != winningGroup:
                    groupsToRemove.append(currentSlot[i])


        print("Slot: ", currentSlot, ". Groups being removed: ", groupsToRemove)            
        for group in groupsToRemove:                #removes the specified groups from the current slot
            currentSlot.remove(group)
            print(currentSlot)

        if currentSlot == None:             #if all groups in the slot have been removed then we put the group into the standard format of a 0 reprisenting an empty group
            currentSlot.append('0')

        print("Slot after removing loosers: ", currentSlot)

### checks all 7 days for conflicting groups by checking each slot for conflicts, returns True if a conflict is found and False is no conflicts are found ###
def checkForConflicts():            
    for day in range(0,7):
        for slot in range(0,24):

            if (len(days[day][slot]) > 1):
                return True

    return False



### Searchs for Conflicts, resolves them using priority system, re-calculates priority, repeats for every conflict ###
def removeConflicts():

    for day in range(0,7):
        for slot in range(0,24):
            currentSlot = days[day][slot]

            GroupsInConflict = []

            if (isConflict(day,slot)):      #if there is conflict to be handled, this is where the handleing begins
                GroupsInConflict = (addGroups(day,slot,GroupsInConflict))   #make a list of groups that are in the initial conflit slot
                print("Groups in initial conflict: ", GroupsInConflict)

                SeriesLengths = {}
                for group in days[day][slot]:
                    SeriesLengths[group] = findLengthOfSeries(group, day, slot)         #make a dictionary that stores the series length of each group in the conflict

                print("Series lengths: ", SeriesLengths)

                greatestSeriesLength = greatestItemInDict(SeriesLengths)
                print("Greatest series length: ", greatestSeriesLength)
                
                for searchSlot in range(slot + 1, slot + greatestSeriesLength):         #looks for other group ID's in slots that are occupied by any of the conflicting group

                    for group in days[day][searchSlot]:                 #adds all the group ID's found in the slots that the series of the initial groups
                        print("found in the conflict: ",group)
                        GroupsInConflict.append(group)

                GroupsInConflict = removeDuplicatesFromList(GroupsInConflict)           #remove the duplicates that were gained when seraching for other groups in the conflict
                print("Groups in final conflict: ", GroupsInConflict)
                for group in GroupsInConflict:
                    print(group, " has priority: ", priorities[group])


                
                winningGroup = comparePrimaryPriorities(GroupsInConflict)       #compare the groups in the conflict to find winning group
                print("Winning Group: ",winningGroup)
                removeLoosingGroups(day, slot, winningGroup, greatestSeriesLength)      #remove all the groups that are conflicting with the winning group
                

                for group in GroupsInConflict:                      #re-calculate each groups priority after groups have lost 
                    print("Group ", group, "'s priority: ", priorities[group])
                    priorities[group] = calculatePriority(group, GroupsMT[group])
                                                                    #and remove any useless group slots that could have been created by this resolution
                    removeUselessSlots(group, GroupsMT[group])                  
                    
            
### MAIN ###

# retuns an error if their aren't 24 slots on each line
try:        
    formatTimeSlots()   # first put the slots into a 3D list
except IndexError:
    print("ERROR: Incorrect Number of Slots, double check inputed slots")
    sys.exit()

# calculate the priorities of each group
## should be changed when the groups system is updated ##
priorities = {}
priorities[A_ID] = calculatePriority(A_ID, AMT)
priorities[B_ID] = calculatePriority(B_ID, BMT)
priorities[C_ID] = calculatePriority(C_ID, CMT)

for x in priorities:
    print("Group ", x, " Priority: ",priorities[x])

#remove any slots that are of length less than the groups minimum time
## should be changed when the groups system is updated ##
removeUselessSlots(A_ID,AMT)
removeUselessSlots(B_ID,BMT)
removeUselessSlots(C_ID,CMT)

printDays()

while (checkForConflicts()):        # looks for conflicts and runs the removeConflicts function to remove them, will normaly take 1 run but in a case when there are no conflicts there is no point in running the remove conflicts function
    print("conflicts found, removing.")
    removeConflicts()

# displays the results
printDays()
for x in priorities:
    print("Group ", x, " Priority: ",priorities[x])


### write the calculated time slots to a new file ###
f2 = open("GroupOrdersWithoutConflict.txt", "w")

print("File is open")

### writes each slot to the currently open file in the same format they were entered, with a 0 reprisenting an empty slot
def writeDaysToFile():

    print("adding stuff")
    
    for day in range(0,7):          # write each slot to the file in the same format it was entered, with 0 reprisenting an empty slot
        for slot in range(0,24):
            
            f2.write(days[day][slot][0])
            f2.write(" ")
        f2.write("\n")
            

writeDaysToFile()
         
f2.close()

print("file closed")



