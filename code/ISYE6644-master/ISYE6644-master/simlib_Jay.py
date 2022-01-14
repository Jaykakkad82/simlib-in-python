import os
import sys

# A doubly Linked list is being defined
# it consists of data, previous link and next link
class Node:
    def __init__(self, data = None , next= None, prev = None):
        self.data = data
        self.prev = prev
        self.next = next

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

  # Defining various methods for LinkedList

    def print(self):
        if self.head is None:
            print('The linkedlist is empty')
            return
        llst = ''
        itr = self.head
        while itr !=None:
            llst += str(itr.data)+'===>>'
            itr = itr.next
        print(llst)

    def get_length(self):
        if self.head == None:
            return 0

        count = 1
        itr = self.head
        while itr.next != None:
            count+=1
            itr = itr.next
        return count

    def insert_at(self, data, index):
        # Exception for invalid Indices
        if index <0 or index> self.get_length():
            raise Exception ("Invalid Index")

        node = Node(data,None, None)

        #Insert at the begining
        if index == 0:
            if self.head == None:
                self.head = node
                self.tail = node
            else:
                node.next = self.head
                self.head = node
                node.next.prev = node
            return

        # Insert at the End
        if index == self.get_length():

            itr = self.head
            while itr.next != None:
                itr = itr.next

            itr.next = node
            node.prev = itr
            self.tail = node
            return

        # Insert anwhere other than begining or End
        itr = self.head
        count = 0
        while itr:
            if count == index-1:
                node.next = itr.next
                node.prev = itr
                itr.next.prev = node
                itr.next = node
            itr = itr.next
            count =count+1


    def remove_at(self,index):
        # Exception for invalid Indices
        if index <0 or index>= self.get_length():
            raise Exception ("Invalid Index")

        #Remove at the begining
        if index ==0:
            self.head = self.head.next
            self.head.prev = None
            return

        itr = self.head
        count = 0
        while itr:
            if count == index-1:
                itr.next = itr.next.next
                if itr.next == None:  # Condition if it is the end of the linkedlist
                    self.tail = itr
                    pass
                else:
                    itr.next.prev = itr

                break
            itr = itr.next
            count = count+1

    def detail_print(self):
        if self.head is None:
            print('The linkedlist is empty')
            return
        itr = self.head
        print ('self.head =',itr)
        while itr !=None:
            print ("previous:   ", itr.prev,'   data: ', itr.data, '   Next : ', itr.next)
            itr = itr.next
        print ("self.tail = ", self.tail)

    def copy_from(self,index):
        # Exception for invalid Indices
        if index <0 or index> self.get_length():
            raise Exception ("Invalid Index")

        if self.head == None:
            raise Exception ("List is empty")

        itr = self.head
        count = 0
        while itr:
            if count == index:
                return itr.data
            itr = itr.next
            count = count +1


        #Remove at the begining
        if index ==0:
            self.head = self.head.next
            self.head.prev = None
            return

        itr = self.head
        count = 0
        while itr:
            if count == index-1:
                itr.next = itr.next.next
                if itr.next == None:  # Condition if it is the end of the linkedlist
                    self.tail = itr
                    pass
                else:
                    itr.next.prev = itr

                break
            itr = itr.next
            count = count+1


# ALl definitions from Simlibdefs.h
MAX_LIST =    25        # Max number of lists.
MAX_ATTR  =  10         # Max number of attributes.
MAX_SVAR  =  25         # Max number of sampst variables.
TIM_VAR   =  25         # Max number of timest variables.
MAX_TVAR =   50         # Max number of timest variables + lists.
EPSILON =   0.001       # Used in event_cancel.


# Initializing Global variables:

list_rank = [0]*26  # The attribute number, if any, according to which the records in list “list” are to be ranked
list_size = [0]*26  # The current number of records in each list
transfer = [0.0]*10  # Array for transferring into and out of the lists used in the simulation, where transfer[i] refers to attribute i of a record
next_event_type = None

# Some constants for the program
LIST_EVENT = 25  # Symbolic constant for the number of the event list
EVENT_TIME = 0    # Attribute number of the event time in the Event list
EVENT_TYPE = 1     # Attribute number of event type in the event list
INFINITY = 10^30  # A very large number

#symbolic constants that can be used by the main program
FIRST = 1
LAST = 2
INCREASING = 3
DECREASING = 4

#1 Initialising list of 26 items as Linkedlist
master = [LinkedList()]*26


Event_list = 25     # Event list is always number 25

#2 Initialize system attributes
sim_time = 0.0
transfer = [0.0]*10



# class simlibPY():  # We dont have to make it a Class. It will be easier to run main programs

