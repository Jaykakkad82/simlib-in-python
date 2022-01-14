#single-server queueing system using simlibPy
import sys
import os
import pandas
import csv
from simlib import simlibPY
from csv_utils import *

class singleServerQueueing:
    def __init__(self, mean_interarrival):
        # Initialize simlib
        self.spy = simlibPY()
        # Event type for arrival.
        self.EVENT_ARRIVAL = 1  
        # Event type for departure.
        self.EVENT_DEPARTURE = 2  
        # List number for queue.
        self.LIST_QUEUE = 1 
        # List number for server. 
        self.LIST_SERVER = 2 
        # sampst variable for delays in queue.         
        self.SAMPST_DELAYS =1 
        # Random-number stream for interarrivals.
        self.STREAM_INTERARRIVAL = 1  
        # Random-number stream for service times
        self.STREAM_SERVICE = 2  
        self.num_custs_delayed = 0
        self.spy.event_schedule(self.spy.sim_time + self.spy.expon(mean_interarrival, self.STREAM_INTERARRIVAL),self.EVENT_ARRIVAL)  

    def arrive(self,mean_service):

        # Schedule next arrival.
        self.spy.event_schedule(self.spy.sim_time + self.spy.expon(mean_interarrival, self.STREAM_INTERARRIVAL),self.EVENT_ARRIVAL)

        # Check to see whether server is busy (i.e., list SERVER contains a record).
        if (self.spy.list_size[self.LIST_SERVER] == 1):
            #Server is busy, so store time of arrival of arriving customer at end of list LIST_QUEUE.
            self.spy.transfer[1] = self.spy.sim_time
            self.spy.list_file(self.spy.LAST, self.LIST_QUEUE)
        else:
            # Server is idle, so start service on arriving customer, who has a delay of zero.  (The following statement IS necessary here.)
            self.spy.sampst(0.0, self.SAMPST_DELAYS)

            # Increment the number of customers delayed.
            self.num_custs_delayed = self.num_custs_delayed +1

            # Make server busy by filing a dummy record in list LIST_SERVER.
            self.spy.list_file(self.spy.FIRST, self.LIST_SERVER)

            #Schedule a departure (service completion).
            self.spy.event_schedule(self.spy.sim_time + self.spy.expon(mean_service, self.STREAM_SERVICE),self.EVENT_DEPARTURE)  
        return None

    def depart(self,mean_service):
        # Check to see whether queue is empty.
        if (self.spy.list_size[self.LIST_QUEUE] == 0):

            '''The queue is empty, so make the server idle and leave the departure
            (service completion) event out of the event list. (It is currently
            not in the event list, having just been removed by timing before
            coming here.)
            '''
            self.spy.list_remove(self.spy.FIRST, self.LIST_SERVER)
        else:
            '''The queue is nonempty, so remove the first customer from the queue,
           register delay, increment the number of customers delayed, and
           schedule departure.'''

            self.spy.list_remove(self.spy.FIRST, self.LIST_QUEUE)
            self.spy.sampst(self.spy.sim_time - self.spy.transfer[1], self.SAMPST_DELAYS)
            self.num_custs_delayed = self.num_custs_delayed + 1
            self.spy.event_schedule(self.spy.sim_time + self.spy.expon(mean_service, self.STREAM_SERVICE),self.EVENT_DEPARTURE)

    def report(self):
        # Get and write out estimates of desired measures of performance.

        print(outfile, "\nDelays in queue, in minutes:\n")
        print("SAMPST_DELAYS", self.SAMPST_DELAYS)
        #out_sampst(outfile, SAMPST_DELAYS, SAMPST_DELAYS)
        print("\nQueue length (1) and server utilization (2):\n")
        print("LIST_QUEUE",self.LIST_QUEUE)
        print("LIST_SERVER",self.LIST_SERVER)
        #out_filest(outfile, LIST_QUEUE, LIST_SERVER)
        print("\nTime simulation ended:%12.3f minutes\n", self.spy.sim_time)
        

if __name__ == "__main__":

    # Open input and output files.
    infile  = read_csv('mm1smlb_in.csv')
    mean_interarrival = infile.iloc[0,0]
    mean_service = infile.iloc[0,1]
    num_delays_required = infile.iloc[0,2]

    outfile = open('mm1smlb_out.csv', 'w+', newline ='')
    # writing the data into the file
    with outfile:    
        write = csv.writer(outfile)
        write.writerow(list(infile.columns))
    
    # Write report heading and input parameters. 
    #print("Single-server queueing system using simlib\n\n")
    #print("Mean interarrival time %11.3f minutes\n\n",outfile.write('mean_interarrival'))
    #print(outfile, "Mean service time%16.3f minutes\n\n", infile['mean_service'])
    #print(outfile, "Number of customers%14d\n\n\n", infile['num_delays_required'])

    # Set maxatr = max(maximum number of attributes per record, 4)
    maxatr = 4

    # Initialize the model
    ssq = singleServerQueueing(mean_interarrival)
    print("Dignotics : \n no of cust delay: {} \n FEL is: {} \n SIM clock:{}\n Next event type: {}".format(ssq.num_custs_delayed, ssq.spy.master[25].print(),ssq.spy.sim_time,ssq.spy.next_event_type))
    #print('List 1 queue ', ssq.spy.master[1].print())
    #print('List 2 Server ', ssq.spy.master[2].print(),'\n\n')


    # Run the simulation while more delays are still needed.
    for i in range(10):
    #while (ssq.num_custs_delayed < num_delays_required):
        #ssq.spy.master[25].print()
        # Determine the next event.
        #print("Dignotics : \n no of cust delay: {} \n FEL is: {} \n SIM clock:{}\n Next event type: {}".format(ssq.num_custs_delayed, ssq.spy.master[25].print(),ssq.spy.sim_time,ssq.spy.next_event_type))
        #print('List 1 queue ', ssq.spy.master[1].print())
        #print('List 2 Server ', ssq.spy.master[2].print(),'\n\n')

        ssq.spy.timing()


        # Invoke the appropriate event function.
        if (ssq.spy.next_event_type == ssq.EVENT_ARRIVAL):
            ssq.arrive(mean_service)
            break
        elif (ssq.spy.next_event_type == ssq.EVENT_DEPARTURE):
            ssq.depart(mean_service)
            break
        else:
            print("error")
        
        
    # Invoke the report generator and end the simulation.

    #ssq.report()

    # fclose(infile)
    # fclose(outfile)

