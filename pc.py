# Producer Consumer Problem
# Submitted By: Paras Raj Pahari ( Student ID: 1507360)
# 30th March ,2017

import threading
import time
import random
condition = threading.Condition()

# -----------------------------Producer Thread Class----------------------------------------------------------


class Producer(threading.Thread):
    def run(self):
        global cntC   # Count Variable that counts the consumer loop through the buffer of size 10
        global cntP   # Count Variable that counts the producer loop through the buffer of size 10
        global diff   # Variable that gives the difference of time from start to end
        global b      # Buffer which is dictionary
        global MAX    # MAX size of buffer
        global top    # Top index where producer produces item in the b[top]
        global start  # Variable that notes down the start time of program
        num = -1      # Initialization of number to be produced by producer
        while True:   # While-1 : Loops thread for infinite times until terminated
            condition.acquire()  # Acquire a lock , changes state of thread from unlocked to locked
            # print "--Producer--"  ---> Used while  Debugging
            if top != MAX:       # Checks Whether buffer has reached its maximum size
                # print begin,top,cntC,cntP ---> Used for Debugging
                top += 1         # Increases the  index of buffer to place the item
                if num == 14:    # Checks whether the item has reached the its maximum value, and initialize it again
                    num = -1     # Initializing again , after reaching max value for number item
                num += 1         # Increments the number item
                b[top] = num     # Places the number item in the buffer 'b' at index 'top'
                tme = time.time()*1000  # Converts the epoch time in milliseconds and saves in tme
                producer_file = open('producer.txt','a+')  # Opens the file in append mode
                line = "%d: Placed %d in buffer location %d\n" % (tme,num, top)  # Statement for Output
                diff = tme-start  # Calculates the difference of time from the begin
                producer_file.write(line)   # Writes the 'line' statement to the file
                print line                  # Outputs the 'line' statement to console
                if diff >= 15000:           # Checks whether the thread has reached its termination time of 15 secs
                    line = "\nProducer Terminated!\n"  # Termination Line for output
                    print line                 # Prints the termination 'line' after 15 sec
                    producer_file.write(line)  # Writes the termination 'line' , after 15 sec
                    producer_file.close()   # Closes the file after 15 sec
                    condition.release()     # Releases the thread if it has completed its 15 secs
                    break                   # Gets out of the loop
                producer_file.close()       # Closes the file
                while True:    # While -2 : Waits for Consumer until it equals the loop count of buffer made by Producer
                    if cntP != cntC:
                        condition.notify()   # Notify consumer thread that it's going to release the lock
                        condition.release()  # Release the thread lock
                        time.sleep(random.uniform(0.01,0.1))  # Thread Sleeps for random 10 to 100 milliseconds
                    else:
                        break              # Breaks out of 'While-2' loop
                    condition.acquire()    # Acquires the thread to go into another 'While-2' loop to check cntP!=cntC
                condition.notify()         # Notifies consumer that producer is going to release thread
                condition.release()        # Releases thread after every production
                time.sleep(random.uniform(0.01,0.1))  # Producer sleeps for 10 to 100 milliseconds after producing
            else:
                top = -1                   # Initializes 'top' index to -1 once the buffer reaches the MAX size
                cntP += 1                  # Increases the buffer loop count  after reaching MAX size
                condition.notify()         # Notifies Consumer that producer is going to release the thread
                condition.release()        # Releases the Producer thread
                time.sleep(random.uniform(0.01, 0.1))  # Thread sleeps for random 10 to 100 milliseconds

# ---------------------------------Consumer Thread Class------------------------------------------


class Consumer(threading.Thread):
    def run(self):
        global cntC   # Count Variable that counts the consumer loop through the buffer of size 10
        global cntP   # Count Variable that counts the producer loop through the buffer of size 10
        global b      # Buffer which is dictionary
        global diff   # Variable that gives the difference of time from start to end
        global top    # Top index where producer produces item in the b[top]
        global MAX    # MAX size of buffer
        global begin  # Index from where buffer consumes the number item
        while True:
            condition.acquire()    # Acquires a lock , changes state of thread from unlocked to locked
            if begin != MAX:       # Checks whether consumer has reached the buffers end location
                # print begin,top,cntC,cntP --> Used for Debugging
                # Checks whether buffer index of consumer has exceeded the buffer index of producer
                # Checks whether the producer has produce the data in the buffer location
                if (begin >= top) & (cntC == cntP):
                    condition.notify()   # Notifies Producer, it is going to release the thread
                    condition.release()  # Releases the consumer thread
                    time.sleep(random.uniform(0.01,0.1))   # Consumer Thread sleeps for a random of 10 to 100 ms
                else:
                    # Checks whether buffer is empty and whether the buffer loop count of C is less or equal to P
                    if (top != -1) & (cntC <= cntP):
                        begin += 1    # Increases the index of buffer for consumer to consumer
                        num = b[begin]  # Value of b[begin] thats going to be consumed
                        consumer_file = open('consumer.txt','a+')  # Opens the file 'consumer.txt' in append mode
                        tme = time.time()*1000   # Converts Current epoch time in milliseconds
                        if diff >= 15000:        # Checks for 15 secs
                            line = "\nConsumer Terminated!\n"
                            print line                   # Prints out the 'line' statement
                            # Convert 'diff' milliseconds into seconds and print it
                            print "Elapsed Time: %d seconds" % (int(diff/1000))
                            consumer_file.write(line)   # Writes into file
                            consumer_file.close()   # Closes the file
                            condition.release()    # Releases the thread
                            break                 # breaks the loop once the thread is released after 15 sec
                        line = "%d : Consumed %d from buffer location %d\n" % (tme, num, begin)
                        del b[begin]             # Deletes the number item from corresponding index
                        print line               # Prints 'line'
                        consumer_file.write(line)   # Writes the 'line' into file
                        consumer_file.close()       # Closes 'consumer.txt'
                        condition.notify()          # Notifies another thread it's about to release thread
                        condition.release()         # Releases the thread
                        time.sleep(random.uniform(0.01, 0.1))   # Consumer waits for random time between 10 to 100 ms
                    else:                           # Enters if buffer is empty and waits for producer to produce
                        # print " Whats Up--I am Consumer" -->Used for Debugging
                        condition.notify()
                        condition.release()
                        time.sleep(random.uniform(0.01, 0.1))  # Consumer waits for random time between 10 to 100 ms

            else:
                begin = -1      # Re initialize the begin index once the max size location of buffer reached
                cntC += 1       # Increases the Buffer loop count of consumer
                condition.notify()  # Notifies Producer, that consumer is going to release the thread
                condition.release() # Consumer releases the thread
                time.sleep(random.uniform(0.01, 0.1))   # Waits for consumer for random time between 10 to 100ms

# -------------------------------MAIN-------------------------------------------------------
if __name__ == "__main__":
    MAX = 9   # Initialization of max size
    diff = 0  # Initializing the difference of time
    cntP = 0  # Initializing Producer Buffer loop count
    cntC = 0  # Initializing Consumer Buffer loop count
    top = -1  # Initializing top index for buffer -->used by producer
    begin = -1  # Initializing begin index for buffer  --> used by consumer
    b = {}      # Buffer which is of data structure dictionary
    start = time.time()*1000  # Initial Start time of program

    open('consumer.txt', 'w').close()  # Creates and opens the consumer.txt -> Overwrites with null if old file exists
    open('producer.txt', 'w').close()  # Creates and opens the producer.txt -> Overwrites with null if old file exists
    Producer().start()                 # Starts Producer Thread
    Consumer().start()                 # Starts Consumer Thread