def init_simlib():
    # Initialize system attributes.
    global sim_time

    #Initialize list attributes
    master = [LinkedList()]*26
    list_size = [0]*26
    list_rank = [0]*26
    global transfer
    list_rank[LIST_EVENT] = EVENT_TIME

    # initialize statistical routines
    sampst(0.0, 0)
    timest(0.0, 0)
    return


def list_file(option, list):

        ''' Place transfr into list "list".
            Update timest statistics for the list.
            option:
                FIRST place at start of list
                LAST  place at end of list
                INCREASING  place in increasing order on attribute list_rank(list)
                DECREASING  place in decreasing order on attribute list_rank(list)
                (ties resolved by FIFO) '''

        # Check if the list values are appropriate
        if list<0 or list > MAX_LIST:
            print("Invalid list {} for list_file at time {}".format(list,sim_time))
            return
        # check if option values is appropriate
        if option<1 or option>4:
            print("Invalid option {} for list_file at time {}".format(option,sim_time))
            return

        if option == 1 or list_size[list]==0: # Also insert at the top if there are no elements in the list
            master[list].insert_at(transfer,0) # insert at the top
        elif option ==2:
            end = master[list].get_length()  # find the length /end of list
            master[list].insert_at(transfer,end) # insert at the end

        # Increasing order
        elif option == 3:
            i = list_rank[list]  # find which attribute (of data) to compare for increasing order
            value_comp = transfer[i]  # find which value to be compared
            itr = master[list].head
            index = 0

            if itr.data[i]>value_comp:  # if the first value is greater than value_comp
                master[list].insert_at(transfer,index) # insert at the top
            else:
                while itr: #lets iterate through the list
                    if ((itr.next == None) or (itr.next.data[i] > value_comp and itr.data[i]<= value_comp)): # We have reached end or value_comp is between next data and current data
                        master[list].insert_at(transfer,index+1) # insert at the next index point
                        break
                    itr = itr.next
                    index+=1

        # decreasing order
        elif option == 4:
            i = list_rank[list]  # find which attribute (of data) to compare for increasing order
            value_comp = transfer[i]  # find which value to be compared
            itr = master[list].head
            index = 0
            if itr.data[i]< value_comp:  # if the first value is less than value_comp
                master[list].insert_at(transfer,index) # insert at the top
            else:
                while (itr != None) : #lets iterate through the list
                    #print('I am here', index, itr.next)
                    if ((itr.next == None) or (itr.next.data[i] < value_comp and itr.data[i]>= value_comp)): # We have reached end or value_comp is between next data and current data
                        master[list].insert_at(transfer,index+1) # insert at the next index point
                        break
                    itr = itr.next
                    #print('I am here', index, itr.next)
                    index+=1


        # increment the list size
        list_size[list] += 1
        # Update the area under the number-in-list curve.
        timest(list_size[list], TIM_VAR + list)
        return



def list_remove(option, list): #Jay
        ''' Remove a record from list "list" and copy attributes into transfer.
            Update timest statistics for the list.
            option = FIRST remove first record in the list
            option = LAST  remove last record in the list '''
        #Raise exception is list number or option is incorrect
        #print(option, list)
        global transfer
        if (list < 0 or list > 25) or (option != FIRST and option != LAST):
            raise Exception ("Invalid entry")

        # Print and Exit if the linkedlist is empty
        if list_size[list] <=0:
            print("underflow of list {} at time {}".format(list,sim_time))
            return

        # Copy to transfer and remove the entry from the list
        len = master[list].get_length()
        if option == FIRST:
            transfer = master[list].copy_from(0)
            master[list].remove_at(0)
        else:
            transfer = master[list].copy_from(len-1)
            master[list].remove_at(len-1)

        #decrement the list size
        list_size[list] -=1

        # Update the area under the number-in-list curve.
        timest(list_size[list], TIM_VAR + list)  # TIM_VAR is total variables in timest
        print('Transfer has this value at end of list remove', transfer)

        return



def timing():

    '''Remove next event from event list, placing its attributes in transfer. Set sim_time (simulation time) to event time, transfer[1].
    Set next_event_type to this event type, transfer[2]. */'''

    # remove the first event from the event list and put it in transfer
    list_remove(FIRST,LIST_EVENT)
    print('Transfer has this value right now', transfer)

    global sim_time
    # check for time reversal
    if transfer[EVENT_TIME] < sim_time:
        print('Incorrect Attempt to schedule event type {} for time {} at time{}'.format(transfer[EVENT_TYPE],transfer[EVENT_TIME],sim_time))
        return
    # advance simulation clock
    sim_time = transfer[EVENT_TIME]
    next_event_type = transfer[EVENT_TYPE]
    return



