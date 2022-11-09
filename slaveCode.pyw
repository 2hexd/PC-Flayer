import socket
import time

IP = "10.0.0.126"
PORT = 5050
ADDR = (IP, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    try:
        client.connect(ADDR)
    except:
        print("[ERROR] Failed connecting to master. Retrying in 5 seconds...")
        time.sleep(5)
        continue
