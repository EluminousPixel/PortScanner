from queue import Queue
import datetime
import socket
import threading

target = "192.168.1.1" # The target is the IP we are using to look at the open and closed ports
queue = Queue() # Holds all the ports that are waiting to be processed 
open_ports = [] # Contains all the open ports 

def portscan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        return True
    except:
        return False
    
def get_ports(mode):
    if mode == 1: # Scans all the standardized ports
        for port in range(1, 1024):
            queue.put(port)
    elif mode == 2: # This mode adds all of the reserved ports 
        for port in range(1, 49152):
            queue.put(port)
    elif mode == 3: # Uses an array of all common ports
        ports = [20, 21, 22, 23, 25, 53, 80, 11, 443]
        for port in ports:
            queue.put(port)
    elif mode == 4: # Takes a user input for one or more specific ports
        ports = input("Enter your ports (seperate by blank): ")
        ports = ports.split()
        ports = list(map(int, ports))
        for port in ports:
            queue.put(port)

def worker():
    while not queue.empty():
        port = queue.get()
        if portscan(port):
            print("Port {} is open!".format(port))
            open_ports.append(port)

def run_scanner(threads, mode):

    get_ports(mode)

    thread_list = []

    for t in range(threads):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)
    
    for thread in thread_list:
        thread.start()
    
    for thread in thread_list:
        thread.join()

    print("Open ports are:", open_ports)
    with open("open_ports_log.txt", mode='a') as file:
        file.write("%s - Open ports in this report are: %s" % 
                   (datetime.datetime.now(), open_ports))
        file.write("\n")

run_scanner(100, 2)

        
