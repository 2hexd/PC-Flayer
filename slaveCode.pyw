import socket
import time

IP = "10.0.0.126"
PORT = 5050
ADDR = (IP, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
