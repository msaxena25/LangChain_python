import threading
import time

"""

def task():
    print("Task started")
    time.sleep(2)
    print("Task completed")

thread = threading.Thread(target=task) # create thread

thread.start() # start thread
print("Main thread continues")

thread.join() # Wait for a thread to finish 
print("Main thread finished")

'''
Task started
Main thread continues
Task completed
Main thread finished
'''


#---------------------- 

# Example: Stop a background thread with set method

event  = threading.Event()

def task1():
    while not event.is_set():
        print("Task 1 is running")
        time.sleep(1)
    
print('Main thread started..')
thread1 = threading.Thread(name='Thread 1', target=task1) # create thread

thread1.start() # start thread
print('Main thread continues...')
time.sleep(3)
event.set() # set the event to True
print('Main thread finished..')

'''
Main thread started..
Task 1 is running
Main thread continues...
Task 1 is running
Task 1 is running
Main thread finished..
'''

#-------------------------------

# lets use event.set inside another thread

event  = threading.Event()

def task1():
    while not event.is_set():
        print("Task 1 is running")
        time.sleep(1)
    
def task2():
  print('Thread 2 running')
  time.sleep(2)
  event.set() # signal from another thread.
  
print('Main thread started..')
thread1 = threading.Thread(name='Thread 1', target=task1) # create thread
thread2 =  threading.Thread(name='Thread 2', target=task2)
thread1.start() # start thread
print('Main thread continues...')
thread2.start()
print('Main thread finished..')

'''
Main thread started..
Task 1 is running
Main thread continues...
Thread 2 running
Main thread finished..
Task 1 is running
'''


#---------------

# Thread join

def task2():
  print('Thread 2 running')
  time.sleep(2)
  
print('Main thread start')
thread3 = threading.Thread(target=task2)
thread3.start()
thread3.join() # wait for thread to finish
print('Main thread end')

'''
Main thread start
Thread 2 running
Main thread end
'''



#------------------------

# Event wait

event = threading.Event()

def task1():
  print('Thread 1 running')
  event.set() # immediately update to main thread to continue
  time.sleep(1)
  print('thread 1 end')

print('main thread started')
thread1 = threading.Thread(target=task1)
thread1.start()
event.wait() # wait for thread signal from set method to continue here..
print('main thread continue')
print('end')

'''
main thread started
Thread 1 running
main thread continue
end
thread 1 end
'''

"""

#-------------------------------

# Thread Lock

# threading.Lock() allows only one thread at a time to execute a protected (critical or sensitive) section of code. 
# It helps prevent multiple threads from modifying shared data simultaneously.

'''
Task - Banking example to withdraw money from account at the same time.

account_balance = 1000 # initial balance
first_withdraw = 500
second_withdraw = 700

Result = I withdrawn 500 in first trasaction, so second withdraw of 700 must be failed because of insufficent balance.

'''

# lets implement that without Lock - 

account_balance = 1000 # initial balance
first_withdraw = 500
second_withdraw = 700

# define function to check and deduct balance
def withdraw(amount: int, transaction_name: str):
    global account_balance
    print('Transaction ', transaction_name)
    if (amount <= account_balance):
        time.sleep(1) # some transaction is running here..
        account_balance -= amount
        print(f'Amount {amount} withdrawn successfully')
    else:
        print('Insufficient balance')

print('Main thread started')        
thread1 = threading.Thread(target=withdraw, args=(first_withdraw, 'Transaction A'))
thread2 = threading.Thread(target=withdraw, args=(second_withdraw, 'Transaction B'))

thread1.start()  # start first transaction thread
thread2.start() # start sefcond transaction thred

thread1.join() # finish first thread
thread2.join() # finish second thread

print('Final balance ', account_balance)
print('main thread end')

'''
Main thread started
Transaction  Transaction A
Transaction  Transaction B
Amount 500 withdrawn successfully
Amount 700 withdrawn successfully
Final balance  -200
main thread end
'''

# In above example - Final balance is -200 and that violating banking rules.

#----------------------------------------------------------------

# Solution with LOCK

print('Solution with LOCK.......')

lock = threading.Lock() # first create lock object

account_balance = 1000 # initial balance
first_withdraw = 500
second_withdraw = 700

# define function to check and deduct balance
def withdraw_with_lock(amount: int, transaction_name: str):
  with lock:
    global account_balance
    print('Transaction ', transaction_name)
    if (amount <= account_balance):
        time.sleep(1) # some transaction is running here..
        account_balance -= amount
        print(f'Amount {amount} withdrawn successfully')
    else:
        print('Insufficient balance')

print('Main thread started')        
thread1 = threading.Thread(target=withdraw_with_lock, args=(first_withdraw, 'Transaction A'))
thread2 = threading.Thread(target=withdraw_with_lock, args=(second_withdraw, 'Transaction B'))

thread1.start()  # start first transaction thread
thread2.start() # start sefcond transaction thred

thread1.join() # finish first thread
thread2.join() # finish second thread

print('Final balance ', account_balance)
print('main thread end')

'''
Main thread started
Transaction  Transaction A
Amount 500 withdrawn successfully
Transaction  Transaction B
Insufficient balance
Final balance  500
main thread end
'''
