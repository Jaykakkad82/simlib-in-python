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
        return None

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
            return None

        # Insert at the End
        if index == self.get_length():

            itr = self.head
            while itr.next != None:
                itr = itr.next

            itr.next = node
            node.prev = itr
            self.tail = node
            return None

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
        return None


    def remove_at(self,index):
        # Exception for invalid Indices
        if index <0 or index>= self.get_length() :
            raise Exception ("Invalid Index")

        if self.head==None:
            raise Exception ("Invalid Index")
        #Remove at the begining
        if index ==0:
            self.head = self.head.next
            #self.head.prev = None
            #return None
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
            return None

    def detail_print(self):
        if self.head is None:
            print('The linkedlist is empty')
            return None
        itr = self.head
        print ('self.head =',itr)
        while itr !=None:
            print ("previous:   ", itr.prev,'   data: ', itr.data, '   Next : ', itr.next)
            itr = itr.next
        print ("self.tail = ", self.tail)
        return None

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