def event_schedule(time_of_event, type_of_event):
    '''Schedule an event at time event_time of type event_type.  If attributes beyond
    the first two (reserved for the event time and the event type) are being used in the event list,
    it is the user's responsibility to place their values into the transfer array before invoking event_schedule.'''
    transfer[EVENT_TIME] = time_of_event
    transfer[EVENT_TYPE] = type_of_event
    list_file(INCREASING,LIST_EVENT)
    return


def event_cancel(event_type): # Jay
    '''Remove the first event of type event_type from the event list, leaving its
   attributes in transfer.  If something is cancelled, event_cancel returns 1;
   if no match is found, event_cancel returns 0.'''

# If the event list is empty, do nothing and return 0.
    if (list_size[LIST_EVENT] == 0):
        return 0

    itr = master[LIST_EVENT].head
    index = 0

    #iterate through the linked list
    while itr:
        if itr.data[EVENT_TYPE] == event_type: # if the event type matches
            transfer = master[LIST_EVENT].copy_from(index)  # put the data into transfer array
            master[LIST_EVENT].remove_at(index)    # remove the entry
            list_size[LIST_EVENT]-=1                # decrement size of event list
            timest(list_size[LIST_EVENT], TIM_VAR + LIST_EVENT)  # Update the area under the number-in-event-list curve
            return 1
        itr = itr.next
        index += 1
    return 0


def sampst(value, variable):
    pass

def timest(value, variable):
    pass

def filest(list): # Jay

    ''' Report statistics on the length of list "list" in transfer:
    [1] = time-average of list length updated to the time of this call
    [2] = maximum length list has attained
    [3] = minimum length list has attained
    This uses timest variable TIM_VAR + list.'''
    return timest(0.0, -(TIM_VAR + list))  # need to check


def out_sampst(unit, lowvar, highvar):
    pass

def out_timest(unit, lowvar, highvar):
    pass


def out_filest(unit, lowlist, highlist): # Need to implement fprintf properly
    ''' Write timest list-length statistics for lists lowlist through highlist on
    file "unit". '''

    if (lowlist>highlist or lowlist > MAX_LIST or highlist > MAX_LIST):  # if variables arent correct do not do anything
        return

    print(unit,"\n  File         Time")
    print(unit, "\n number       average          Maximum          Minimum")
    print(unit, "\n_______________________________________________________")
    for list in range(lowlist, highlist+1):
        print(unit, "\n\n", list)
        filest(list)
        for iatrr in range(1,4):
            print(unit, iatrr)
    print(unit, "\n_______________________________________________________")
    print(unit, "\n\n\n")
    return




def expon(mean,stream):
    import math
    return -mean * math.log(lcgrand(stream))

def random_integer(prob_distrib, stream):
    pass

def uniform(a, b, stream): #Jay
    return a + lcgrand(stream)* (b - a)


def erlang(m, mean, stream):
    pass

def lcgrand(stream):
    pass

def lcgrandst(zset, stream): #Jay
    zrng[stream] = zset
    return


def lcgrandgt(stream):
    pass

def pprint_out():
    pass




if __name__ == '__main__':


    #1 testing the methods of linkedlist
    #dll = LinkedList()
    #dll.insert_at('A',0)
    #dll.insert_at('B',0)
    #dll.insert_at('C',2)
    #dll.print()
    #print(dll.get_length())

    #dll.print()
    #dll.insert_at([0,1],3)
    #dll.print()
    #a = [0]*2
    #a = dll.copy_from(3)
    #print (a)
    #master[25].insert_at((2,1),0)
    #master[25].insert_at((1,0),0)
    #master[25].insert_at((1,1,5,8),0)
    #master[25].print()
    #transfer = master[25].copy_from(2)
    #print('In the transfer array: ',transfer)

    #testing the functions
    init_simlib()
    master[25].insert_at([1,1],0)
    master[25].insert_at([2,0],1)
    master[25].insert_at([3,1],2)
    master[25].print()
    transfer = master[25].copy_from(2)
    print('In the transfer array: ',transfer)
    transfer = [2,2]
    list_size[25] = 3
    master[25].detail_print()

    # 2.testing list_file function
    list_file(3,25)
    master[25].detail_print()
    print('Other stuff to check')
    print(transfer)
    master[25].print()
    print (list_size[25])
    print(list_rank[25])

    #3. testing list_remove
    list_remove(1,25)
    #master[25].detail_print()
    #print('Other stuff to check')
    #print(transfer)
    print('')
    print('')
    master[25].print()
    #print (list_size[25])
    #print(list_rank[25])

    # testing timing()
    print('LIST EVENT', LIST_EVENT)
    print('sim time ', sim_time)
    sim_time =0
    timing()
    print('sim time ', sim_time)
    print('Transfer', transfer)
    master[25].print()






