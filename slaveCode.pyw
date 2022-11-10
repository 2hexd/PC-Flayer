import socket
import time
import threading
import os

IP = "10.0.0.126"
PORT = 5050
ADDR = (IP, PORT)

CONNECTED = False

client = None

def processCommand(cmd, args):
    if cmd == "lock":
        os.system("Rundll32.exe user32.dll,LockWorkStation")
    elif cmd == "restart":
        os.system("shutdown -r -t 00")
    else:
        print('[ERROR] Unknown command: ' + '"' + cmd + '"')

def Receive():
    global CONNECTED
    global client
    while True:
        if CONNECTED == True:
            try:
                msgLength = client.recv(2048).decode("utf-8")
                msg = client.recv(int(msgLength)).decode("utf-8")
                if msg != "":
                    msgList = msg.split(" ")
                    cmd = msgList[0]
                    args = None
                    if msgList:
                        msgList.pop(0)
                        args = msgList
                    processCommand(cmd, args)
            except:
                print("[ERROR] Master disconnected / failed to listen for command.")
                CONNECTED = False
                checkConnection()
                break
        else:
            time.sleep(0.5)
            continue

def checkConnection():
    global CONNECTED
    global client
    while True:
        if CONNECTED == False:
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(ADDR)
                CONNECTED = True
                print("[CLIENT] Successfully connected to master computer!")
                Receive()
                break
            except:
                CONNECTED = False
                print("[ERROR] Failed to connect. Retrying in 5 seconds...")
                time.sleep(5)
                continue

checkConnectionThread = threading.Thread(target=checkConnection)
checkConnectionThread.run()
