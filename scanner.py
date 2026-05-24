import socket
import threading
from queue import Queue

target = input("Enter IP or hostname: ")
ip = socket.gethostbyname(target)
print(f"Scanning {ip}")

queue = Queue()
for port in range(1, 1025):
    queue.put(port)

def scan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        if sock.connect_ex((ip, port)) == 0:
            print(f"Port {port} open")
        sock.close()
    except:
        pass

def worker():
    while not queue.empty():
        port = queue.get()
        scan(port)
        queue.task_done()

threads = []
for _ in range(200):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

queue.join()
for t in threads:
    t.join()
print("Done")


