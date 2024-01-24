import threading

def a():
    # execution code
    b()

def b():
    # execution code

# Create threads
thread_a = threading.Thread(target=a)
thread_b = threading.Thread(target=b)

# Start threads
thread_a.start()
thread_b.start()

# Wait for both threads to finish
thread_a.join()
thread_b.join()
